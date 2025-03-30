# **Handwritten Code OCR**

## **1. Introduction**
This project focuses on **fine-tuning Microsoft's Transformer-based OCR model (TrOCR)** for recognizing **handwritten Python code** from images. The ultimate goal is to build a **Neural Compiler** capable of converting handwritten code into executable scripts.

---

## **2. Dataset Collection**
The dataset used for fine-tuning consists of **55 handwritten Python code snippets** obtained from a research study on **Handwritten Code Recognition for Pen-and-Paper CS Education**.

### **📌 Citation for Dataset**
> Md Sazzad Islam, Moussa Koulako Bala Doumbouya, Christopher D. Manning, Chris Piech,  
> "Handwritten Code Recognition for Pen-and-Paper CS Education,"  
> *Proceedings of the Eleventh ACM Conference on Learning @ Scale (L@S '24)*, 2024.  
> [Paper Link](https://web.stanford.edu/~cpiech/bio/papers/handwrittencode.pdf)

GitHub Repository for the dataset and implementation:  
[CodeOCR GitHub](https://github.com/mdoumbouya/codeocr/tree/main)

Each sample consists of:
- **An image** containing a handwritten Python snippet.
- **A ground truth label** representing the corresponding text.

---

## **3. Preprocessing Images**
To ensure the images are compatible with the Transformer OCR model, the following preprocessing steps were applied:

✅ **Converted grayscale images to RGB** (TrOCR expects 3-channel input).  
✅ **Rescaled pixel values** to 0–255.  
✅ **Normalized images** to match model input format.

### **🔹 Libraries Used:**
- `PIL`: Convert images and ensure correct format.
- `NumPy`: Normalize and preprocess image data.
- `Matplotlib`: Visualizing images.

---

## **4. Fine-Tuning Microsoft TrOCR Model**
We fine-tuned the **Microsoft TrOCR base model** using our **55 examples**.

### **Training Setup**
- **Model:** `microsoft/trocr-base-handwritten`
- **Batch Size:** `4`
- **Epochs:** `10`
- **Optimizer:** Adam
- **Loss Function:** Cross-entropy

### **🔹 Libraries Used & Why?**
- `transformers`: Load and fine-tune the **TrOCR model**.
- `torch`: Handle training, tensors, and GPU acceleration.
- `datasets`: Manage dataset preparation.

### **Model Saving**
After training, the fine-tuned model was saved using:
```
model.save_pretrained("model_dir") processor.save_pretrained("model_dir")
```


---

## **6. Future Work**
While the model shows promising results, there are several improvements to be made:

### **🔹 Dataset Expansion**
- Collect and annotate a **larger dataset** to improve generalization.
- Include handwritten code from **multiple sources** to handle variations in handwriting.

### **🔹 Enhancing Language Support**
- Extend support to **C and C++** handwritten code recognition.
- Implement **language detection** to classify input code before processing.

### **🔹 Fine-Tuning with ABC Algorithm**
- Use **Artificial Bee Colony (ABC) optimization** to improve model fine-tuning.
- Apply ABC for **post-OCR correction**, refining the extracted code before execution.

### **🔹 Final Goal: Image-to-Code Execution Pipeline**
- Develop a **full pipeline** where:
  1. A user uploads a **handwritten code image**.
  2. The system **recognizes and converts it** into digital text.
  3. The extracted code is **compiled and executed** automatically.

---

## **7. Conclusion**
This project lays the foundation for a **Neural Compiler** capable of **translating handwritten code into executable scripts**. By expanding the dataset, supporting multiple languages, and integrating an execution pipeline, we aim to create an AI-powered system for handwritten code recognition and execution. 
