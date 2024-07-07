import requests
from bs4 import BeautifulSoup

# Сделайте запрос к сайту
url = 'https://www.rustore.ru/help/sdk/updates/unity/0-2-1'
response = requests.get(url)

# Проверьте, что запрос прошел успешно
if response.status_code == 200:
    # Создайте объект BeautifulSoup
    soup = BeautifulSoup(response.content, 'lxml')

    # Найдите все теги <p>
    p_tags = soup.find_all('p')

    # Извлеките текст из каждого тега <p>
    visible_texts = [p_tag.get_text(strip=True) for p_tag in p_tags]

    # Выведите результат
    for text in visible_texts:
        print(text)
