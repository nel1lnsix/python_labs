"""ЛР6: две команды для чтения UTF-8 текстовых файлов."""
import argparse
from pathlib import Path

from src.lab04.io_txt_csv import read_text
from src.lib.text import normalize, tokenize, count_freq, top_n


def main(argv=None):
    parser = argparse.ArgumentParser(description="Чтение файла и подсчёт слов")
    commands = parser.add_subparsers(dest="command", required=True)

    cat = commands.add_parser("cat", help="Показать содержимое файла")
    cat.add_argument("--input", type=Path, required=True)
    cat.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats = commands.add_parser("stats", help="Посчитать слова")
    stats.add_argument("--input", type=Path, required=True)
    stats.add_argument("--top", type=int, default=5, help="Сколько слов вывести")

    args = parser.parse_args(argv)
    if args.command == "stats" and args.top < 0:
        parser.error("--top не может быть отрицательным")

    try:
        if args.command == "cat":
            # Чтение в текстовом режиме приводит переводы строк к '\n'.
            with args.input.open(encoding="utf-8") as file:
                for number, line in enumerate(file, start=1):
                    if args.n:
                        print(f"{number}: {line}", end="")
                    else:
                        print(line, end="")
        else:
            text = read_text(args.input)
            words = tokenize(normalize(text))
            counts = count_freq(words)
            print(f"Всего слов: {len(words)}")
            print(f"Уникальных слов: {len(counts)}")
            print(f"Топ-{args.top}:")
            for word, count in top_n(counts, args.top):
                print(f"{word}:{count}")
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
