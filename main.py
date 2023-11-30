import requests
from bs4 import BeautifulSoup
import lxml
import base64


def get_free_proxies():

    # Сookie для получения данных
    cookies = {
        'fp': '11fa6ff18da1fc58eb98815ba9da0600',
    }

    # Заголовки запроса
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }

    # Создание сессии для отправки запросов
    s = requests.Session()

    # GET-запрос на страницу для получения прокси
    response = s.get('http://free-proxy.cz/en/proxylist/country/US/http/ping/all', cookies=cookies, headers=headers)

    # Создание объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'lxml')

    # Поиск доступных стран для выбора прокси
    countries = soup.find('select', id='frmsearchFilter-country').find_all('option')

    print('[INFO] Доступные страны: ')

    # Вывод доступных стран пользователю
    for c in countries:
        short_name = c.get('value')
        name = c.text.split('(')[0].strip()
        print(f'{short_name} -- {name}')

    # Пользовательский ввод выбранной страны
    select_country = input('Выберите страну: ')
    url = f'http://free-proxy.cz/en/proxylist/country/{select_country}/http/ping/all'
    print(url)
    print('[INFO] Пожалуйста, подождите, идет сбор халявы...')

    # GET-запрос на страницу выбранной страны
    response = s.get(url, cookies=cookies, headers=headers)
    ip_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # Получение таблицы с прокси
        table_trs = soup.find('table', id='proxy_list').find('tbody').find_all('tr')

        # Парсинг IP-адресов и портов прокси
        for tr in table_trs:

            try:
                ip = tr.find('td').find('script').text
            except Exception as ex:
                print(ex)
                continue

            if ip:
                ip = base64.b64decode(ip.split('"')[1]).decode('utf-8')
                port = tr.find('span', class_='fport').text
                print(f'[+] {ip}:{port}')
                ip_list.append(f'{ip}:{port}')
            else:
                continue

        # Запись прокси в файл
        with open('ip_list.txt', 'w') as file:
            file.writelines(f'{ip}n' for ip in ip_list)

        print(f'[INFO] Собрали {len(ip_list)} прокси. Хорошего вам дня!')
    else:
        print(f'Что-то пошло не так! Статус код ответа: {response.status_code}')

        
def main():
    get_free_proxies()


if __name__ == 'main':
    main()
