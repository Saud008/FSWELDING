# Friction Stir Welding Defect Detection using YOLOv8

## Project Overview
This project focuses on detecting defects in Friction Stir Welding (FSW) using the YOLOv8 object detection model. The system classifies welding defects into four categories:
- **Channel**
- **Flash**
- **Cavity**
- **Crack/Groove**

The implementation leverages YOLOv8 for accurate and real-time defect detection, improving the efficiency and reliability of welding inspections.

---

## Project Structure
```
FSWelding-Project/
|
|-- dataset/
|   |-- images/
|       |-- train/          # Training images
|       |-- test/           # Test images
|   |-- labels/
|       |-- train/          # Training labels
|       |-- test/           # Test labels
|   |-- data.yaml           # Dataset configuration file
|
|-- runs/                   # Output folder for YOLO results
|
|-- requirements.txt        # Dependencies
|-- train.py                # Training script
|-- predict.py              # Inference script
|-- README.md               # Project documentation
```

---

## Installation
### Prerequisites
- Python 3.8+
- Google Colab (recommended for ease of setup)

### Steps
1. Clone the repository.
2. Install the required dependencies.
3. Install YOLOv8 using the Ultralytics library.

---

## Dataset Preparation
Ensure your dataset is organized as follows:
- Images are stored in `dataset/images/train` and `dataset/images/test`.
- Corresponding labels are in YOLO format under `dataset/labels/train` and `dataset/labels/test`.

Modify the `data.yaml` file to include paths for training and testing images, the number of classes (nc), and their names.

---

## Training the Model
The training process involves loading YOLOv8 with a pre-trained model (e.g., `yolov8n.pt`), specifying dataset paths, and defining hyperparameters such as the number of epochs, batch size, and image size. The training outputs include metrics and model weights saved in the `runs/detect` folder.

---

## Inference
Inference can be run on test images to detect defects. Predictions, including bounding boxes and classifications, are saved in the `runs/detect` folder for further analysis.

---

## Visualizations
### Metrics and Graphs
1. **Confusion Matrix**: Evaluate the model’s performance in classifying defects.
2. **Training Loss Graphs**: Visualize loss metrics (box loss, objectness loss, classification loss) over epochs.
3. **Precision-Recall Curve**: Analyze model’s precision and recall for each class.

Metrics and graphs provide insights into the model’s learning process and its ability to generalize to unseen data.

---

## Exporting the Model
After training, the model can be exported to various formats such as TorchScript, ONNX, or CoreML for deployment in different environments.

---

## Deployment
The trained model can be integrated into real-time applications such as Flask-based web apps or edge devices for monitoring welding defects. Batch inference capabilities allow for processing multiple images simultaneously.

