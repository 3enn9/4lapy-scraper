import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd

# URL сайта
base_url = "https://4lapy.ru/catalog/koshki/korm-koshki/?page="

# Список для хранения данных
data = []


# Функция для извлечения данных с одной страницы
def scrape_page(page_number):
    url = f"{base_url}{page_number}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('article', class_='CardProduct_root__7zZ3z')

        for product in products:
            product_id = product['data-id']
            product_name_div = product.find('div', class_='CardProduct_productNameInner__Jc_on')
            product_name = product_name_div.text.strip() if product_name_div else "Нет названия"
            product_link_a = product.find('a', class_='CardProduct_link__Rg5M2')
            product_link = product_link_a['href'] if product_link_a else "Нет ссылки"
            price_div = product.find('div', class_='text-price-big')
            price = price_div.text.strip() if price_div else "Нет цены"
            old_price_div = product.find('div', class_='CardProductPrice_priceOld__5UPLv')
            old_price = old_price_div.text.strip() if old_price_div else "Нет старой цены"

            # Добавление данных в список
            data.append({
                "ID товара": product_id,
                "Наименование товара": product_name,
                "Ссылка на товар": product_link,
                "Регулярная цена": price,
                "Старая цена": old_price
            })
        print(f"Page {page_number} готова")
    else:
        print(f"Ошибка при доступе к странице {page_number}: {response.status_code}")


# Основной цикл для всех 25 страниц
for page in range(1, 26):
    scrape_page(page)
    # Пауза от 1 до 5 секунд перед следующим запросом
    time.sleep(random.uniform(1, 5))
    print('след страница')

# Создание DataFrame из списка данных
df = pd.DataFrame(data)

# Сохранение в CSV
df.to_csv('products.csv', index=False, encoding='utf-8-sig')

# Сохранение в JSON
df.to_json('products.json', orient='records', force_ascii=False)

# Сохранение в Excel
df.to_excel('products.xlsx', index=False, engine='openpyxl')

print("Данные успешно сохранены в файлы products.csv, products.json и products.xlsx.")
