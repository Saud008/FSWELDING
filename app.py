from flask import Flask, request, jsonify, render_template, url_for, redirect
from ultralytics import YOLO
from PIL import Image, ImageDraw
import os
import uuid
from werkzeug.utils import secure_filename

# Initialize the Flask app
app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the YOLO model
MODEL_PATH = "weights/best.pt"
model = YOLO(MODEL_PATH)
print("YOLO model loaded successfully!")

# Define a function to perform inference and draw bounding boxes
def predict_image(image_path):
    # Perform inference using the YOLO model
    results = model.predict(source=image_path, save=False, conf=0.25)  # Adjust confidence threshold as needed
    
    # Open the image using Pillow
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    # Extract predictions
    predictions = results[0].boxes.data.cpu().numpy()
    print(predictions)
    formatted_results = []
    for pred in predictions:
        x1, y1, x2, y2, confidence, class_id = pred
        class_id = int(class_id)
        
        if class_id == 0:
            continue

        formatted_results.append({
            "x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "confidence": float(confidence),
            "class_id": int(class_id)
        })
        # Draw bounding box and label on the image
        classes = {1:"flash",2:"channel",3:"cavity",4:"crack"}
        colors = {1:"red",2:"green",3:"blue",4:"yellow"}
        label = f"{classes[int(class_id)]}: {confidence*100:.2f}"
        draw.rectangle([x1, y1, x2, y2], outline=colors[class_id], width=3)
        draw.text((x1, y1 - 10), label, fill="black")

    # Save the image with bounding boxes
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"result_{os.path.basename(image_path)}")
    image.save(output_path)

    return formatted_results, output_path

@app.route("/home")
def home():
    result = request.args.get("result", None)
    image_url = request.args.get("image_url", None)
    return render_template("upload.html", result=result, image_url=image_url)

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # try:
    # Save the uploaded image temporarily
    filename = secure_filename(str(uuid.uuid4()) + os.path.splitext(file.filename)[-1])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Perform inference and get the output image path
    predictions, output_path = predict_image(file_path)

    # Redirect to the home page with the results
    return redirect(url_for('home', result=predictions, image_url=url_for('static', filename=f'uploads/{os.path.basename(output_path)}')))
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)