n = int(input())
full_time = 0
part_time = 0
for _ in range(n):
    surname, name, age, is_full_time = input().split()
    if is_full_time == "True":
        full_time += 1
    else:
        part_time += 1
print(full_time, part_time)
