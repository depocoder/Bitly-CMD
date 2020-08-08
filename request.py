import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv
import requests


def format_url(user_url):
    '''Функция удаляет http или https.

    Docs - https://docs.python.org/3/library/urllib.parse.html#url-parsing
    Ключевые аргументы:
    user_url -- ссылкка пользователя для сокращения.
    Возвращаемое отформотированная ссылка.'''

    url_info = urlparse(user_url)
    url_info = url_info._replace(scheme='')
    user_url = url_info.geturl()[2:]
    return user_url


def shorten_link(bitly_token, user_url):
    '''Функция создает битлинки.

    Docs - https://dev.bitly.com/v4/#operation/createBitlink
    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly.
    user_url -- ссылкка пользователя для сокращения.
    возвращаемое значение строка битлинка.'''

    auth_headers = {'Authorization': f"Bearer {bitly_token}"}
    link = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {"long_url": user_url}
    response = requests.post(link, headers=auth_headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()
    return bitlink["id"]


def check_bitlink(bitly_token, user_url):
    '''Функция проверяет битлинк ли это.

    Docs - https://dev.bitly.com/v4/#operation/expandBitlink
    Ключевые аргументы:
    user_url -- ссылкка пользователя для проверки.
    возвращаемое значение: истина или ложь.'''

    if user_url.find("://") != -1:
        user_url = format_url(user_url)
    auth_headers = {'Authorization': f"Bearer {bitly_token}"}
    link = 'https://api-ssl.bitly.com/v4/expand'
    payload = {"bitlink_id": user_url}
    response = requests.post(link, headers=auth_headers, json=payload)
    return response.ok


def count_clicks(bitly_token, user_url):
    '''Функция считывает переходы по битлинку.

    Docs - https://dev.bitly.com/v4/#operation/getClicksForBitlink
    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly.
    user_url -- битлинк пользователя.
    возвращаемое значение количество кликов по битлинку.'''

    auth_headers = {'Authorization': f"Bearer {bitly_token}"}
    if user_url.find("://") != -1:
        user_url = format_url(user_url)
    link = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}/clicks/summary'
    payload = {"unit": 'week', 'units': -1}
    response = requests.get(link, headers=auth_headers, params=payload)
    response.raise_for_status()
    about_bitlink = response.json()
    return about_bitlink["total_clicks"]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''Этот проект позволяет создать сокращённую ссылки.
        Посмотреть переходы по вашей сокращённой (bit.ly) ссылке
        через командную строку.''')

    parser.add_argument(
        'url', help='''Введите ссылку которую хотите
        сократить или узнать переходы:''')

    args = parser.parse_args()
    user_url = args.url
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    if check_bitlink(bitly_token, user_url):
        try:
            counter_clicks = count_clicks(bitly_token, user_url)
        except requests.exceptions.HTTPError:
            print('''ОШИБКА. Ваша bit.ly ссылка не корректная!
                  Введите ссылку в формате "bit.ly/30iqvat".''')
        else:
            print('Количество переходов',
                  f'по вашей ссылке {user_url}: {counter_clicks}')
    else:
        try:
            short_link = shorten_link(bitly_token, user_url)
        except requests.exceptions.HTTPError:
            print('''ОШИБКА. Ваша ссылка не корректная!
                  Введите ссылку в формате "https://dvmn.org/modules/"''')
        else:
            print(f'Ваш битлинк: {short_link}')
