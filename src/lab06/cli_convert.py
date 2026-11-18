"""ЛР6: вызов уже готовых конвертеров из ЛР5."""
import argparse
import csv
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Конвертация JSON, CSV и XLSX")
    commands = parser.add_subparsers(dest="command", required=True)

    json2csv = commands.add_parser("json2csv", help="JSON в CSV")
    json2csv.add_argument("--in", dest="input", required=True)
    json2csv.add_argument("--out", dest="output", required=True)

    csv2json = commands.add_parser("csv2json", help="CSV в JSON")
    csv2json.add_argument("--in", dest="input", required=True)
    csv2json.add_argument("--out", dest="output", required=True)

    csv2xlsx = commands.add_parser("csv2xlsx", help="CSV в XLSX")
    csv2xlsx.add_argument("--in", dest="input", required=True)
    csv2xlsx.add_argument("--out", dest="output", required=True)

    args = parser.parse_args(argv)

    # Нельзя случайно записывать поверх входного файла.
    if Path(args.input).resolve() == Path(args.output).resolve():
        parser.error("входной и выходной файлы должны различаться")

    try:
        # Импортируем только модуль выбранной команды.
        # Поэтому другие команды и --help не зависят от openpyxl.
        if args.command == "json2csv":
            from src.lab05.json_csv import json_to_csv
            json_to_csv(args.input, args.output)
        elif args.command == "csv2json":
            from src.lab05.json_csv import csv_to_json
            csv_to_json(args.input, args.output)
        else:
            from src.lab05.csv_xlsx import csv_to_xlsx
            csv_to_xlsx(args.input, args.output)
    except ImportError as error:
        parser.error(f"Ошибка импорта: {error}. Проверьте requirements.txt")
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        parser.error(str(error))

    print(f"Готово: {args.output}")


if __name__ == "__main__":
    main()
