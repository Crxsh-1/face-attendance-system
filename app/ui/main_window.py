import tkinter as tk

from app.recognize import main as start_recognition
from app.attendance.history import get_attendance
from app.export.csv_export import export_attendance
from pathlib import Path
from tkinter import messagebox


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

def run():
    root = tk.Tk()
    root.title("Face Attendance System")
    root.geometry("500x400")

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
        text="Export CSV",
        width=25,
        command=export_csv,
    ).pack(pady=8)

    root.mainloop()


if __name__ == "__main__":
    run()