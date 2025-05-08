# Real-Time Deepfake Detector

A web-based application that detects deepfake images and videos using a trained deep learning model. It supports real-time webcam detection as well as uploaded media.

# Features

-  Upload and detect deepfakes in images and videos
-  Real-time detection using your webcam
-  FastAPI backend with a simple and responsive frontend
-  Pre-trained deep learning model for accurate classification
# Project Structure

real-time-deepfake-detector/
│
├── backend/ # FastAPI backend
│ ├── detect_utils.py # Prediction logic
│ ├── main.py # API routes
│
├── frontend/ # HTML, CSS, JS frontend
│ ├── index.html
│ ├── style.css
│ └── script.js
│
├── model/ # Saved deepfake detection model
│ └── xception_model.h5
│
├── data/ # (Optional) Dataset samples
│
├── static/uploads/ # Temporarily stores uploaded files
│
├── .gitignore
├── README.md


# Installation & Run
# Prerequisites
- Python 3.8+
- Git
# Install Dependencies
pip install -r requirements.txt

# Run the Backend (FastAPI)
uvicorn backend.main:app --reload
# Open the Frontend
Open frontend/index.html in your browser

# References
Kaggle Deepfake Dataset
TensorFlow, OpenCV, FastAPI, JavaScript
Various academic papers on deepfake detection

