import cv2
import os

def extract_objects_transparent(input_folder, output_folder):
    # Создаем выходную папку, если она не существует
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем список файлов во входной папке
    image_files = os.listdir(input_folder)

    for image_file in image_files:
        # Считываем изображение
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Преобразуем изображение в оттенки серого
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Применяем алгоритм пороговой обработки, чтобы выделить фон
        _, thresholded_image = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY)

        # Создаем маску для выделения объектов (инвертируем пороговое изображение)
        object_mask = cv2.bitwise_not(thresholded_image)

        # Применяем маску к оригинальному изображению
        transparent_image = cv2.bitwise_and(image, image, mask=object_mask)

        # Создаем новое изображение с прозрачным фоном
        transparent_image = cv2.cvtColor(transparent_image, cv2.COLOR_BGR2BGRA)
        transparent_image[:, :, 3] = object_mask

        # Сохраняем изображение с прозрачным фоном
        output_image_path = os.path.join(output_folder, image_file.split('.')[0] + '.png')
        cv2.imwrite(output_image_path, transparent_image)

# Пути к папкам с изображениями и папкам для сохранения результатов
input_folder_1 = 'images/resizeBrushes'
input_folder_2 = 'images/resizePaints'
input_folder_3 = 'images/resizePaper'

output_folder_1 = 'images/newBrushes'
output_folder_2 = 'images/newPaints'
output_folder_3 = 'images/newPaper'

# Выполняем обработку каждой папки с изображениями
extract_objects_transparent(input_folder_1, output_folder_1)
extract_objects_transparent(input_folder_2, output_folder_2)
extract_objects_transparent(input_folder_3, output_folder_3)