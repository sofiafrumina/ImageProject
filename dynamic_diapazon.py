from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt

# Путь к папке с измененными изображениями
folder_path = "images/dynamic_images"

# Создаем список для хранения усредненных значений яркости
mean_brightness_values = []

# Проходим по всем изображениям в папке
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        # Открываем изображение
        img = Image.open(os.path.join(folder_path, filename))

        # Преобразуем изображение в массив NumPy и нормализуем значения пикселей
        pixel_values = np.array(img) / 255.0

        # Усредняем значения яркости пикселей
        mean_brightness = np.mean(pixel_values)

        # Берем логарифм от усредненной яркости, добавляя небольшое значение, чтобы избежать логарифма от нуля
        mean_brightness_log = np.log(mean_brightness + 1)

        # Добавляем усредненное значение в список
        mean_brightness_values.append(mean_brightness_log)

# Преобразуем список усредненных значений в массив NumPy
mean_brightness_array = np.array(np.sort(mean_brightness_values))
print(mean_brightness_array)

# Создаем список для хранения значений EV
ev_values = [-4.0, -3.9, -3.8, -3.5, -3.4, -3.1, -2.9, -2.7, -2.4, -2.1,
             -1.8, -1.4, -0.7, 0.0, 0.9, 1.5, 2.3, 3.0, 3.4, 3.8]

# Преобразуем список значений EV в массив NumPy
ev_array = np.array(ev_values)

# Визуализируем кривую
plt.plot(ev_array, mean_brightness_array, marker='o', linestyle='-')
plt.xlabel("Значение экспозиции (EV)")
plt.ylabel("Логарифм средней яркости")
plt.title("Кривая динамического диапазона")
plt.grid(True)
plt.show()
