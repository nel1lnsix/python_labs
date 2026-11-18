"""ЛР5, задание A — конвертация JSON <-> CSV."""
import csv
import json
from pathlib import Path


def check_suffix(path: Path, suffix: str) -> None:
    if path.suffix.lower() != suffix:
        raise ValueError(f"{path}: ожидался файл {suffix}")


def json_to_csv(json_path: str, csv_path: str) -> None:
    """
    Преобразует JSON-файл в CSV.
    Поддерживает список словарей [{...}, {...}].
    Кодировка UTF-8. Порядок колонок — ключи первого объекта, потом новые ключи из остальных объектов.
    Отсутствующие поля -> пустые строки.
    """
    src = Path(json_path)
    dst = Path(csv_path)
    check_suffix(src, ".json")
    check_suffix(dst, ".csv")

    with src.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list) or not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"элемент {i} не словарь: {item!r}")

    fieldnames = []
    for item in data:
        for key in item:
            if key not in fieldnames:
                fieldnames.append(key)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(data)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """
    Преобразует CSV в JSON (список словарей).
    Заголовок обязателен, значения сохраняются как строки.
    """
    src = Path(csv_path)
    dst = Path(json_path)
    check_suffix(src, ".csv")
    check_suffix(dst, ".json")

    with src.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        if not reader.fieldnames or any(not name.strip() for name in reader.fieldnames):
            raise ValueError("CSV пустой или без заголовка")
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("Заголовки CSV не должны повторяться")
        rows = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Строка {reader.line_num}: неверное число полей CSV")
            rows.append(row)

    if not rows:
        raise ValueError("CSV не содержит данных, кроме заголовка")

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    json_to_csv("data/lab05/samples/people.json", "data/lab05/out/people_from_json.csv")
    csv_to_json("data/lab05/samples/people.csv", "data/lab05/out/people_from_csv.json")
