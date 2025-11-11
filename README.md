# 🌿 AI-Powered Pest Detection Web App

A complete **Flask-based web application** that uses a **YOLOv8 deep learning model** to detect plant pests from uploaded images.  
The app not only performs pest detection but also provides additional pest information (pesticides and insecticides), shows sample reference images for each detected pest, and supports **multi-language translation** through **Google Translate**.

---

## 🧩 Features

✅ **YOLOv8 Object Detection** – Detects multiple pest species from uploaded images.  
✅ **Information Lookup** – Fetches pest-specific control info (pesticides & insecticides) from `info.json`.  
✅ **Sample Reference Images** – Displays example pest images for user comparison.  
✅ **Google Translate Integration** – Supports major Indian languages (Hindi, Tamil, Bengali, etc).  
✅ **Duplicate-Free Results** – Only one entry per unique detected pest.  
✅ **Clean Modern UI** – Built with responsive HTML + CSS.  
✅ **Error Handling** – Graceful messages for missing files or no detections.  

---

## 📁 Project Structure

```
project/
│
├── app.py                  # Main Flask application
├── best.pt                 # Trained YOLOv8 model weights
├── info.json               # Pest information file (pesticides/insecticides)
├── uploads/                # Uploaded images folder
├── results/                # Temporary results (annotated images)
├── samples/                # Contains sample reference images for pests
│   ├── White Fly/
│   │   ├── sample1.jpg
│   │   ├── sample2.jpg
│   ├── Stem Fly/
│   └── Grey Weevil/
│
├── templates/
│   ├── home.html           # Upload page
│   └── predict.html        # Detection results page
│
├── static/
│   └── style.css           # Global styling
│
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/plant-pest-detector.git
cd plant-pest-detector
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

**Example `requirements.txt`:**
```
flask
ultralytics
pillow
```

---

## 🧠 How It Works

### 🔹 Step 1: Upload Image
The user uploads a photo of a plant leaf or stem.

### 🔹 Step 2: YOLO Model Inference
The app uses `ultralytics.YOLO` to predict pest locations and labels.

```python
results = model.predict(source=image_path, conf=0.25, save=False)
```

### 🔹 Step 3: Unique Pest Extraction
Each pest label appears only once in the results — the app keeps the highest-confidence detection.

```python
if label not in predictions or conf > predictions[label]["confidence"]:
    predictions[label] = {...}
```

### 🔹 Step 4: Info Lookup
The label name is used as a key in `info.json` to fetch related data.

**Example `info.json`:**
```json
{
  "White Fly": {
    "pesticides": "Imidacloprid, Thiamethoxam",
    "insecticides": "Neem oil, Spinosad"
  },
  "Stem Fly": {
    "pesticides": "Chlorpyrifos, Cypermethrin",
    "insecticides": "Fipronil, Lambda-cyhalothrin"
  }
}
```

### 🔹 Step 5: Annotated Image
YOLO’s `result.plot()` generates a bounding-box image that’s converted to base64 for browser display.

### 🔹 Step 6: Sample Image Section
The app searches `/samples/<label>/` to show a few sample pest images for user comparison.

---

## 🌐 Multi-Language Translation

Integrated with Google Translate API for **inline page translation**.

```html
<div id="google_translate_element"></div>
<script type="text/javascript">
  function googleTranslateElementInit() {
    new google.translate.TranslateElement({
      pageLanguage: 'en',
      includedLanguages: 'en,hi,bn,ta,te,ml,kn,gu,mr,pa,or,as,sd,ne',
      layout: google.translate.TranslateElement.InlineLayout.SIMPLE
    }, 'google_translate_element');
  }
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
```

---

## 🎨 UI Breakdown

### **1️⃣ `home.html`**
- Uploads the image via `<form>` to `/predict`.
- Uses a clean layout with white card and green accent.

### **2️⃣ `predict.html`**
- Displays detected pests, confidence, and their pesticide info.
- Shows annotated image and sample references.
- Includes “🔙 Go Back” button.
- Clicking on a **sample image** opens it in full screen (lightbox effect).

---

## 💻 Backend (Flask App Overview)

### **Key Functions in `app.py`**

#### 🧩 `allowed_file(filename)`
Ensures only `.jpg`, `.jpeg`, and `.png` files are accepted.

#### 🧩 `get_sample_images(predictions)`
Finds up to 2 sample reference images for each detected pest from `/samples/<label>/`.

#### 🧩 `run_inference(image_path)`
Performs YOLO prediction, filters duplicates, retrieves pest info, and encodes the annotated image.

#### 🧩 `/predict` Route
- Accepts uploaded file.
- Validates it.
- Runs inference.
- Renders results in `predict.html`.

#### 🧩 `/` Route
- Renders the `home.html` upload page.

---

## 🧾 Example Output

| Label | Confidence | Pesticides | Insecticides |
|--------|-------------|-------------|---------------|
| **White Fly** | 0.92 | Imidacloprid, Thiamethoxam | Neem oil, Spinosad |
| **Stem Fly** | 0.85 | Chlorpyrifos, Cypermethrin | Fipronil, Lambda-cyhalothrin |

---

## 🚀 Run the App

```bash
python app.py
```

App will run on:
> http://127.0.0.1:5000/
