import cv2
from tkinter import messagebox

from app.vision.face_engine import FaceEngine
from app.storage.participants import add_participant


def main():
    name = input("Participant name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    print()
    print("Privacy notice:")
    print("- Face data is stored locally on this computer.")
    print("- Face data is not uploaded to a cloud service.")
    print("- Enrollment should only happen with the participant's consent.")
    print()

    consent = input("Has the participant given consent? (yes/no): ").strip().lower()

    if consent != "yes":
        print("Enrollment cancelled because consent was not confirmed.")
        return

    input("Press Enter when ready...")

    engine = FaceEngine()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Look at the camera.")
    print("Press SPACE to capture or Q to cancel.")

    faces = None

    while True:
        ok, frame = camera.read()

        if not ok:
            break

        faces = engine.detect(frame)

        if faces is not None:
            for face in faces:
                x, y, w, h = face[:4].astype(int)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2,
                )

        cv2.putText(
            frame,
            "SPACE: capture   Q: cancel",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Enrollment", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        if key == ord(" ") and faces is not None and len(faces) == 1:
            embedding = engine.embedding(frame, faces[0])

            participant_id = add_participant(
                name,
                embedding,
            )

            print(
                f"Enrollment complete. Participant ID: {participant_id}"
            )

            messagebox.showinfo(
                "Enrollment Complete",
                f"{name} was enrolled successfully.\n\n"
                "The face data is stored locally.",
            )

            break

        if key == ord(" ") and (faces is None or len(faces) != 1):
            print("Please make sure exactly one face is visible.")

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()