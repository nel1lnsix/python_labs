"""ЛР3, задание A — обработка текста: нормализация, токенизация, частоты."""
import re

# слово: буквы/цифры, внутри допускаются дефисы ("по-настоящему", "из-за")
_WORD_RE = re.compile(r"\w+(?:-\w+)*")


def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:

    if not isinstance(text, str):
        raise TypeError(f"text должен быть строкой, дан {type(text).__name__}")

    if casefold:
        text = text.casefold()
    else:
        text = text.lower()
    if yo2e:
        text = text.replace("ё", "е").replace("Ё", "Е")

    text = "".join(ch if ch.isprintable() else " " for ch in text)

    return " ".join(text.split())


def tokenize(text: str) -> list[str]:

    if not isinstance(text, str):
        raise TypeError(f"text должен быть строкой, дан {type(text).__name__}")

    return _WORD_RE.findall(text)


def count_freq(tokens: list[str]) -> dict[str, int]:

    if not isinstance(tokens, (list, tuple)):
        raise TypeError(f"tokens должен быть списком или кортежем, дан {type(tokens).__name__}")

    freq: dict[str, int] = {}
    for token in tokens:
        if not isinstance(token, str):
            raise TypeError(f"каждый токен должен быть строкой, дан {type(token).__name__}")
        freq[token] = freq.get(token, 0) + 1
    return freq


def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:

    if not isinstance(freq, dict):
        raise TypeError(f"freq должен быть словарём, дан {type(freq).__name__}")
    # отсекаю True/False с помощью подкласса int'a - bool
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n должен быть целым числом")
    if n < 0:
        raise ValueError("n не может быть отрицательным")
    return sorted(freq.items(), key=lambda pair: (-pair[1], pair[0]))[:n]


if __name__ == "__main__":
    # Для функции normalize:
    print("\nТесты для функции normalize")

    # -> 'привет мир', 'ежик, елка', 'hello world', 'двойные пробелы', '', TypeError
    test_cases_normalize = ["ПрИвЕт\nМИр\t", "ёжик, Ёлка", "Hello\r\nWorld", "  двойные   пробелы  ", " \n\t ", None]
    for case in test_cases_normalize:
        try:
            print(repr(normalize(case)))
        except TypeError as error:
            print("TypeError:", error)

    # casefold=False -> lower(): 'strasse', 'straße'
    print(repr(normalize("Straße")))
    print(repr(normalize("Straße", casefold=False)))

    # Для функции tokenize:
    print("\nТесты для функции tokenize")

    test_cases_tokenize = ["привет мир", "hello,world!!!", "по-настоящему круто", "2025 год", "emoji 😀 не слово"]
    for case in test_cases_tokenize:
        print(tokenize(case))

    # Для функции count_freq:
    print("\nТесты для функции count_freq")

    test_cases_count_freq = [["a", "b", "a", "c", "b", "a"], ["bb", "aa", "bb", "aa", "cc"], [], "abca", ["a", 1]]
    for case in test_cases_count_freq:
        try:
            print(count_freq(case))
        except TypeError as error:
            print("TypeError:", error)

    # Для функции top_n:
    print("\nТесты для функции top_n")

    test_cases_top_n = [
        ({"a": 3, "b": 2, "c": 1}, 2),
        ({"bb": 2, "aa": 2, "cc": 1}, 2),
        ({}, 5),
        ({"a": 1}, -1),
        ({"a": 1}, True),
        ({"a": 1}, "2"),
    ]
    for freq, n in test_cases_top_n:
        try:
            print(top_n(freq, n))
        except ValueError as err2:
            print("ValueError:", err2)
        except TypeError as error:
            print("TypeError:", error)
