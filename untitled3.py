num =str(153)
sum = 0
for i in num:
    sum += int(i)**len(num)

if sum == int(num):
    print("true")
else:
    print("false")