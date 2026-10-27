"""ЛР5, задание B — конвертация CSV -> XLSX."""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

MIN_WIDTH = 8


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
    """
    Конвертирует CSV в XLSX.
    Первая строка CSV — заголовок, лист называется "Sheet1".
    Ширина колонки — по самому длинному значению (не меньше 8 символов).
    """
    src = Path(csv_path)
    dst = Path(xlsx_path)
    if src.suffix.lower() != ".csv":
        raise ValueError(f"{src}: ожидался файл .csv")
    if dst.suffix.lower() != ".xlsx":
        raise ValueError(f"{dst}: ожидался файл .xlsx")

    with src.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    if not rows or not any(rows[0]):
        raise ValueError("CSV пустой или без заголовка")

    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    widths = {}  # номер колонки -> длина самого длинного значения
    for row in rows:
        ws.append(row)
        for col, value in enumerate(row, start=1):
            widths[col] = max(widths.get(col, 0), len(value))

    for col, width in widths.items():
        ws.column_dimensions[get_column_letter(col)].width = max(width + 2, MIN_WIDTH)

    dst.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dst)


if __name__ == "__main__":
    csv_to_xlsx("data/lab05/samples/people.csv", "data/lab05/out/people.xlsx")
    csv_to_xlsx("data/lab05/samples/cities.csv", "data/lab05/out/cities.xlsx")
