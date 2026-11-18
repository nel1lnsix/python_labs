"""Простые автоматические проверки ЛР6 через настоящие CLI-команды."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

# test_cases.py находится в src/lab06; parents[2] -- корень python_labs.
ROOT = Path(__file__).resolve().parents[2]


def run(module, *args):
    """Запустить CLI и вернуть код завершения, stdout и stderr."""
    command = [sys.executable, "-X", "utf8", "-m", "src.lab06." + module]
    for arg in args:
        command.append(str(arg))
    return subprocess.run(command, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8")


class CliTests(unittest.TestCase):
    def test_help(self):
        for module in ("cli_text", "cli_convert"):
            result = run(module, "--help")
            self.assertEqual(result.returncode, 0)
            self.assertIn("usage:", result.stdout)
        self.assertEqual(run("cli_convert", "csv2xlsx", "--help").returncode, 0)

    def test_cat(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "текст с пробелами.txt"
            path.write_text("Ёж ёж!\nPython\n\nконец", encoding="utf-8")
            result = run("cli_text", "cat", "--input", path, "-n")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "1: Ёж ёж!\n2: Python\n3: \n4: конец")

            # Проверка переносов Windows без сложной имитации потоков.
            path.write_bytes(b"one\r\ntwo\r\n")
            result = run("cli_text", "cat", "--input", path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "one\ntwo\n")

    def test_stats(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "words.txt"
            path.write_text("Ёж ёж! Python", encoding="utf-8")
            result = run("cli_text", "stats", "--input", path, "--top", 2)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Всего слов: 3", result.stdout)
            self.assertIn("еж:2\npython:1", result.stdout)
            path.write_text("", encoding="utf-8")
            self.assertIn("Всего слов: 0", run("cli_text", "stats", "--input", path).stdout)

    def test_json_csv_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "people.json"
            source.write_text('[{"name": "Анна", "age": 22}]', encoding="utf-8")
            table = folder / "output" / "people.csv"
            result = run("cli_convert", "json2csv", "--in", source, "--out", table)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("name,age", table.read_text(encoding="utf-8"))

            target = folder / "back.json"
            result = run("cli_convert", "csv2json", "--in", table, "--out", target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))[0]["age"], "22")

    def test_csv_xlsx(self):
        from openpyxl import load_workbook
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            table = folder / "people.csv"
            table.write_text("name,age\nАнна,22\n", encoding="utf-8")
            output = folder / "people.xlsx"
            result = run("cli_convert", "csv2xlsx", "--in", table, "--out", output)
            self.assertEqual(result.returncode, 0, result.stderr)
            workbook = load_workbook(output)
            self.assertEqual(workbook.active["A2"].value, "Анна")
            workbook.close()

    def test_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bad_json = folder / "bad.json"
            bad_json.write_text("{broken", encoding="utf-8")
            wrong_suffix = folder / "bad.txt"
            wrong_suffix.write_text("[]", encoding="utf-8")
            invalid_utf8 = folder / "bad-encoding.txt"
            invalid_utf8.write_bytes(b"\xff")
            cases = [
                ("cli_text", "cat", "--input", folder / "missing.txt"),
                ("cli_text", "cat", "--input", invalid_utf8),
                ("cli_text", "stats", "--input", bad_json, "--top", -1),
                ("cli_convert", "json2csv", "--in", bad_json, "--out", folder / "out.csv"),
                ("cli_convert", "json2csv", "--in", wrong_suffix, "--out", folder / "out.csv"),
                ("cli_convert", "json2csv", "--in", bad_json, "--out", bad_json),
            ]
            for case in cases:
                result = run(*case)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("error:", result.stderr)


    def test_bad_csv_does_not_replace_existing_output(self):
        cases = [
            "name,name\nАнна,Борис\n",
            "name,age\nАнна\n",
            "name,age\nАнна,22,extra\n",
        ]
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "bad.csv"
            target = Path(tmp) / "existing.json"
            for text in cases:
                with self.subTest(csv=text):
                    source.write_text(text, encoding="utf-8")
                    target.write_text("OLD", encoding="utf-8")
                    result = run("cli_convert", "csv2json", "--in", source, "--out", target)
                    self.assertEqual(result.returncode, 2, result.stdout)
                    self.assertEqual(target.read_text(encoding="utf-8"), "OLD")

    def test_csv_quotes_and_empty_values_remain_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, target = Path(tmp) / "valid.csv", Path(tmp) / "result.json"
            source.write_text('name,note\n"Анна, Мария",\n', encoding="utf-8")
            result = run("cli_convert", "csv2json", "--in", source, "--out", target)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")),
                             [{"name": "Анна, Мария", "note": ""}])


if __name__ == "__main__":
    unittest.main(verbosity=2)
