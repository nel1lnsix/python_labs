"""ЛР4, задание A — чтение текста и запись CSV."""
import csv
from pathlib import Path
from typing import Iterable, Sequence


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Читает файл целиком и возвращает строку.

    Пустой файл -> "". FileNotFoundError и UnicodeDecodeError пробрасываются.
    Другая кодировка: read_text("data/lab04/input_cp1251.txt", encoding="cp1251")
    """
    return Path(path).read_text(encoding=encoding)


def read_text_auto(path: str | Path,
                   encodings: tuple[str, ...] = ("utf-8-sig", "cp1251")) -> str:
    """Пробует кодировки по очереди и возвращает текст первой подошедшей."""
    data = Path(path).read_bytes()
    last_error = None
    for enc in encodings:
        try:
            return data.decode(enc)
        except UnicodeDecodeError as e:
            last_error = e
    raise ValueError(f"{path}: не подошла ни одна кодировка из {encodings}") from last_error


def ensure_parent_dir(path: str | Path) -> None:
    """Создаёт родительские папки для path, если их нет."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    """Пишет rows в CSV (UTF-8, разделитель запятая).

    rows=[] и header=None => пустой файл; rows=[] и header => только заголовок.
    ValueError, если строки (и заголовок) разной длины.
    """
    rows = list(rows)
    expected = len(header) if header is not None else (len(rows[0]) if rows else 0)
    for i, r in enumerate(rows):
        if len(r) != expected:
            raise ValueError(f"строка {i}: длина {len(r)}, ожидалась {expected}")

    ensure_parent_dir(path)
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        w.writerows(rows)
