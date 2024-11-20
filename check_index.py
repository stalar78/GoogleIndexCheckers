import requests
from bs4 import BeautifulSoup
import time
import os

def check_index_status(domain):
    url = f"https://www.bing.com/search?q=site:{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        print(f"Проверяем домен: {domain}")
        response = requests.get(url, headers=headers)
        print(f"Получен ответ для {domain} с кодом: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Проверяем наличие результатов на странице
            results = soup.find_all('li', class_='b_algo')
            if results:
                return True
            else:
                return False
    except Exception as e:
        print(f"Ошибка при проверке домена {domain}: {e}")
    
    return False

def batch_check(domains_file):
    print(f"Запуск batch_check для файла: {domains_file}")
    
    if not os.path.exists(domains_file):
        print(f"Файл {domains_file} не найден. Проверьте путь и имя файла.")
        return

    try:
        with open(domains_file, "r", encoding="utf-8") as file:
            domains = [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Ошибка при открытии файла {domains_file}: {e}")
        return

    if not domains:
        print(f"Файл {domains_file} пуст. Добавьте домены для проверки.")
        return

    print(f"Начало проверки {len(domains)} доменов.")
    for domain in domains:
        print(f"Начинаем проверку домена: {domain}")
        is_indexed = check_index_status(domain)
        status = "проиндексирован" if is_indexed else "не проиндексирован"
        print(f"Домен {domain} - {status}")
        
        # Не перегружать Bing запросами, добавляем задержку
        time.sleep(1)

if __name__ == "__main__":
    print("Запуск программы")
    try:
        batch_check("domains.txt")
    except Exception as e:
        print(f"Ошибка при выполнении batch_check: {e}")
    print("Программа завершена")
