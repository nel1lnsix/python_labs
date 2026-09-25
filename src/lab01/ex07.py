s = input()

# 1) первая заглавная буква — начало исходной строки
start = 0
while not s[start].isupper():
    start += 1

# 2) второй символ стоит сразу после первой цифры (ищем её после заглавной)
digit = start + 1
while not s[digit].isdigit():
    digit += 1
step = digit + 1 - start

# 3) берём символы с этим шагом, пока не дойдём до точки
result = ""
for i in range(start, len(s), step):
    result += s[i]
    if s[i] == ".":
        break
print(result)
