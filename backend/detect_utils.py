import numpy as np
import cv2
from tensorflow.keras.models import load_model
from mtcnn.mtcnn import MTCNN

model = load_model('model/xception_model.h5')
detector = MTCNN()

def extract_face(img_path):
    image = cv2.imread(img_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(image_rgb)

    if not faces:
        return None

    x, y, w, h = faces[0]['box']
    x, y = max(0, x), max(0, y)
    face = image_rgb[y:y+h, x:x+w]

    face = cv2.resize(face, (299, 299))
    face = face.astype('float32') / 255.0
    return np.expand_dims(face, axis=0)

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np




def predict(file_path):
    

    if file_path.endswith('.mp4'):
        return predict_video(file_path)
    else:
        face = extract_face(file_path)
        if face is None:
            return "No face detected", 0.0
        pred = model.predict(face)[0][0]

        confidence = round(pred * 100, 2)  
        
        if pred > 0.5:
            label = "FAKE"
            confidence = round(pred * 100, 2)  
        else:
            label = "REAL"
            confidence = round((1 - pred) * 100, 2)  

        return label, confidence

def predict_video(video_path):
    cap = cv2.VideoCapture(video_path)
    predictions = []
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret or count > 30:
            break
        if count % 5 == 0:
            cv2.imwrite("temp.jpg", frame)
            face = extract_face("temp.jpg")
            if face is not None:
                pred = model.predict(face)[0][0]
                predictions.append(pred)
        count += 1
    cap.release()
    if not predictions:
        return "No face detected", 0.0
    avg = np.mean(predictions)
    label = "FAKE" if avg > 0.5 else "REAL"
    confidence = round(avg * 100, 2) if label == "FAKE" else round((1 - avg) * 100, 2)
    return label, confidence
def predict_frame(frame):
    # Convert BGR (OpenCV) to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(image_rgb)

    if not faces:
        return "No face detected", 0.0

    x, y, w, h = faces[0]['box']
    x, y = max(0, x), max(0, y)
    face = image_rgb[y:y+h, x:x+w]
    face = cv2.resize(face, (299, 299))
    face = face.astype('float32') / 255.0
    face = np.expand_dims(face, axis=0)

    pred = model.predict(face)[0][0]
    label = "FAKE" if pred > 0.5 else "REAL"
    confidence = round(pred * 100, 2) if label == "FAKE" else round((1 - pred) * 100, 2)
    return label, confidence
# In detect_utils.py
def predict_image_from_bytes(image: np.ndarray):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face = extract_face_from_image(img_rgb)
    if face is None:
        return "No face detected", 0.0
    pred = model.predict(face)[0][0]
    label = "FAKE" if pred > 0.5 else "REAL"
    confidence = round(pred * 100, 2) if label == "FAKE" else round((1 - pred) * 100, 2)
    return label, confidence

def extract_face_from_image(image):
    faces = detector.detect_faces(image)
    if not faces:
        return None
    x, y, w, h = faces[0]['box']
    face = image[y:y+h, x:x+w]
    face = cv2.resize(face, (299, 299))  # Match model input
    face = face.astype('float32') / 255.0
    return np.expand_dims(face, axis=0)
