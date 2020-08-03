import requests
from dotenv import load_dotenv
import  os


# Please, read OpenAPI specification: https://dev.bitly.com/v4/v4.json
# OpenAPI editor (ignore errors): https://editor.swagger.io/


def shorten_link(bitly_token,user_url):
    AUTH_HEADERS = { 'Authorization' : f"Bearer {bitly_token}" }

    '''Функция создает битлинки
    Документация - https://dev.bitly.com/v4/#operation/createBitlink

    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly
    user_url -- ссылкка пользователя для сокращения
    возвращаемое значение строка битлинка'''
    
    link = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = { "long_url" : user_url }

    response = requests.post(link, headers = AUTH_HEADERS, json = payload)
    response.raise_for_status()

    bitlink = (response.json())
    return bitlink["id"]

def if_bitlink(bitly_token,user_url):
    AUTH_HEADERS = { 'Authorization' : f"Bearer {bitly_token}" }

    '''Функция проверяет битлинк ли это
    Документация - https://dev.bitly.com/v4/#operation/expandBitlink

    Ключевые аргументы:
    user_url -- ссылкка пользователя для проверки
    возвращаемое значение истина или ложь'''
    
    link = 'https://api-ssl.bitly.com/v4/bitlinks'
    payload = { "long_url" : user_url }

    response = requests.post(link, json = payload)
    response.raise_for_status()

    url = (response.json())
    return url

def counter_link(bitly_token,user_url):
    AUTH_HEADERS = { 'Authorization' : f"Bearer {bitly_token}" }
    
    '''Функция считывает переходы по битлинку
    Документация - https://dev.bitly.com/v4/#operation/getClicksForBitlink

    Ключевые аргументы:
    bitly_token -- Токен пользователя сервиса bitly
    user_url -- битлинк пользователя
    возвращаемое значение количество кликов по битлинку'''

    link = f'{BITLY_URL}/bitlinks/{user_url}/clicks/summary'
    payload = {"unit":'week', 'units': -1}

    response = requests.get(link, headers = AUTH_HEADERS, params = payload)
    response.raise_for_status()

    count_clicks = response.json()
    return count_clicks["total_clicks"]
    

if __name__ == '__main__':

    load_dotenv()
    bitly_token = os.getenv('USER_TOKEN')
    user_url = input('Введите ссылку которую хотите сократить или узнать переходы: ')

    if user_url.startswith('bit'):
        try: 
            counter_link(bitly_token,user_url)
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша biy.ly ссылка не корректная!\nВведите ссылку в формате "bit.ly/30iqvat".')
        else:
            print(f'Количество переходов по вашей ссылке {user_url}: {counter_link(bitly_token,user_url)}')
    else:
        try: 
            shorten_link(bitly_token,user_url)
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша ссылка не корректная!\nВведите ссылку в формате "https://dvmn.org/modules/"')
        else:
            print(f'Ваш битлинк: {shorten_link(bitly_token,user_url)}' )