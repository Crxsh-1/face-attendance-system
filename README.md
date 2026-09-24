# Local Face Attendance System

A consent-based local face recognition and attendance system built for learning computer vision.

## Planned V1 Features

- Webcam face detection
- Consent-based participant registration
- Local face recognition
- Attendance recording
- Duplicate attendance prevention
- Attendance history
- CSV export
- Participant deletion
- Local-only biometric data processing

## Privacy

Face images, biometric data, databases, and attendance records are intended to remain local and are excluded from version control.

## Development Environment

The project targets **Python 3.12 64-bit** on Windows. Use the Python launcher to create the local virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install opencv-contrib-python numpy Pillow pytest
```

The current environment was verified with:

- Python 3.12.4
- opencv-contrib-python 5.0.0.93 (OpenCV 5.0.0)
- NumPy 2.5.3
- Pillow 12.3.0
- pytest 9.1.1
- Tkinter/Tcl 8.6 / 8.6.13

OpenCV and NumPy are installed in `.venv`; no face-recognition models have been downloaded yet. Models will be obtained later only from approved, documented sources.

The following packages are intentionally not installed: MediaPipe, dlib, face_recognition, DeepFace, InsightFace, TensorFlow, and PyTorch.

Basic verification commands:

```powershell
python -c "import cv2, numpy, PIL, pytest, tkinter; print(cv2.__version__)"
python -m pip check
```

## Status

Project environment setup complete. Application code and model downloads are pending.
