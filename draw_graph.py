import math
import random
import matplotlib.pyplot as plt

N = 50
angles = [math.atan(1 / 2 ** j) for j in range(N)]

def cordic(X, Y, k):
    x, y = X, Y
    res_angle = 0

    for i in range(k):
        t = 2 ** i
        if y > 0:
            res_angle += angles[i]
            x, y = x + y / t, - x / t + y
        else:
            res_angle -= angles[i]
            x, y = x - y / t, x / t + y

    return abs(res_angle - math.atan2(Y, X))

T = 1000
max_k = 30

average_errors = []

for k in range(1, max_k + 1):
    total_error = 0.0
    for _ in range(T):
        x, y = random.random(), random.random()
        total_error += cordic(x, y, k)
    
    average_error = total_error / T
    average_errors.append(average_error)
    print(f"k = {k}, Средняя ошибка = {average_error}")

plt.figure(figsize=(10, 6))
plt.plot(range(1, max_k + 1), average_errors, marker='o', linestyle='-')
plt.xlabel('Количество итераций (k)')
plt.ylabel('Средняя ошибка')
plt.title('Зависимость средней ошибки CORDIC от количества итераций')
plt.grid(True)
plt.yscale('log')

plt.savefig('cordic_error_vs_iterations.png', dpi=300, bbox_inches='tight')
plt.show()