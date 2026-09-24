import csv
from pathlib import Path

from app.attendance.history import get_attendance


def export_attendance(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    records = get_attendance()

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Timestamp"])
        writer.writerows(records)