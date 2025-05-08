import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.detect_utils import predict, predict_image_from_bytes
from io import BytesIO
import cv2
import numpy as np


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_path = f"static/uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    
    prediction = predict(upload_path)
    result = prediction[0]
    confidence = prediction[1]
    os.remove(upload_path) 
    return {
    "result": str(result),
    "confidence": float(confidence)
    }

@app.post("/detect-frame")
async def detect_frame(file: UploadFile = File(...)):
    # Read the uploaded image (frame from webcam)
    contents = await file.read()
    image = np.array(bytearray(contents), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Process the image with deepfake detection
    result, confidence = predict_image_from_bytes(image)
    return {"result": str(result), "confidence": float(confidence)}
