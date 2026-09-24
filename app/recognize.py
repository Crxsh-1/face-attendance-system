import cv2

from app.vision.face_engine import FaceEngine
from app.vision.matcher import find_best_match
from app.storage.participants import get_embeddings, get_participant_name


def main():
    engine = FaceEngine()
    candidates = get_embeddings()

    if not candidates:
        print("No enrolled participants found.")
        return

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Recognition started. Press Q to quit.")

    while True:
        ok, frame = camera.read()

        if not ok:
            break

        faces = engine.detect(frame)

        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)

                embedding = engine.embedding(frame, face)
                participant_id, distance = find_best_match(
                    embedding,
                    candidates,
                    threshold=0.363,
                )

                

                name = (
                    get_participant_name(participant_id)
                    if participant_id is not None
                    else None
                )

                label = (
                    f"{name} ({distance:.2f})"
                    if name
                    else f"Unknown ({distance:.2f})"
                )


                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    label,
                    (x, max(25, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

        cv2.imshow("Face Recognition Test", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()