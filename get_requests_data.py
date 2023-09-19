import requests
import json
from config import base_api_key

base_url = 'http://data.fixer.io/api/'  # Рандомный апи с курсом. Курс в нём по отношению к Евро


html = requests.get(base_url + "latest?access_key=" + base_api_key + "&format=1").content

api_data = json.loads(html)  # Данные всего апи
values_data = api_data['rates']  # Курс валют из апи (он во вложенном словаре лежит)
