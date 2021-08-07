import requests
import json

from config import keys


class CurrencyException(Exception):
    pass


class ConvertCurrency:
    @staticmethod
    def convert(message):

        if len(message) != 3:
            raise CurrencyException('Некорректный ввод!')

        base, quote, quantity = message

        if base == quote:
            raise CurrencyException('Вы пытаетесь перевести валюту саму в себя!')
        elif (base not in keys.keys()) or (quote not in keys.keys()):
            raise CurrencyException('Такой валюты нет в базе данных, \n/help - посмотреть доступные валюты.')
        elif base != 'Евро':
            raise CurrencyException('В настоящее время конвертировать можно только из валюты "Евро"')
        try:
            quantity = int(quantity)
        except ValueError:
            raise CurrencyException('Количество должно быть числом')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key='
                         f'e05d0c5a78edd088c9ea514caa33a167&base={keys[base]}&symbols={keys[quote]}')

        content = json.loads(r.content)
        return content


if __name__ == '__main__':
    i = ConvertCurrency()
    print(i.convert('Доллар Евро 15'.split()))
