"""Базовые алгоритмы поиска и Two Sum."""


def linear_search(nums, x) -> int:
    """Индекс первого вхождения x или -1. Время O(n)."""
    for index, value in enumerate(nums):
        if value == x:
            return index
    return -1


def binary_search(sorted_nums, x) -> int:
    """Индекс любого вхождения x или -1 за O(log n).

    Список должен быть отсортирован по возрастанию.
    На неотсортированном списке результат не определён.
    """
    lo, hi = 0, len(sorted_nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if sorted_nums[mid] == x:
            return mid
        if sorted_nums[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def two_sum_brute(nums, target) -> tuple[int, int] | None:
    """Пара (i, j), i < j, с нужной суммой или None. O(n²)."""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j
    return None


def two_sum_fast(nums, target) -> tuple[int, int] | None:
    """Та же задача за ожидаемое O(n) времени и O(n) памяти."""
    seen = {}
    for j, value in enumerate(nums):
        complement = target - value
        if complement in seen:
            return seen[complement], j
        seen[value] = j
    return None
