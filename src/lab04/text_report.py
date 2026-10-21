"""ЛР4, задание B — отчёт по частотам слов в CSV."""
import argparse
import os
import sys
from pathlib import Path

# чтобы импорт работал при запуске файла напрямую из папки lab04
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.text import normalize, tokenize, count_freq, top_n
from lab04.io_txt_csv import read_text, read_text_auto, write_csv


def find_root(marker: str = ".gitignore") -> Path:
    # поднимаюсь от файла вверх, пока не найду папку проекта
    for folder in Path(__file__).resolve().parents:
        if (folder / marker).exists():
            return folder
    raise FileNotFoundError(f"не найдена папка проекта с {marker}")


ROOT = find_root()
IN_PATH = ROOT / "data" / "lab04" / "input.txt"
OUT_PATH = ROOT / "data" / "lab04" / "report.csv"
TOP_COUNT = 5


def file_freq(path: Path, encoding: str | None) -> dict[str, int]:
    # без --encoding кодировка подбирается функцией read_text_auto
    if encoding:
        text = read_text(path, encoding)
    else:
        text = read_text_auto(path)
    return count_freq(tokenize(normalize(text)))


def print_summary(freq: dict[str, int]) -> None:
    print(f"Всего слов: {sum(freq.values())}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{TOP_COUNT}:")
    for word, count in top_n(freq, TOP_COUNT):
        print(f"{word}:{count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Частоты слов в CSV")
    parser.add_argument("--in", dest="inputs", nargs="+", type=Path, default=[IN_PATH],
                        help="входные файлы")
    parser.add_argument("--out", type=Path, default=OUT_PATH, help="куда писать отчёт")
    parser.add_argument("--encoding", help="кодировка входных файлов")
    parser.add_argument("--per-file", type=Path, help="отчёт по каждому файлу")
    parser.add_argument("--total", type=Path, help="общий отчёт")
    args = parser.parse_args()

    try:
        per_file_rows = []
        total = {}
        for path in args.inputs:
            freq = file_freq(path, args.encoding)
            # top_n с n = len(freq) просто сортирует все слова
            for word, count in top_n(freq, len(freq)):
                per_file_rows.append((path.name, word, count))
                total[word] = total.get(word, 0) + count
    except FileNotFoundError as err1:
        print(f"Файл не найден: {err1.filename}")
        sys.exit(1)
    except ValueError as err2:  # сюда же попадает UnicodeDecodeError
        print(f"Ошибка: {err2}")
        sys.exit(1)
    except LookupError:
        print(f"Неизвестная кодировка: {args.encoding}")
        sys.exit(1)

    total_rows = top_n(total, len(total))
    if args.per_file or args.total:
        if args.per_file:
            write_csv(per_file_rows, args.per_file, header=("file", "word", "count"))
        if args.total:
            write_csv(total_rows, args.total, header=("word", "count"))
    else:
        write_csv(total_rows, args.out, header=("word", "count"))

    print_summary(total)


if __name__ == "__main__":
    main()
