"""ЛР7: замеры timeit; большие сортировки запускаются с лимитом."""
import argparse
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import timeit

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

ROOT = Path(__file__).resolve().parents[2]
SORT_TIMEOUT = 60


def measure(fn, nums, *args):
    """Секунды одного вызова без генерации данных и печати."""
    return timeit.timeit(lambda: fn(nums, *args), number=1)


def measure_limited(fn, nums, timeout=SORT_TIMEOUT):
    """Измерить сортировку; остановить отдельный процесс по лимиту."""
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "numbers.json"
        source.write_text(json.dumps(nums), encoding="utf-8")
        command = [sys.executable, "-X", "utf8", "-m", "src.lab07.bench_worker",
                   "--sort", fn.__name__, "--input", str(source)]
        try:
            result = subprocess.run(command, cwd=ROOT, capture_output=True,
                                    text=True, encoding="utf-8", timeout=timeout, check=True)
        except subprocess.TimeoutExpired:
            return f">{timeout:g}s"
        return float(result.stdout.strip())


def measure_search(fn, numbers, queries):
    """Измерить всю серию одинаковых запросов."""
    def search_all():
        for value in queries:
            fn(numbers, value)
    return timeit.timeit(search_all, number=1)


def print_row(row):
    task, n, implementation, seconds = row
    value = f"{seconds:.9f}" if isinstance(seconds, (int, float)) else seconds
    print(f"{task:<20} {n:>8} {implementation:<18} {value}", flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Сравнение времени алгоритмов ЛР7")
    parser.add_argument("--quick", action="store_true", help="Короткий пробный замер")
    parser.add_argument("--output", type=Path, help="Путь для таблицы CSV")
    args = parser.parse_args(argv)
    default_file = "data/lab07/bench_quick.csv" if args.quick else "data/lab07/bench.csv"
    output = args.output if args.output else Path(default_file)
    rng = random.Random(42)
    rows = []
    print(f"{'task':<20} {'n':>8} {'impl':<18} seconds", flush=True)

    sort_sizes = (100, 1000) if args.quick else (1000, 10000, 100000)
    for n in sort_sizes:
        data = [rng.randint(-100000, 100000) for _ in range(n)]
        for fn in (bubble_sort, insertion_sort, selection_sort, sorted):
            if n == 100000 and fn is not sorted:
                seconds = measure_limited(fn, data)
            else:
                seconds = measure(fn, data)
            row = ("sort", n, fn.__name__, seconds)
            rows.append(row)
            print_row(row)

    n = 1000 if args.quick else 100000
    data = [rng.randint(-100000, 100000) for _ in range(n)]
    count = 10 if args.quick else 10000
    queries = [rng.randint(-150000, 150000) for _ in range(count)]
    # Замер подготовки — отдельный эквивалентный вызов sorted.
    # Для самих поисков подготовленный список создаётся вне их замера.
    prep = measure(sorted, data)
    ordered = sorted(data)
    row = ("search_prepare", n, "sorted", prep)
    rows.append(row)
    print_row(row)
    for fn, numbers in ((linear_search, data), (binary_search, ordered)):
        seconds = measure_search(fn, numbers, queries)
        row = (f"search_{count}", n, fn.__name__, seconds)
        rows.append(row)
        print_row(row)

    two_sizes = (100, 1000) if args.quick else (1000, 10000)
    for n in two_sizes:
        data = list(range(1, n - 1))
        rng.shuffle(data)
        data.extend((-1, -2))
        for fn in (two_sum_brute, two_sum_fast):
            row = ("two_sum", n, fn.__name__, measure(fn, data, -3))
            rows.append(row)
            print_row(row)

    write_csv(rows, output, header=("task", "n", "impl", "seconds"))
    print(f"Готово: {output}")


if __name__ == "__main__":
    main()
