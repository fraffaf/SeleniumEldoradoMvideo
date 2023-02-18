import random
import time
import csv
from os import stat

import fake_useragent
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from settings import *
from eldorado_parse import parse_eldorado, find_number_of_pages_eldorado
from mvideo_parse import parse_mvideo_page, find_number_of_pages_mvideo


def exchange_currency(value_rub: float, currency: str):
    list_value = []
    cbr = requests.get("https://www.cbr.ru/", headers=user_agent())
    cbr.raise_for_status()
    soup = BeautifulSoup(cbr.text, "lxml")
    value_usd = soup.findAll("div", class_="col-md-2 col-xs-9 _right mono-num")
    for el in enumerate(value_usd):
        if el[0] % 2 != 0:
            list_value.append(el[1].text[0:7])
    list_value = list(map(lambda x: float(x.replace(',', '.')), list_value))
    print(list_value)
    if currency == "usd":
        return value_rub / list_value[0]
    elif currency == "eur":
        return value_rub / list_value[1]
    elif currency == "cny":
        return value_rub / list_value[2]
    else:
        raise Exception("argument value error")


def user_agent():
    return {"User-Agent": fake_useragent.UserAgent().random}


def create_driver():
    driver = webdriver.Chrome(options=Options())
    driver.set_window_size(1920, 1080)
    return driver


def main():
    list_result_eldorado = [['eldorado']]
    list_result_mvideo = [['mvideo']]

    number_of_page_eldorado = find_number_of_pages_eldorado(create_driver(), search_name)
    for i in range(0, number_of_page_eldorado):
        list_result_eldorado.append(parse_eldorado(create_driver(), search_name, i))

    number_of_page_mvideo = find_number_of_pages_mvideo(create_driver(), search_name)
    for i in range(0, number_of_page_mvideo):
        print('cicl')
        list_result_mvideo.append(parse_mvideo_page(create_driver(), search_name, i))
    if result_data_type == 'csv':
        if stat('./result.csv').st_size != 0:
            print("файл занят")
            return
        with open('result.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f)
            for a in list_result_eldorado:
                writer.writerows([a])
            for a in list_result_mvideo:
                writer.writerows([a])


if __name__ == "__main__":
    main()
