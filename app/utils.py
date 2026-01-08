from ultralytics import YOLO
import os
import time
from datetime import datetime
from PIL import Image
import cv2

# ================= PATHS =================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'models', 'model.safetensors')

# ================= MODEL CACHE =================
_model = None

def get_model():
    global _model
    if _model is None:
        print(f"📦 Loading YOLO model from {MODEL_PATH}")
        _model = YOLO(MODEL_PATH)
        print("✅ Model loaded")
    return _model


# ================= HELPERS =================
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def detect_fruits(image_path, result_folder):
    model = get_model()   # ✅ SAFE CALL

    results = model.predict(
        source=image_path,
        conf=0.5,
        iou=0.45,
        save=False,
        verbose=False
    )

    result = results[0]

    result_filename = f"result_{int(time.time())}_{os.path.basename(image_path)}"
    result_path = os.path.join(result_folder, result_filename)

    annotated_img = result.plot()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB)
    Image.fromarray(annotated_img).save(result_path)

    predictions = []
    if result.boxes:
        for box in result.boxes:
            predictions.append({
                "class": result.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })

    class_counts = {}
    for p in predictions:
        class_counts[p["class"]] = class_counts.get(p["class"], 0) + 1

    return {
        "success": True,
        "result_image": result_filename,
        "predictions": predictions,
        "total_detections": len(predictions),
        "class_counts": class_counts,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def cleanup_old_files(folder_path, max_age_hours=24):
    now = time.time()
    max_age = max_age_hours * 3600

    for f in os.listdir(folder_path):
        fp = os.path.join(folder_path, f)
        if os.path.isfile(fp) and now - os.path.getmtime(fp) > max_age:
            try:
                os.remove(fp)
            except Exception as e:
                print(f"⚠️ Could not delete {fp}: {e}")
