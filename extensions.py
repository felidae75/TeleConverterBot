from get_requests_data import values_data
from data import values_dict, values_dict_reverse


class APIException(Exception):
    pass


class GetConvertData:
    @staticmethod
    def get_price(user_input):
        if len(user_input) == 2:
            # Если две валюты без цифры, то курс 1 к 1
            base_func, quote_func = user_input
            amount_func = 1
        else:
            base_func, quote_func, amount_func = user_input
            # Валюта изначальная, валюта, в которую конвертировать, сколько конвертировать

        base_func = base_func.strip()
        quote_func = quote_func.strip()

        try:
            amount_func = float(amount_func)   # Сколько конвертировать
        except ValueError:
            raise APIException('Не введено число')

        try:
            if len(base_func) == 3:                # Проверка формата ввода. Если три буквы, то это usd или eur
                base_func = values_data[base_func.upper()]
            else:
                base_func = values_data[values_dict[base_func]]  # Из чего конвертировать
        except KeyError:
            raise APIException(f'Бот не может обработать валюту "{base_func}"')

        try:
            if len(quote_func) == 3:
                quote_func = values_data[quote_func.upper()]
            else:
                quote_func = values_data[values_dict[quote_func]]  # Во что конвертировать
        except KeyError:
            raise APIException(f'Бот не может обработать валюту "{quote_func}"')

        if base_func == quote_func:
            raise APIException('Две одинаковых валюты')

        return base_func, quote_func, amount_func


class GetRateText:
    @staticmethod
    def text_rate(rate_command):
        value_for_eur = float(values_data[rate_command])
        # В том апи курс по отношению к евро, поэтому опять формулы перерасчёта
        value_for_usd = float(values_data[rate_command]) / float(values_data['USD'])
        value_for_bitcoin = float(values_data[rate_command]) / float(values_data['BTC'])
        value_for_rub = float(values_data[rate_command]) / float(values_data['RUB'])
        value_for_cny = float(values_data[rate_command]) / float(values_data['CNY'])
        text = f'Курс {values_dict_reverse[rate_command]}:\n'
        text += '\nБиткоин {0:^10} {1:>20.7f}'.format("-", value_for_bitcoin) if rate_command != "BTC" else ""
        text += '\nДоллар {0:^14} {1:>14.7f}'.format("-", value_for_usd) if rate_command != "USD" else ""
        text += '\nЕвро {0:^24} {1:>0.7f}'.format("-", value_for_eur) if rate_command != "EUR" else ""
        text += '\nРубль {0:^20} {1:>10.7f}'.format("-", value_for_rub) if rate_command != "RUB" else ""
        text += '\nЮань {0:^20} {1:>10.7f}'.format("-", value_for_cny) if rate_command != "CNY" else ""
        return text
