from urllib.request import urlopen
from xml.etree import ElementTree as ET
import time

def get_currencies(currencies_ids_lst=['R01235', 'R01239', 'R01820']):
    """
    Получение данных о текущих курсах валют с сайта Центробанка РФ
    """
    cur_res_str = urlopen("http://www.cbr.ru/scripts/XML_daily.asp")
    result = {}
    cur_res_xml = ET.parse(cur_res_str)
    root = cur_res_xml.getroot()
    valutes = root.findall('Valute')
    for el in valutes:
        valute_id = el.get('ID')
        if str(valute_id) in currencies_ids_lst:
            valute_cur_val = el.find('Value').text
            result[valute_id] = valute_cur_val
    time.clock()
    return result

class CurrencyBoard():
    """
    Класс-синглтон
    """
    def __init__(self):
        """
        Хранение данных о валютах
        """
        self.currencies = ['R01235','R01239','R01820']
        self.rates = get_currencies(self.currencies)

    def get_currency_from_cache(self, code):
        """
        Получение информации о всех сохраненных в кэше валютах без запроса к сайту
        """
        return self.currencies[code]

    def get_new_currency(self, code):
        """
        Метод о запросе курса новой валюты (с получением свежих данных с сервера) и добавлением её в кэш
        """
        self.currencies.append(code)
        self.rates.update(get_currencies([code]))
        return self.rates[code]

    def update(self):
        """
        Метод класса для принудительного обновления данных о валютах
        """
        new_val = get_currencies(self.currencies)
        self.rates.update(dict(zip(sorted(self.currencies),new_val.values())))
        return self.rates

    def check(self):
        """
        Проверка времени загрузки данных
        """
        if (time.clock() > 5*60):
            return get_currencies(self.currencies)
        else:
            print('Last update was made less than 5 minutes ago')

cur_vals = get_currencies()

print("\ndollar = USD = R01235 \neuro = EUR = R01239 \niena = GBP = R01820  \n", cur_vals)
