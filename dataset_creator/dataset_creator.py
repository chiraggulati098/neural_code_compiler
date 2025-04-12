import streamlit as st
import numpy as np
import pandas as pd
import os
from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
file_path = os.path.join(root_dir, "dataset.csv")
img_folder = os.path.join(root_dir, "dataset_creator", "images")

# ---------------------------------------- FUNCTIONS ----------------------------------------

def dataset_csv_exists(file_path):
    """
    Check if the dataset.csv file exists in the specified path.
    If it doesn't exist, create an empty DataFrame with specified columns and save it as dataset.csv.
    """
    if not os.path.exists(file_path):
        print(f"{file_path} doesn't exist.")
        df = pd.DataFrame(columns=["img_name", "ground_truth"])
        df.to_csv("dataset.csv", index=False)
        print(f"{file_path} created with columns - img_name and ground_truth")
    else:
        print(f"{file_path} already exists.")

def open_csv(file_path):
    """
    Open the dataset.csv file and return its contents as a DataFrame.
    """
    df = pd.read_csv(file_path)
    return df

def save_csv(file_path, df):
    """
    Save the DataFrame to the dataset.csv file.
    """
    df.to_csv("dataset.csv", index=False)
    print(f"Data saved to {file_path}")

def get_code_from_image(img_path):
    """
    Use the Gemini API to extract code from the image at img_path.
    The image is expected to be a PNG file.
    """
    with open(img_path, "rb") as img_file:
        image_data = img_file.read()
    
    client = genai.Client(api_key = GEMINI_API)
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",  
        contents=[
            "Extract and return only the code written in this image. The code is handwritten and in C or C++. Do not include any explanations or comments or even tripple backticks, just give me the code as plain text.\nCode:",
            types.Part.from_bytes(data=image_data, mime_type="image/png")  
        ]
    )
    
    return(response.text)

def get_unprocessed_images(df):
    # Get all PNG files from the images folder
    all_images = [f for f in os.listdir(img_folder) if f.endswith('.png')]
    # Filter out images that are already in the DataFrame
    processed_images = set(df['img_name'].tolist())
    return [img for img in all_images if img not in processed_images]

# ---------------------------------------- LOGIC ----------------------------------------

dataset_csv_exists(file_path)
df = open_csv(file_path)

# Initialize session state for image processing
if 'unprocessed_images' not in st.session_state:
    st.session_state.unprocessed_images = get_unprocessed_images(df)

if 'current_image' not in st.session_state:
    st.session_state.current_image = st.session_state.unprocessed_images[0] if st.session_state.unprocessed_images else None

if 'output_code' not in st.session_state:
    st.session_state.output_code = ""

# ---------------------------------------- UI ----------------------------------------

st.set_page_config(layout="wide")
st.title("Dataset Creator")

col1, col2 = st.columns(2)

with col1:
    st.header("Code Image")
    if st.session_state.current_image:
        st.image(f"{img_folder}/{st.session_state.current_image}")
        st.text(f"Current image: {st.session_state.current_image}")
    else:
        st.write("All images processed!")

with col2:
    st.header("Ground Truth")
    if st.session_state.current_image and not st.session_state.output_code:
        output = get_code_from_image(f"{img_folder}/{st.session_state.current_image}")
        st.session_state.output_code = output
    
    # Use session state for the text area
    st.session_state.output_code = st.text_area("Code", st.session_state.output_code, height=450)

    col2_1, col2_2, col2_3 = st.columns(3)
    with col2_1:
        skip = st.button("Skip", type="primary", use_container_width=True)
    with col2_2:
        generate = st.button("Generate", type="secondary", use_container_width=True)
    with col2_3:
        save = st.button("Save", type="primary", use_container_width=True)
    
    if generate and st.session_state.current_image:
        # Regenerate the code from the current image
        output = get_code_from_image(f"{img_folder}/{st.session_state.current_image}")
        st.session_state.output_code = output
        st.rerun()

    if save:
        # Add the current image and code to the dataset
        new_row = pd.DataFrame({
            'img_name': [st.session_state.current_image],
            'ground_truth': [st.session_state.output_code]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        save_csv(file_path, df)
        st.success(f"Saved {st.session_state.current_image} to dataset!")
        
        # Move to next image
        st.session_state.unprocessed_images.remove(st.session_state.current_image)
        st.session_state.current_image = st.session_state.unprocessed_images[0] if st.session_state.unprocessed_images else None
        st.session_state.output_code = ""
        st.rerun()
    
    if skip:
        # Move to next image without saving
        st.session_state.unprocessed_images.remove(st.session_state.current_image)
        st.session_state.current_image = st.session_state.unprocessed_images[0] if st.session_state.unprocessed_images else None
        st.session_state.output_code = ""
        st.rerun()