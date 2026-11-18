"""Сортировки вручную: новый список, исходный не изменяется."""


def bubble_sort(nums) -> list:
    """Пузырёк, O(n²); ранний выход без обменов."""
    result = list(nums)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for i in range(end):
            if result[i] > result[i + 1]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort(nums) -> list:
    """Вставки, O(n²), O(n) на уже отсортированном списке."""
    result = list(nums)
    for i in range(1, len(result)):
        value = result[i]
        j = i - 1
        while j >= 0 and result[j] > value:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = value
    return result


def selection_sort(nums) -> list:
    """Выбором, O(n²) даже на отсортированном списке."""
    result = list(nums)
    for i in range(len(result) - 1):
        smallest = i
        for j in range(i + 1, len(result)):
            if result[j] < result[smallest]:
                smallest = j
        result[i], result[smallest] = result[smallest], result[i]
    return result
