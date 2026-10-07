"""ЛР2, задание A — операции над списками."""


def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:

    if not nums:
        raise ValueError("список не может быть пуст")

    min_val = max_val = nums[0]
    for num in nums[1:]:
        if num < min_val:
            min_val = num
        if num > max_val:
            max_val = num

    return (min_val, max_val)


def unique_sorted(nums: list[float | int]) -> list[float | int]:

    if not nums:
        return []

    unique = []
    for num in nums:
        if num not in unique:
            unique.append(num)

    for i in range(len(unique)):
        for j in range(i + 1, len(unique)):
            if unique[i] > unique[j]:
                unique[i], unique[j] = unique[j], unique[i]

    return unique


def flatten(mat: list[list | tuple]) -> list:

    result = []
    for row in mat:
        if not isinstance(row, (list, tuple)):
            raise TypeError(f"каждый элемент матрицы должен быть списком или кортежем, дан {type(row).__name__}")
        result.extend(row)
    return result

'''Тест кейсы:'''
if __name__ == "__main__":

    ## Для функции min_max:
    print('\nТесты для функции min_max')

    print(min_max([3, -1, 5, 5, 0])) # -> (-1, 5)    
    print(min_max([42])) # -> (42, 42)        
    print(min_max([-5, -2, -9])) # -> (-9, -2)  
    print(min_max([1.5, 2, 2.0, -3.1])) # -> (-3.1, 2)
            
    #Для функции unique_sorted:
    print('\nТесты для функции unique_sorted')

    print(unique_sorted([3, 1, 2, 1, 3])) # -> [1, 2, 3]  
    print(unique_sorted([])) # -> []     
    print(unique_sorted([-1, -1, 0, 2, 2])) # -> [-1, 0, 2]
    print(unique_sorted([1.0, 1, 2.5, 2.5, 0])) # -> [0, 1.0, 2.5]

    #Для функции flatten:
    print('\nТесты для функции flatten')

    test_cases_flatten = [[[1, 2], [3,4]], [[1,2], (3, 4, 5)], [[1], [], [2,3]], [[1, 2], "ab"]]
    for test in test_cases_flatten:
        try:
            print(flatten(test))
        except TypeError as error:
            print("TypeError:", error)