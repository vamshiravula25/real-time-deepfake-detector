
let detectionInterval;

let videoStream;

let isProcessingFile = false;  
let isProcessingWebcam = false;  

function uploadFile() {
    const input = document.getElementById('fileInput');
    const file = input.files[0];
    const result = document.getElementById('result');
    const loading = document.getElementById('loading');
    const imagePreview = document.getElementById('imagePreview');
    const videoPreview = document.getElementById('videoPreview');

    if (!file) {
        result.innerText = "Please select a file.";
        return;
    }

    // Set flag to true to indicate that file is being processed
    isProcessingFile = true;
    isProcessingWebcam = false;  // Stop webcam processing
    result.innerText = '';  // Reset result
    loading.innerText = 'Analyzing...';

    // Reset views
    imagePreview.style.display = 'none';
    videoPreview.style.display = 'none';

    // Preview
    const fileURL = URL.createObjectURL(file);
    if (file.type.startsWith('image/')) {
        imagePreview.src = fileURL;
        imagePreview.style.display = 'block';
    } else if (file.type.startsWith('video/')) {
        videoPreview.src = fileURL;
        videoPreview.style.display = 'block';
    }

    // Upload
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (isProcessingFile) {  // Only update result if it's file processing
            loading.innerText = '';
            result.innerText = `Result: ${data.result} (${data.confidence}%)`;
        }
    })
    .catch(err => {
        loading.innerText = '';
        result.innerText = 'Error during upload';
        console.error(err);
    });
}

function startCamera() {
    const videoElement = document.getElementById('video');
    
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            videoStream = stream;
            videoElement.srcObject = stream;
            isProcessingWebcam = true;  // Flag for webcam processing
            detectFromWebcam();  // Start webcam detection
        })
        .catch(err => {
            console.error('Error accessing camera', err);
        });
    }
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());  // Stop camera
    }
    isProcessingWebcam = false;  // Flag to stop webcam processing
}

// Capture frame and send to backend
function captureFrame() {
    const videoElement = document.getElementById('video');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('file', blob, 'frame.jpg');

        fetch('http://localhost:8000/detect-frame', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (isProcessingWebcam) {  // Only update result if it's webcam processing
                document.getElementById('result').innerText = `Result: ${data.result} (${data.confidence}%)`;
            }
        })
        .catch(err => {
            console.error('Error in real-time detection', err);
        });
    });
}

// Detect from webcam continuously
function detectFromWebcam() {
    setInterval(() => {
        if (isProcessingWebcam) {
            captureFrame();
        }

    }, 1000); // Every second
}
