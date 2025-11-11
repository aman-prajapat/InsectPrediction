from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import io
import base64
from PIL import Image
import traceback
import json  # <-- Added

# ---------------- CONFIG ----------------
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
SAMPLES_FOLDER = os.path.join(BASE_DIR, "samples")
INFO_JSON = os.path.join(BASE_DIR, "info.json")  # <-- Added

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- LOAD MODEL ----------------
try:
    model = YOLO(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)
    model = None

# ---------------- LOAD INFO JSON ----------------
try:
    with open(INFO_JSON, "r", encoding="utf-8") as f:
        label_info = json.load(f)
    print("Info JSON loaded!")
except Exception as e:
    print("Could not load info.json:", e)
    label_info = {} 

# ---------------- SAMPLE IMAGES ----------------
def get_sample_images(predictions, max_per_label=2):
    sample_images = {}
    for pred in predictions:
        label = pred['label']
        label_folder = os.path.join(SAMPLES_FOLDER, label)
        if os.path.exists(label_folder):
            files = [f for f in os.listdir(label_folder) if allowed_file(f)]
            files = files[:max_per_label]
            imgs_b64 = []
            for f in files:
                path = os.path.join(label_folder, f)
                with open(path, "rb") as image_file:
                    encoded_img = base64.b64encode(image_file.read()).decode('utf-8')
                    imgs_b64.append(encoded_img)
            sample_images[label] = imgs_b64
    return sample_images

# ---------------- HELPERS ----------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def run_inference(image_path):
    try:
        results = model.predict(source=image_path, conf=0.25, save=False)
        result = results[0]
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return [], None

        predictions = {}
        for box in boxes:
            cls_id = int(box.cls)
            label = result.names[cls_id]
            conf = float(box.conf)

            # Only store if label not already added or if this detection has higher confidence
            if label not in predictions or conf > predictions[label]["confidence"]:
                info = label_info.get(label, {"pesticides": "No info available", "insecticides": "No info available"})
                predictions[label] = {
                    "label": label,
                    "confidence": round(conf, 3),
                    "info": info
                }

        # Convert dict → list
        predictions = list(predictions.values())

        # Annotated image
        annotated_img = result.plot()
        image_pil = Image.fromarray(annotated_img[:, :, ::-1])
        buffer = io.BytesIO()
        image_pil.save(buffer, format="JPEG")
        encoded_img = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return predictions, encoded_img

    except Exception as e:
        traceback.print_exc()
        return None, str(e)

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('predict.html', error="Model not loaded!")

    if 'file' not in request.files:
        return render_template('predict.html', error="No file uploaded!")

    file = request.files['file']

    if file.filename == '':
        return render_template('predict.html', error="No file selected!")

    if file and allowed_file(file.filename):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        predictions, encoded_img = run_inference(filepath)

        if encoded_img is None:
            return render_template('predict.html', error="No detections found!")

        sample_images = get_sample_images(predictions)

        return render_template(
            'predict.html',
            predictions=predictions,
            image_data=encoded_img,
            sample_images=sample_images
        )
    else:
        return render_template('predict.html', error="Invalid file type! Only JPG/PNG allowed.")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
