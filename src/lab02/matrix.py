"""ЛР2, задание B — матрицы (списки списков)."""


def _check_rectangular(mat: list[list[float | int]]) -> int:
    """Проверяет, что все строки одной длины, и возвращает эту длину."""
    row_length = len(mat[0])
    for row in mat:
        if len(row) != row_length:
            raise ValueError("матрица рваная — строки должны быть одинаковой длины")
    return row_length


def transpose(mat: list[list[float | int]]) -> list[list]:

    if not mat:
        return []

    row_length = _check_rectangular(mat)

    result = []
    for col_idx in range(row_length):
        new_row = []
        for row in mat:
            new_row.append(row[col_idx])
        result.append(new_row)

    return result


def row_sums(mat: list[list[float | int]]) -> list[float]:
    
    if not mat:
        return []

    _check_rectangular(mat)

    return [sum(row) for row in mat]


def col_sums(mat: list[list[float | int]]) -> list[float]:
    
    if not mat:
        return []

    row_length = _check_rectangular(mat)

    result = []
    for col_idx in range(row_length):
        col_sum = 0
        for row in mat:
            col_sum += row[col_idx]
        result.append(col_sum)

    return result

'''Тест кейсы:'''
if __name__ == "__main__":

    #Для функции transpose:
    print('\nТесты для функции transpose:')

    test_Cases_transpose = [[[1, 2, 3]], [[1], [2], [3]], [[1, 2], [3, 4]], [], [[1, 2], [3]]]
    for case in test_Cases_transpose:
        try:
            print(transpose(case))
        except ValueError as error:
            print("ValueError:", error)

    ##Для функции row_sums:
    print("\nТесты для функции row_sums:")

    test_Cases_row_sums = [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]], [[1, 2], [3]]]
    for case in test_Cases_row_sums:
        try:
            print(row_sums(case))
        except ValueError as error:
            print("ValueError:", error)
                

    ##Для функции col_sums:
    print("\nТесты для функции col_sums:")

    test_Cases_col_sums = [[[1, 2, 3], [4, 5, 6]], [[-1, 1], [10, -10]], [[0, 0], [0, 0]], [[1, 2], [3]]]
    for case in test_Cases_col_sums:
        try:
            print(col_sums(case))
        except ValueError as error:
            print("ValueError:", error)
    