fio = input("ФИО: ")
# split() без аргументов убирает все лишние пробелы
parts = fio.split()
initials = "".join(part[0].upper() for part in parts)
clean = " ".join(parts)
print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(clean)}")
