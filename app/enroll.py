import cv2

from app.vision.face_engine import FaceEngine
from app.storage.participants import add_participant


def main():
    name = input("Participant name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    print("Enrollment requires the participant's consent.")
    input("Press Enter when ready...")

    engine = FaceEngine()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Look at the camera. Press SPACE to capture or Q to cancel.")

    while True:
        ok, frame = camera.read()

        if not ok:
            break

        faces = engine.detect(frame)

        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Enrollment", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == ord(" ") and faces is not None and len(faces) == 1:
            embedding = engine.embedding(frame, faces[0])
            participant_id = add_participant(name, embedding)
            print(f"Enrollment complete. Participant ID: {participant_id}")
            break

        if key == ord(" ") and (faces is None or len(faces) != 1):
            print("Please make sure exactly one face is visible.")

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()