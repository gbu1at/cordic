import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter  # Добавлено для сохранения GIF

N = 50
angles = [math.atan(1 / 2 ** j) for j in range(N)]

def cordic_steps(X, Y, max_iter):
    x, y = X, Y
    res_angle = 0
    steps = []
    
    for i in range(max_iter):
        t = 2 ** i
        if y > 0:
            res_angle += angles[i]
            x, y = x + y / t, -x / t + y
        else:
            res_angle -= angles[i]
            x, y = x - y / t, x / t + y
        
        true_angle = math.atan2(Y, X)
        error = abs(res_angle - true_angle)
        steps.append((i+1, res_angle, true_angle, error, x, y))
    
    return steps

print("Введите координаты вектора (x, y):")
x = float(input("x = "))
y = float(input("y = "))
max_iter = int(input("Максимальное число итераций: "))

steps = cordic_steps(x, y, max_iter)
true_angle = math.atan2(y, x)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle(f'Анимация алгоритма CORDIC для вектора ({x}, {y})')

ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.grid(True)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')

ax2.set_xlim(0, max_iter+1)
ax2.set_ylim(0, math.pi/2)
ax2.set_title('Изменение угла и ошибки')
ax2.set_xlabel('Итерация')
ax2.set_ylabel('Угол (рад)')
ax2.grid(True)

vector_line, = ax1.plot([0, x], [0, y], 'r-', lw=2)
current_vector_line, = ax1.plot([0, x], [0, y], 'b--', lw=1)
angle_line, = ax2.plot([], [], 'g-', label='Вычисленный угол')
true_line = ax2.axhline(true_angle, color='r', linestyle='--', label='Истинный угол')
error_line, = ax2.plot([], [], 'b-', label='Ошибка')
info_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.8))

ax2.legend()

def init():
    angle_line.set_data([], [])
    error_line.set_data([], [])
    info_text.set_text('')
    return vector_line, current_vector_line, angle_line, error_line, info_text

def update(frame):
    iteration, current_angle, true_angle, error, current_x, current_y = steps[frame]
    
    current_vector_line.set_data([0, current_x], [0, current_y])
    
    x_data = list(range(1, iteration+1))
    angles_data = [s[1] for s in steps[:iteration]]
    errors_data = [s[3] for s in steps[:iteration]]
    
    angle_line.set_data(x_data, angles_data)
    error_line.set_data(x_data, errors_data)
    
    info_text.set_text(
        f'Итерация: {iteration}\n'
        f'Текущий угол: {current_angle:.6f} рад\n'
        f'Истинный угол: {true_angle:.6f} рад\n'
        f'Ошибка: {error:.6f} рад\n'
    )
    
    return vector_line, current_vector_line, angle_line, error_line, info_text

ani = FuncAnimation(fig, update, frames=len(steps),
                    init_func=init, blit=True, interval=500, repeat=False)

plt.tight_layout()

writer = PillowWriter(fps=1) 
ani.save("cordic_animation.gif", writer=writer)  # Сохраняем GIF

plt.show()