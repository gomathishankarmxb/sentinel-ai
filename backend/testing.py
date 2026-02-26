from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import cv2
import numpy as np
import io
from PIL import Image

app = FastAPI()

#YOLO model loading
model = YOLO("yolov8n.pt")

SUSPICIOUS_CLASSES = ["knife", "baseball bat", "cell phone"]


@app.get("/")
def home():
    return {"status": "Sentinel AI is Online"}


@app.post("/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    # Read the uploaded image
    request_object_content = await file.read()
    img = Image.open(io.BytesIO(request_object_content))
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


    results = model(img_cv)

    detections = []
    alert_triggered = False

    for r in results:
        for box in r.boxes:
            class_name = model.names[int(box.cls[0])]
            confidence = float(box.conf[0])

            # Check if object is in our suspicious list
            if class_name in SUSPICIOUS_CLASSES and confidence > 0.5:
                alert_triggered = True
                detections.append({
                    "object": class_name,
                    "confidence": confidence,
                    "location": box.xyxy[0].tolist()
                })

    return {
        "alert": alert_triggered,
        "detections": detections,
        "message": "Suspicious activity detected!" if alert_triggered else "Region clear."
    }