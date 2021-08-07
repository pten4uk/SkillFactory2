import telebot

from config import TOKEN, keys
from extentions import ConvertCurrency, CurrencyException


BOT = telebot.TeleBot(TOKEN)


@BOT.message_handler(commands=['start', 'help'])
def get_info(message):
    text = 'Инструкция по использованию бота.' \
           '\nВведите: ' \
           '\n<валюта, цену которой хотите узнать> ' \
           '<валюта, в которой хотите узнать цену> ' \
           '<количество первой валюты>' \
           '\n\nПример:' \
           '\nЕвро Доллар 5'
    BOT.send_message(message.chat.id, text)


@BOT.message_handler(commands=['values'])
def get_info(message):
    text = 'Доступные валюты для конвертации:'
    for key in keys.keys():
        text += f'\n{key}'
    BOT.send_message(message.chat.id, text)


@BOT.message_handler()
def convert_currency(message):
    values = ' '.join(message.text.split()).lower()
    values = values.title().split()
    try:
        converted = ConvertCurrency().convert(values)
    except CurrencyException as e:
        print('-'*40)
        print(f'При взаимодействии с пользователем {message.chat.username} произошла ошибка:'
              f'\n{e}')
        BOT.send_message(message.chat.id, f'Ошибка:\n{e}')
    else:
        base, quote, quantity = values
        BOT.send_message(message.chat.id, f'{quantity} {base} = {converted["rates"][keys[quote]] * int(quantity)} {quote}')
        print('-'*40)
        print(f'Пользователь {message.chat.username} успешно переконвертировал валюту')


BOT.polling(none_stop=True)
