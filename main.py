import telebot
from config import TOKEN_BOT # Токен бота
from extensions import *   # Классы, обработчики исключений, функции, которые ищут данные по словарям
from data import bot_commands_rate, greeting

bot = telebot.TeleBot(TOKEN_BOT)


@bot.message_handler(commands=['start', 'help'])
def bot_start(message: telebot.types.Message):
    bot.send_message(message.chat.id, greeting())


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    # Выводит список доступных валют
    text = "Список доступных валют:\n"
    for key in values_dict.keys():
        text += '\n{0:<5}{1:^10}/{2:>0}'.format(key, "-", values_dict[key])
    text += f'\n\nЧтобы узнать текущий курс, нажмите на валюту\n\nИнструкция  /start'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=[*bot_commands_rate])
def get_rate(message: telebot.types.Message):
    # Команда для вывода курса конкретной валюты
    rate_command = message.text[1:]   # Срез, потому что там слеш вначале
    text_rate = GetRateText.text_rate(rate_command)
    text_rate += f'\n\nПрочитать инструкцию  /start\n\nСписок доступных валют  /values'
    bot.send_message(message.chat.id, text_rate)


@bot.message_handler(content_types=['text', ])
def convert_func(message: telebot.types.Message):
    try:
        user_input = message.text.title().split(",")

        if not 2 <= len(user_input) <= 3:
            raise APIException('Вы где-то ошиблись, введите две валюты и сумму(не обязательно) через запятую')

        base, quote, amount = GetConvertData.get_price(user_input)
        # Валюта изначальная, валюта, в которую конвертировать, сколько конвертировать

    except APIException as e:
        bot.send_message(message.chat.id, f'{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Техническая ошибка {e}')
    else:
        res = float(quote) * amount / float(base)
        # Бесплатная версия апи не поддерживает автоматическую конвертацию, поэтому формула
        text = f'{amount}   {user_input[0]}\n=\n{res}   {user_input[1]}'
        text += f'\n\nПрочитать инструкцию  /start\n\nСписок доступных валют  /values'
        bot.send_message(message.chat.id, text)


bot.polling()
