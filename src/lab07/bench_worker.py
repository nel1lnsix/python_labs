"""Один большой замер для bench.py; основной скрипт ограничивает время процесса."""
import argparse
import json
from pathlib import Path
import timeit

from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


def main():
    functions = {"bubble_sort": bubble_sort, "insertion_sort": insertion_sort,
                 "selection_sort": selection_sort}
    parser = argparse.ArgumentParser()
    parser.add_argument("--sort", choices=functions, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    # Чтение файла не входит в замер самой сортировки.
    nums = json.loads(args.input.read_text(encoding="utf-8"))
    fn = functions[args.sort]
    print(timeit.timeit(lambda: fn(nums), number=1))


if __name__ == "__main__":
    main()
