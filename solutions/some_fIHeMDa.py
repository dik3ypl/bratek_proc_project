def addd(num, num2):
    return num + num2

data = input()
x, y = data.split(',')
x = int(x)
y = int(y)

print(addd(x, y))