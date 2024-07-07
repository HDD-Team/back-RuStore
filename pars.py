import requests
from bs4 import BeautifulSoup


# Сделайте запрос к сайту
# Проверьте, что запрос прошел успешно


def parse(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Создайте объект BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')

        # Найдите все теги <p>
        p_tags = soup.find_all('p')

        # Извлеките текст из каждого тега <p>
        visible_texts = [p_tag.get_text(strip=True) for p_tag in p_tags]
        full_text = ' '.join(visible_texts)
        # Верните результат
        return full_text


