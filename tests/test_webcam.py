import cv2
from app.vision.face_engine import FaceEngine


engine = FaceEngine()
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("Could not open webcam.")

print("Webcam started. Press Q to quit.")

while True:
    ok, frame = camera.read()
    if not ok:
        break

    faces = engine.detect(frame)

    if faces is not None:
        for face in faces:
            x, y, w, h = face[:4].astype(int)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Detection Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()