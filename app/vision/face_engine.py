import cv2
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

YUNET_MODEL = BASE_DIR / "models" / "yunet" / "face_detection_yunet_2023mar.onnx"
SFACE_MODEL = BASE_DIR / "models" / "sface" / "face_recognition_sface_2021dec_int8.onnx"


class FaceEngine:
    def __init__(self):
        self.detector = cv2.FaceDetectorYN.create(
            str(YUNET_MODEL),
            "",
            (320, 320),
            0.9,
            0.3,
            500,
        )

        self.recognizer = cv2.FaceRecognizerSF.create(
            str(SFACE_MODEL),
            "",
        )

    def detect(self, frame: np.ndarray):
        height, width = frame.shape[:2]
        self.detector.setInputSize((width, height))
        _, faces = self.detector.detect(frame)
        return faces

    def embedding(self, frame: np.ndarray, face):
        aligned = self.recognizer.alignCrop(frame, face)
        feature = self.recognizer.feature(aligned)
        return feature.flatten().astype(np.float32)