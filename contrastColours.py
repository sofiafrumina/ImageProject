import os
import cv2
from colormath.color_diff import delta_e_cie2000
from colormath.color_objects import LabColor
from colormath.color_conversions import convert_color
import numpy as np


def patch_asscalar(a):
    return a.item()


setattr(np, "asscalar", patch_asscalar)


def compute_average_color(image):
    # Вычисляем средний цвет в прямоугольнике
    average_color = np.mean(image, axis=(0, 1))
    return LabColor(average_color[0], average_color[1], average_color[2])


# Загрузка изображений и вычисление их средних цветов
image_dir = 'images/newPaints'
image_files = os.listdir(image_dir)
image_paths = [os.path.join(image_dir, f) for f in image_files]
images = []
average_colors = []
for image_path in image_paths:
    image = cv2.imread(image_path)
    images.append(image)
    average_color = compute_average_color(image)
    average_colors.append(average_color)


# Функция для поиска наиболее похожих изображений по цвету
def search_similar_images(query_color, average_colors):
    similarities = []
    for color in average_colors:
        similarity = delta_e_cie2000(query_color, color)
        similarities.append(similarity)
    return similarities


def find_photo_for_color(r, g, b):
    rgb = np.array([[[r, g, b]]], dtype=np.uint8)
    hsv_color = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[0][0]

    # Вычисляем комплементарный оттенок
    complementary_hue = (hsv_color[0] + 180) % 360

    # Конвертируем комплементарный оттенок обратно в BGR
    complementary_rgb_color = np.array([[[complementary_hue, hsv_color[1], hsv_color[2]]]], dtype=np.uint8)
    complementary_rgb_color = cv2.cvtColor(complementary_rgb_color, cv2.COLOR_HSV2RGB)[0][0]

    # Конвертируем RGB в Lab
    complementary_lab_color = convert_color(LabColor(complementary_rgb_color[0], complementary_rgb_color[1], complementary_rgb_color[2]), LabColor)

    # Поиск похожих изображений
    similarities = search_similar_images(complementary_lab_color, average_colors)

    # Находим наиболее похожие изображения
    num_similar_images = 5
    similar_image_indices = np.argsort(similarities)[:num_similar_images]

    # Создаем каталог для результатов, если его еще нет
    output_directory = 'images/output_complementary_colour'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Сохраняем найденные изображения
    for idx in similar_image_indices:
        image_filename = os.path.join(output_directory, f'similar_image_{idx}.png')
        cv2.imwrite(image_filename, images[idx])


find_photo_for_color(255, 0, 255)
