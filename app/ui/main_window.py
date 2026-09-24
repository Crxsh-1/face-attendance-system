import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from app.attendance.history import get_attendance
from app.enroll import main as start_enrollment
from app.export.csv_export import export_attendance
from app.recognize import main as start_recognition
from app.storage.participants import (
    delete_participant,
    get_participants,
)


def show_history(parent):
    records = get_attendance()

    window = tk.Toplevel(parent)
    window.title("Attendance History")
    window.geometry("650x450")
    window.resizable(True, True)

    frame = ttk.Frame(window, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Attendance History",
        font=("Arial", 16, "bold"),
    ).pack(anchor="w", pady=(0, 15))

    if not records:
        ttk.Label(
            frame,
            text="No attendance records yet.",
        ).pack(anchor="w")
        return

    tree = ttk.Treeview(
        frame,
        columns=("name", "timestamp"),
        show="headings",
    )

    tree.heading("name", text="Name")
    tree.heading("timestamp", text="Timestamp")

    tree.column("name", width=200)
    tree.column("timestamp", width=380)

    for name, timestamp in records:
        tree.insert("", "end", values=(name, timestamp))

    tree.pack(fill="both", expand=True)


def export_csv(parent):
    try:
        output = Path("attendance") / "attendance.csv"
        export_attendance(output)

        messagebox.showinfo(
            "Export Complete",
            f"Attendance exported to:\n{output}",
            parent=parent,
        )

    except Exception as error:
        messagebox.showerror(
            "Export Error",
            f"Could not export attendance:\n{error}",
            parent=parent,
        )


def manage_participants(parent):
    window = tk.Toplevel(parent)
    window.title("Participants")
    window.geometry("550x450")
    window.resizable(True, True)

    frame = ttk.Frame(window, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Manage Participants",
        font=("Arial", 16, "bold"),
    ).pack(anchor="w", pady=(0, 15))

    list_frame = ttk.Frame(frame)
    list_frame.pack(fill="both", expand=True)

    def refresh():
        for widget in list_frame.winfo_children():
            widget.destroy()

        records = get_participants()

        if not records:
            ttk.Label(
                list_frame,
                text="No enrolled participants.",
            ).pack(pady=20)
            return

        for participant_id, name in records:
            row = ttk.Frame(list_frame)
            row.pack(fill="x", pady=5)

            ttk.Label(
                row,
                text=f"{participant_id}: {name}",
            ).pack(side="left")

            ttk.Button(
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

        if not confirmed:
            return

        try:
            deleted = delete_participant(participant_id)

            if deleted:
                messagebox.showinfo(
                    "Participant Deleted",
                    "The participant and their attendance records were deleted.",
                    parent=window,
                )
                refresh()
            else:
                messagebox.showwarning(
                    "Not Found",
                    "The participant could not be found.",
                    parent=window,
                )

        except Exception as error:
            messagebox.showerror(
                "Delete Error",
                f"Could not delete participant:\n{error}",
                parent=window,
            )

    refresh()


def safe_action(parent, action, title):
    try:
        action()
    except Exception as error:
        messagebox.showerror(
            title,
            str(error),
            parent=parent,
        )


def run():
    root = tk.Tk()
    root.title("Face Attendance System")
    root.geometry("520x500")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=30)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Face Attendance System",
        font=("Arial", 20, "bold"),
    ).pack(pady=(10, 10))

    ttk.Label(
        frame,
        text="Local attendance management",
    ).pack(pady=(0, 25))

    ttk.Button(
        frame,
        text="Enroll Participant",
        command=lambda: safe_action(
            root,
            start_enrollment,
            "Enrollment Error",
        ),
    ).pack(fill="x", pady=6)

    ttk.Button(
        frame,
        text="Start Recognition",
        command=lambda: safe_action(
            root,
            start_recognition,
            "Recognition Error",
        ),
    ).pack(fill="x", pady=6)

    ttk.Button(
        frame,
        text="Attendance History",
        command=lambda: show_history(root),
    ).pack(fill="x", pady=6)

    ttk.Button(
        frame,
        text="Manage Participants",
        command=lambda: manage_participants(root),
    ).pack(fill="x", pady=6)

    ttk.Button(
        frame,
        text="Export CSV",
        command=lambda: export_csv(root),
    ).pack(fill="x", pady=6)

    ttk.Separator(frame).pack(fill="x", pady=20)

    ttk.Label(
        frame,
        text="Face data is stored locally on this computer.",
    ).pack()

    ttk.Label(
        frame,
        text="Use only with participant consent.",
    ).pack(pady=(4, 0))

    root.mainloop()


if __name__ == "__main__":
    run()