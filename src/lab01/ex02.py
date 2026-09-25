# заменяем запятую на точку, чтобы float() понял число
a = float(input("a: ").replace(",", "."))
b = float(input("b: ").replace(",", "."))
total = a + b
avg = total / 2
print(f"sum={total:.2f}; avg={avg:.2f}")
