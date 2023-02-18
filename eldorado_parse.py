from urllib.parse import quote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from settings import *


def parse_eldorado(driver, addlink: str, page_iter):
    list_result = []
    addlink = quote(addlink)
    if page_iter == 1:
        driver.get(ELDORADO_SITE+"search/catalog.php?q="+addlink+"&utf")
    else:
        driver.get(
            ELDORADO_SITE + "search/catalog.php?q=" + addlink + "&offset=" + str(page_iter * 36) + "&utf"
        )
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//a[@class='JD']"))
        )
    except NoSuchElementException:
        return

    names = driver.find_elements(By.XPATH, "//a[@class='JD']")
    prices = driver.find_elements(By.XPATH, "//span[@class='OQ VQ']")

    for count in zip(names, prices):
        prices_for = count[1].text
        names_for = count[0].text
        prices_for = prices_for.replace(" ", "").replace("₽", "")
        list_result.append(f"{names_for} {prices_for}")
    return list_result


def find_number_of_pages_eldorado(driver, addlink):
    driver.get(ELDORADO_SITE + 'search/catalog.php?q=' + quote(addlink) + "&utf")
    driver.implicitly_wait(3)
    try:
        pages = driver.find_element(By.XPATH, "//div[@class='yo d']/ul")
        return int(pages.text[len(pages.text)-1])  # берем последнию страницу в списке старниц
    except NoSuchElementException:
        return 1  #Всего одна страница
