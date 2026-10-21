"""ЛР3, задание B — статистика по тексту из stdin.

Запуск:
    python text_stats.py          # обычный вывод
    python text_stats.py --table  # топ-слов в виде таблицы (бонус)
"""
import os
import sys

# чтобы импорт lib работал при запуске файла напрямую из папки lab03
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.text import normalize, tokenize, count_freq, top_n

TOP_COUNT = 5


def print_table(top: list[tuple[str, int]]) -> None:
    header = "слово"
    width = max([len(header)] + [len(word) for word, _ in top])
    print(f"{header:<{width}} | частота")
    print("-" * width + "-+-" + "-" * len("частота"))
    for word, count in top:
        print(f"{word:<{width}} | {count}")


def main() -> None:
    text = sys.stdin.read()

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, TOP_COUNT)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{TOP_COUNT}:")

    if "--table" in sys.argv[1:]:
        print_table(top)
    else:
        for word, count in top:
            print(f"{word}:{count}")


if __name__ == "__main__":
    main()
