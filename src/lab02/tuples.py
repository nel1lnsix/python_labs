"""ЛР2, задание C — записи."""

def format_record(rec: tuple[str, str, float]) -> str:
    fio, group, gpa = rec # кортеж с данными о user'e
    
    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError('ФИО и группа студента должны быть в строчном виде данных')
    if not (0.0 <= gpa <= 5.0):
        raise ValueError('GPA студента должен быть in range(0.0 - 5.0)')
    
    parts_fio = fio.split()
    parts_fio = [p for p in parts_fio if p]

    if len(parts_fio) < 2:
        raise ValueError('ФИО не может состоять из менее 2-ух слов')
    
    surname = parts_fio[0].capitalize()
    initials = '.'.join(p[0].upper() for p in parts_fio[1:]) + '.' 

    gpa_s = f"{gpa:.2f}"

    return f"{surname} {initials}, гр. {group}, GPA {gpa_s}" 

'''Тест кейсы:'''

#Для функции format_record:
if __name__ == "__main__":

    test_cases = [("Иванов Иван Иванович", "BIVT-25", 4.6), ("Петров Пётр", "IKBO-12", 5.0), 
    ("Петров Пётр Петрович", "IKBO-12", 5.0), ("  сидорова  анна   сергеевна ", "ABB-01", 3.999), ("Курин Вильян Энкорденко", "BIVT-33", 6), ("Димасик", "DSBA-26", 2)] 

    for case in test_cases:
        try:
            print(format_record(case))
        except ValueError as er1:
            print('ValueError:', er1)
        except TypeError as er2:
            print('TypeError:', er2)
