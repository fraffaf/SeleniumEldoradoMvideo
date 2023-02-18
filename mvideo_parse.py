from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from settings  import *


def parse_mvideo_page(driver, addlink: str, page_iter: int):
    list_result = []
    driver.get(
        MVIDEO_SITE + 'product-list-page?q=' + quote(addlink) + "&page=" + str(page_iter) + "&showCount=12"
    )
    driver.implicitly_wait(15)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//span[@class='price__main-value']"))
    )
    names = driver.find_elements(By.XPATH, "//a[@class='product-title__text product-title--clamp']")
    prices = driver.find_elements(By.XPATH, "//span[@class='price__main-value']")

    for count in zip(names, prices):
        prices_for = count[1].text
        names_for = count[0].text
        prices_for = prices_for.replace(" ", "").replace("₽", "")
        list_result.append(f"{names_for} {prices_for}")
    return list_result


def find_number_of_pages_mvideo(driver, addlink):
    driver.get(MVIDEO_SITE + 'product-list-page?q=' + quote(addlink) + "&showCount=12")
    driver.implicitly_wait(3)
    try:
        pages = driver.find_element(By.XPATH, "//a[@class='page-link']")
        return int(pages.text)
    except NoSuchElementException:
        return 1  #Всего одна страница
