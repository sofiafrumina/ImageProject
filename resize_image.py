import cv2
import os
import numpy as np

def resize_images(input_folder, output_folder, target_width=200, target_height=300):
    # Создаем выходную папку, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список файлов во входной папке
    image_files = os.listdir(input_folder)

    for image_file in image_files:
        # Считываем изображение
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Получаем текущие размеры изображения
        height, width, _ = image.shape

        # Создаем новое изображение с белым фоном заданного размера
        if width != target_width or height != target_height:
            new_image = 255 * np.ones((target_height, target_width, 3), dtype=np.uint8)

            # Вычисляем координаты для вставки оригинального изображения в центре
            x_offset = (target_width - width) // 2
            y_offset = (target_height - height) // 2

            # Вставляем оригинальное изображение на белый фон
            new_image[y_offset:y_offset+height, x_offset:x_offset+width] = image

            # Сохраняем измененное изображение
            output_image_path = os.path.join(output_folder, image_file)
            cv2.imwrite(output_image_path, new_image)
        else:
            # Если изображение уже имеет нужный размер, сохраняем его без изменений
            output_image_path = os.path.join(output_folder, image_file)
            cv2.imwrite(output_image_path, image)

# Пути к папке с изображениями и папке для сохранения результатов
input_folder_1 = 'images/brushes'
input_folder_2 = 'images/paints'
input_folder_3 = 'images/paper'

output_folder_1 = 'images/resizeBrushes'
output_folder_2 = 'images/resizePaints'
output_folder_3 = 'images/resizePaper'

# Выполняем изменение размеров изображений
resize_images(input_folder_1, output_folder_1)
resize_images(input_folder_2, output_folder_2)
resize_images(input_folder_3, output_folder_3)