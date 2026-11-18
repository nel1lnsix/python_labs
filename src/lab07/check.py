"""ЛР7: проверяем алгоритмы на крайних и случайных примерах."""
import random

from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

SORT_EDGES = [[], [1], [2, 1], [1, 2], [2, 2], [-1, 0, -1], list(range(10)), list(range(9, -1, -1))]
SEARCH_EDGES = [[], [1], [1, 2], [2, 1], [2, 2], [-3, 0, 5]]
PAIR_EDGES = [([], 0), ([1], 2), ([3, 3], 6), ([0, 0], 0), ([-3, 2, 7], 4), ([1, 2], 10), ([1, 2, 3, 4], 5)]


def random_lists(seed, count):
    """Воспроизводимые списки длиной 0..50, значения -100..100."""
    rng = random.Random(seed)
    cases = []
    for _ in range(count):
        size = rng.randint(0, 50)
        cases.append([rng.randint(-100, 100) for _ in range(size)])
    return cases


def pair_exists(nums, target):
    """Независимая проверка существования хотя бы одной пары."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return True
    return False


def check_sorting(fn, trials=100) -> None:
    """Сравнить сортировку с эталоном и проверить сохранность входа."""
    for sample in SORT_EDGES + random_lists(42, trials):
        nums = sample.copy()
        original = nums.copy()
        result = fn(nums)
        expected = sorted(original)
        assert result == expected, (fn.__name__, "результат", original, result, expected)
        assert nums == original, (fn.__name__, "изменён вход", original, nums)
        assert result is not nums, (fn.__name__, "нужен новый список", original)


def check_search() -> None:
    """Линейный — первое вхождение; бинарный — любое в отсортированном."""
    for sample in SEARCH_EDGES + random_lists(43, 100):
        nums = sample.copy()
        ordered = sorted(nums)
        queries = [-101, 0, 101]
        if ordered:
            queries.extend((ordered[0], ordered[-1]))
        for value in queries:
            expected = nums.index(value) if value in nums else -1
            actual = linear_search(nums, value)
            assert actual == expected, ("linear_search", nums, value, actual, expected)
            index = binary_search(ordered, value)
            if value in ordered:
                assert isinstance(index, int) and 0 <= index < len(ordered), (
                    "binary_search", ordered, value, index)
                assert ordered[index] == value, ("binary_search", ordered, value, index)
            else:
                assert index == -1, ("binary_search", ordered, value, index, -1)


def check_two_sum(trials=100) -> None:
    """Проверить существование решения и каждую пару, не равенство пар."""
    rng = random.Random(44)
    pair_cases = PAIR_EDGES.copy()
    for nums in random_lists(44, trials):
        pair_cases.append((nums, rng.randint(-200, 200)))
    for sample, target in pair_cases:
        nums = sample.copy()
        original = nums.copy()
        expected = pair_exists(nums, target)
        for fn in (two_sum_brute, two_sum_fast):
            pair = fn(nums, target)
            if not expected:
                assert pair is None, (fn.__name__, nums, target, pair, "ожидалось None")
            else:
                assert isinstance(pair, tuple) and len(pair) == 2, (
                    fn.__name__, nums, target, pair, "ожидалась пара индексов")
                i, j = pair
                assert isinstance(i, int) and isinstance(j, int), (fn.__name__, nums, target, pair)
                assert 0 <= i < j < len(nums), (fn.__name__, nums, target, pair, "неверные индексы")
                assert nums[i] + nums[j] == target, (fn.__name__, nums, target, pair, "неверная сумма")
            assert nums == original, (fn.__name__, "изменён вход", original, nums, target)


def main():
    trials = 100
    for fn in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn, trials)
    check_search()
    check_two_sum(trials)
    sort_count = 3 * (len(SORT_EDGES) + trials)
    search_count = len(SEARCH_EDGES) + 100
    pair_count = len(PAIR_EDGES) + trials
    total = sort_count + search_count + pair_count
    print(f"OK: {total} наборов ({sort_count} сортировки, "
          f"{search_count} поиска, {pair_count} Two Sum)")


if __name__ == "__main__":
    main()
