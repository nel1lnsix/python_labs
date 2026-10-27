"""ЛР5 — проверка конвертаций и ошибок.

Запуск из корня репозитория: python src/lab05/test_cases.py
"""
import csv
import json

from openpyxl import load_workbook

from csv_xlsx import csv_to_xlsx
from json_csv import csv_to_json, json_to_csv

SAMPLES = "data/lab05/samples/"
ERRORS = "data/lab05/samples/errors/"
OUT = "data/lab05/out/"


def check(name, func, src, dst):
    # запускаю конвертацию и печатаю, какая ошибка вылетела
    try:
        func(src, dst)
        print(name, "-> OK")
    except (ValueError, FileNotFoundError) as e:
        print(name, "->", type(e).__name__, e)


print("1. JSON -> CSV")
json_to_csv(SAMPLES + "people.json", OUT + "people_from_json.csv")

with open(SAMPLES + "people.json", encoding="utf-8") as f:
    people = json.load(f)
with open(OUT + "people_from_json.csv", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
print("заголовок:", reader.fieldnames)
print("записей было:", len(people), "стало:", len(rows))

print()
print("2. CSV -> JSON")
csv_to_json(SAMPLES + "people.csv", OUT + "people_from_csv.json")

with open(SAMPLES + "people.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
with open(OUT + "people_from_csv.json", encoding="utf-8") as f:
    people = json.load(f)
print("ключи:", list(people[0].keys()))
print("записей было:", len(rows), "стало:", len(people))

print()
print("3. CSV -> XLSX")
csv_to_xlsx(SAMPLES + "people.csv", OUT + "people.xlsx")
csv_to_xlsx(SAMPLES + "cities.csv", OUT + "cities.xlsx")

for name in ["people.xlsx", "cities.xlsx"]:
    ws = load_workbook(OUT + name).active
    print(name, "лист:", ws.title, "строк:", ws.max_row)
    print("ширина A, B, C:",
          ws.column_dimensions["A"].width,
          ws.column_dimensions["B"].width,
          ws.column_dimensions["C"].width)

print()
print("4. Ошибки")
check("пустой файл JSON", json_to_csv, ERRORS + "empty.json", OUT + "error.csv")
check("JSON = []", json_to_csv, ERRORS + "empty_list.json", OUT + "error.csv")
check("объект вместо списка", json_to_csv, ERRORS + "object.json", OUT + "error.csv")
check("в списке не словарь", json_to_csv, ERRORS + "not_dicts.json", OUT + "error.csv")
check("нет JSON-файла", json_to_csv, ERRORS + "nope.json", OUT + "error.csv")
check("CSV вместо JSON", json_to_csv, SAMPLES + "people.csv", OUT + "error.csv")
check("пустой CSV", csv_to_json, ERRORS + "empty.csv", OUT + "error.json")
check("CSV только с заголовком", csv_to_json, ERRORS + "only_header.csv", OUT + "error.json")
check("CSV без заголовка", csv_to_json, ERRORS + "no_header.csv", OUT + "error.json")
check("нет CSV-файла", csv_to_json, ERRORS + "nope.csv", OUT + "error.json")
check("пустой CSV -> XLSX", csv_to_xlsx, ERRORS + "empty.csv", OUT + "error.xlsx")
check("выход .xls, а не .xlsx", csv_to_xlsx, SAMPLES + "people.csv", OUT + "error.xls")
