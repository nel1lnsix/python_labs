"""ЛР3, задание B — статистика по тексту из stdin.

Читает весь ввод до EOF.
Табличный вывод топа (бонус) включается переменной окружения TEXT_STATS_TABLE=1.
$OutputEncoding = [Text.UTF8Encoding]::new() - кодировать в UTF-8 

"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.FuncLib import normalize, tokenize, count_freq, top_n
TOP_COUNT = 5
TABLE_MODE = os.environ.get("TEXT_STATS_TABLE") == "1"


def print_table(top: list[tuple[str, int]]) -> None:
    header = "слово"
    width = max([len(header)] + [len(word) for word, _ in top])
    title = f"{header:<{width}} | частота"
    print(title)
    print("-" * len(title))
    for word, count in top:
        print(f"{word:<{width}} | {count}")


def main() -> None:
    sys.stdin.reconfigure(encoding="utf-8")
    text = sys.stdin.read()

    tokens = tokenize(normalize(text))
    freq = count_freq(tokens)
    top = top_n(freq, TOP_COUNT)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(freq)}")
    print(f"Топ-{TOP_COUNT}:")

    if TABLE_MODE:
        print_table(top)
    else:
        for word, count in top:
            print(f"{word}:{count}")


if __name__ == "__main__":
    main()
