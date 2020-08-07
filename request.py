import  os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse
import requests

def if_http(user_url):
    '''Функция удаляет http или https.

    Документация - https://docs.python.org/3/library/urllib.parse.html#url-parsing
    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitl.
    user_url -- ссылкка пользователя для сокращения.
    Возвращаемое отформотированная ссылка.'''
        urlib_parce = urlparse(user_url)
        urlib_parce = urlib_parce._replace(scheme='')
        user_url = urlib_parce.geturl()[2:]
        return user_url

def shorten_link(bitly_token,user_url):
    '''Функция создает битлинки.

    Документация - https://dev.bitly.com/v4/#operation/createBitlink
    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly.
    user_url -- ссылкка пользователя для сокращения.
    возвращаемое значение строка битлинка.'''

    auth_headers = {'Authorization' : f"Bearer {bitly_token}"}
    link = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = {"long_url" : user_url}
    response = requests.post(link, headers = auth_headers, json = payload)
    response.raise_for_status()
    bitlink = response.json()
    return bitlink["id"]

def if_bitlink(bitly_token,user_url):
    '''Функция проверяет битлинк ли это.

    Документация - https://dev.bitly.com/v4/#operation/expandBitlink
    Ключевые аргументы:
    user_url -- ссылкка пользователя для проверки.
    возвращаемое значение: истина или ложь.'''

    if user_url.find("://") != -1:
        user_url = if_http(user_url)
    auth_headers = {'Authorization' : f"Bearer {bitly_token}"}
    link = 'https://api-ssl.bitly.com/v4/expand'
    payload = {"bitlink_id" : user_url}
    response = requests.post(link, headers = auth_headers, json = payload)
    return response.ok

def count_clicks(bitly_token,user_url):
    '''Функция считывает переходы по битлинку.

    Документация - https://dev.bitly.com/v4/#operation/getClicksForBitlink
    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly.
    user_url -- битлинк пользователя.
    возвращаемое значение количество кликов по битлинку.'''

    auth_headers = {'Authorization' : f"Bearer {bitly_token}"}
    if user_url.find("://") != -1:
        user_url = if_http(user_url)
    link = f'https://api-ssl.bitly.com/v4/bitlinks/{user_url}/clicks/summary'
    payload = {"unit":'week', 'units': -1}
    response = requests.get(link, headers = auth_headers, params = payload)
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
    if if_bitlink(bitly_token,user_url):
        try: 
            count_clicks(bitly_token,user_url)
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша biy.ly ссылка не корректная!\nВведите ссылку в формате "bit.ly/30iqvat".')
        else:
            print(f'Количество переходов по вашей ссылке {user_url}: {count_clicks(bitly_token,user_url)}')
    else:
        try: 
            shorten_link(bitly_token,user_url)
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша ссылка не корректная!\nВведите ссылку в формате "https://dvmn.org/modules/"')
        else:
            print(f'Ваш битлинк: {shorten_link(bitly_token,user_url)}')