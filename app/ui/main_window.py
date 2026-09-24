import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from app.recognize import main as start_recognition
from app.enroll import main as start_enrollment
from app.attendance.history import get_attendance
from app.export.csv_export import export_attendance
from app.storage.participants import get_participants, delete_participant


def show_history():
    records = get_attendance()

    window = tk.Toplevel()
    window.title("Attendance History")
    window.geometry("600x400")

    if not records:
        tk.Label(
            window,
            text="No attendance records yet.",
        ).pack(pady=30)
        return

    for name, timestamp in records:
        tk.Label(
            window,
            text=f"{name} — {timestamp}",
            anchor="w",
        ).pack(fill="x", padx=20, pady=3)


def export_csv():
    output = Path("attendance") / "attendance.csv"
    export_attendance(output)

    messagebox.showinfo(
        "Export Complete",
        f"Attendance exported to:\n{output}",
    )


def manage_participants():
    window = tk.Toplevel()
    window.title("Participants")
    window.geometry("500x400")

    list_frame = tk.Frame(window)
    list_frame.pack(fill="both", expand=True)

    def refresh():
        for widget in list_frame.winfo_children():
            widget.destroy()

        records = get_participants()

        if not records:
            tk.Label(
                list_frame,
                text="No enrolled participants.",
            ).pack(pady=20)
            return

        for participant_id, name in records:
            row = tk.Frame(list_frame)
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(
                row,
                text=f"{participant_id}: {name}",
            ).pack(side="left")

            tk.Button(
                row,
                text="Delete",
                command=lambda pid=participant_id: delete_selected(pid),
            ).pack(side="right")

    def delete_selected(participant_id):
        confirmed = messagebox.askyesno(
            "Delete Participant",
            "Delete this participant and their attendance records?",
            parent=window,
        )

        if confirmed:
            delete_participant(participant_id)
            refresh()

    refresh()


def run():
    root = tk.Tk()
    root.title("Face Attendance System")
    root.geometry("500x450")

    title = tk.Label(
        root,
        text="Face Attendance System",
        font=("Arial", 20, "bold"),
    )
    title.pack(pady=30)

    tk.Button(
        root,
        text="Enroll Participant",
        width=25,
        command=start_enrollment,
    ).pack(pady=8)

    tk.Button(
        root,
        text="Start Recognition",
        width=25,
        command=start_recognition,
    ).pack(pady=8)

    tk.Button(
        root,
        text="Attendance History",
        width=25,
        command=show_history,
    ).pack(pady=8)

    tk.Button(
        root,
        text="Manage Participants",
        width=25,
        command=manage_participants,
    ).pack(pady=8)

    tk.Button(
        root,
        text="Export CSV",
        width=25,
        command=export_csv,
    ).pack(pady=8)

    root.mainloop()


if __name__ == "__main__":
    run()