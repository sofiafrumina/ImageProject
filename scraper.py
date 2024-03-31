import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_image(url, folder_path, index):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = os.path.join(folder_path, f"{index}.jpg")
            with open(image_name, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Изображение {url} успешно скачано и сохранено как {image_name}.")
        else:
            print(f"Ошибка при скачивании изображения {url}. Статус код: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения {url}: {str(e)}")


def scrape_images(base_url, total_pages, folder_path):
    index = 1
    for page_number in range(1, total_pages + 1):
        page_url = f"{base_url}?page={page_number}"
        page_response = requests.get(page_url)
        
        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.content, 'html.parser')
            product_cards = soup.find_all('article', attrs={'data-chg-product-shelf-index': True})
            for card in product_cards:
                image_url = card.find('img').get('data-src', None)
                if image_url:
                    full_image_url = urljoin(base_url, image_url)
                    download_image(full_image_url, folder_path, index)
                    index += 1
                else:
                    print("data-src битое")
        else:
            print(f"Ошибка при получении страницы {page_url}. Статус код: {page_response.status_code}")

if __name__ == "__main__":
    base_url = "https://www.chitai-gorod.ru/catalog/artists-110621"
    total_pages = 30
    folder_path = "images"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    scrape_images(base_url, total_pages, folder_path)
