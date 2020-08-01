import requests
from dotenv import load_dotenv
import  os

load_dotenv()
BITLY_TOKEN=os.getenv('USER_TOKEN')

# Please, read OpenAPI specification: https://dev.bitly.com/v4/v4.json
# OpenAPI editor (ignore errors): https://editor.swagger.io/
USER_URL = input('Введите ссылку которую хотите сократить или узнать переходы: ')
BITLY_URL = 'https://api-ssl.bitly.com/v4'
AUTH_HEADERS = { 'Authorization' : f"Bearer {BITLY_TOKEN}" }

def shorten_link():
    '''
        - https://dev.bitly.com/v4/#operation/createBitlink
        
    '''
    
    link = f'{BITLY_URL}/bitlinks'
    payload = { "long_url" : USER_URL }

    response = requests.post(link, headers = AUTH_HEADERS, json = payload)
    bitlink = (response.json())

    response.raise_for_status()
    return bitlink["id"]


def counter_link():
    
    '''
        - https://dev.bitly.com/v4/#operation/getClicksForBitlink
        
    '''

    link = f'{BITLY_URL}/bitlinks/{USER_URL}/clicks/summary'
    payload = {"unit":'week', 'units': -1}

    response = requests.get(link, headers = AUTH_HEADERS, params = payload)
    count_clicks = response.json()

    response.raise_for_status()
    return count_clicks["total_clicks"]
    

if __name__ == '__main__':
    if USER_URL.startswith('bit'):
        try: 
            counter_link()
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша biy.ly ссылка не корректная!\nВведите ссылку в формате "bit.ly/30iqvat".')
        else:
            print(f'Количество переходов по вашей ссылке {USER_URL}: {counter_link()}')
    else:
        try: 
            shorten_link()
        except requests.exceptions.HTTPError:
            print('ОШИБКА. Ваша ссылка не корректная!\nВведите ссылку в формате "https://dvmn.org/modules/"')
        else:
            print(f'Ваш битлинк: {shorten_link()}' )