import cv2
import numpy as np
import os

def are_complementary_colors(hue1, hue2):
    # Определяем интервалы комплиментарных оттенков
    complementary_ranges = [(0, 60), (120, 180)]
    
    # Проверяем, находятся ли оттенки в разных интервалах
    for range_start, range_end in complementary_ranges:
        if (hue1 >= range_start and hue1 <= range_end) and (hue2 >= range_start and hue2 <= range_end):
            return True
    return False

def find_dominant_hue(image):
    # Преобразование изображения в оттенки серого
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Вычисление среднего значения оттенков серого
    mean_gray = np.mean(gray_image)
    
    # Возвращаем среднее значение, округленное до ближайшего целого
    return int(mean_gray)

def find_complementary_images(target_image_path, directory_path, num_complementary=5):
    # Загрузка изображения, для которого мы ищем комплиментарные
    target_image = cv2.imread(target_image_path, cv2.IMREAD_UNCHANGED)
    target_alpha_channel = target_image[:, :, 3]
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2BGR)  # Преобразуем в RGB для определения преобладающего оттенка
    target_dominant_hue = find_dominant_hue(target_image)

    # Создаем список для хранения полных путей к комплиментарным изображениям
    complementary_images_paths = []

    # Перебор всех изображений в директории
    for filename in os.listdir(directory_path):
        if filename.endswith(".png") and  filename != os.path.basename(target_image_path):
            image_path = os.path.join(directory_path, filename)
            image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if len(image.shape) == 3 and image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # Преобразуем в RGB для определения преобладающего оттенка
            dominant_hue = find_dominant_hue(image)

            # Проверяем, являются ли преобладающие оттенки комплиментарными
            if are_complementary_colors(target_dominant_hue, dominant_hue):
                complementary_images_paths.append((image_path, dominant_hue))
    
    # Сортируем список комплиментарных изображений по преобладающему оттенку
    complementary_images_paths.sort(key=lambda x: abs(x[1] - target_dominant_hue))

    # Выводим названия комплиментарных изображений (максимум пять)
    print("Complementary images found:")
    for image_path, _ in complementary_images_paths[:num_complementary]:
        print(image_path)

    # Возвращаем список комплиментарных изображений
    return [image_path for image_path, _ in complementary_images_paths[:num_complementary]]

# Путь к изображению, для которого мы ищем комплиментарные
target_image_path = 'images/newPaints/201.png'
# Директория, в которой мы ищем комплиментарные изображения
directory_path = 'images/newPaints'

# Находим комплиментарные изображения
complementary_images = find_complementary_images(target_image_path, directory_path)
