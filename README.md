# Face Attendance System

A local, consent-based face attendance application built with Python, OpenCV, YuNet, SFace, SQLite, and Tkinter.

## Features

- Local face enrollment
- Explicit consent confirmation during enrollment
- Local face embeddings stored in SQLite
- Face detection using OpenCV YuNet
- Face recognition using OpenCV SFace
- Attendance recorded once per participant per day
- Attendance history
- CSV export
- Participant management
- Participant deletion
- Local-only operation
- Automated tests

## Privacy

This project is designed for local, consent-based use.

- Face data is stored locally on the computer.
- Face data is not uploaded to a cloud service by this application.
- Enrollment requires confirmation that the participant has given consent.
- Participants can be deleted through the application.
- The `data/` and `attendance/` directories are excluded from Git.

Only enroll people who have knowingly agreed to participate.

## Requirements

- Windows
- Python 3.12
- Webcam
- Git

The application uses:

- OpenCV Contrib
- NumPy
- Pillow
- Tkinter
- SQLite
- pytest for testing

## Models

The application uses OpenCV Zoo models:

- YuNet for face detection
- SFace for face recognition

The model files are stored locally under:

```text
models/
├── yunet/
│   └── face_detection_yunet_2023mar.onnx
└── sface/
    └── face_recognition_sface_2021dec_int8.onnx
```

Models are not automatically downloaded by the application.

## Setup

Create the virtual environment with Python 3.12:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Make sure the required model files are present under `models/`.

## Run the Application

From the project root:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\python -m app.ui.main_window
```

The main window provides:

- **Enroll Participant**
- **Start Recognition**
- **Attendance History**
- **Manage Participants**
- **Export CSV**

## Enrollment

1. Open the application.
2. Select **Enroll Participant**.
3. Enter the participant's name.
4. Confirm that the participant has given consent.
5. Make sure exactly one face is visible.
6. Press `SPACE` to capture.
7. The face embedding is stored locally.

Press `Q` to cancel enrollment.

## Recognition

Select **Start Recognition**.

The application detects faces from the webcam and compares them with locally enrolled participants.

Press `Q` to stop recognition.

Recognition is limited to participants who have been enrolled in the local database.

## Attendance

A participant can be recorded once per UTC calendar day.

Attendance records are stored in:

```text
data/attendance.db
```

CSV exports are written to:

```text
attendance/attendance.csv
```

These local data directories are excluded from Git.

## Participant Management

The **Manage Participants** window allows enrolled participants to be deleted.

Deleting a participant also removes their stored face embedding and attendance records.

The number shown beside a participant is a display number based on the current participant list. It is not the permanent database ID.

## Testing

Run the test suite from the project root:

```powershell
$env:PYTHONPATH="."
.\.venv\Scripts\pytest -q
```

The test suite covers:

- Face matching
- Cosine similarity
- Unknown-face matching
- Attendance recording
- Attendance history
- CSV export
- Participant deletion

## Project Structure

```text
face-attendance-system/
├── app/
│   ├── attendance/
│   ├── export/
│   ├── storage/
│   ├── ui/
│   ├── vision/
│   ├── enroll.py
│   └── recognize.py
├── models/
│   ├── sface/
│   └── yunet/
├── tests/
├── attendance/
├── data/
├── .gitignore
├── README.md
└── requirements.txt
```

## Dependencies

The main runtime dependencies are pinned in `requirements.txt`:

```text
numpy==2.5.3
opencv-contrib-python==5.0.0.93
pillow==12.3.0
```

`pytest` is used for development and automated testing.

## Limitations

This is a local V1 project intended for educational and small-scale use.

Recognition accuracy can vary with:

- Lighting
- Camera quality
- Face angle
- Distance from the camera
- Changes in appearance

The recognition threshold is project-specific and has not been calibrated as a universal biometric threshold.

## Responsible Use

Use this project only for consent-based face recognition.

Do not use it for covert identification or surveillance.

Participants should understand that face recognition is being used and should provide appropriate consent before enrollment.

## License

This project is for educational and personal development purposes.