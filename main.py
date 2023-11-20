import requests
from bs4 import BeautifulSoup
import lxml
import base64


def get_free_proxies():

    cookies = {
        'fp': '11fa6ff18da1fc58eb98815ba9da0600',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        # 'Cookie': 'fp=11fa6ff18da1fc58eb98815ba9da0600',
        'Upgrade-Insecure-Requests': '1',
    }

    s = requests.Session()
    response = s.get('http://free-proxy.cz/en/proxylist/country/US/http/ping/all', cookies=cookies, headers=headers)

    # with open('index.html', 'w') as file:
    #     file.write(response.text)
        
    # with open('index.html') as file:
    #     src = file.read()

    soup = BeautifulSoup(response.text, 'lxml')
    countries = soup.find('select', id='frmsearchFilter-country').find_all('option')

    print('[INFO] Доступные страны: ')

    for c in countries:
        short_name = c.get('value')
        name = c.text.split('(')[0].strip()
        print(f'{short_name} -- {name}')

    select_country = input('Выберите страну: ')
    url = f'http://free-proxy.cz/en/proxylist/country/{select_country}/http/ping/all'
    print(url)
    print('[INFO] Пожалуйста ожидайте, идет сбор халявы...')

    response = s.get(url, cookies=cookies, headers=headers)
    ip_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        table_trs = soup.find('table', id='proxy_list').find('tbody').find_all('tr')

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

        with open('ip_list.txt', 'w') as file:
            file.writelines(f'{ip}\n' for ip in ip_list)

        print(f'[INFO] Собрали {len(ip_list)} прокси. Хорошего вам дня!')
    else:
        print(f'Что-то пошло не так! Статус код ответа: {response.status_code}')

def main():
    get_free_proxies()


if __name__ == '__main__':
    main()
