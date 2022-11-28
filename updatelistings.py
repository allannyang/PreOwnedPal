from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import math

url = 'https://www.amiami.com/eng/search/list/?s_keywords=nendoroid&s_st_condition_flg=1&s_sortkey=preowned'
driver = webdriver.Chrome()
driver.get(url)

sleep(5)
get_html = driver.execute_script(
    "return document.getElementsByTagName('html')[0].innerHTML")

html = BeautifulSoup(get_html, 'html.parser')

num_items_html = html.findAll(
    "p", attrs={"class": "search-result__text"})

# calculate number of pages to iterate through
num_items_text = ''
i = 0

for item in num_items_html:
    num_items_text = item.text

num_items = int(num_items_text.split()[2])
num_pages = math.ceil(num_items / 20)

# iterate through all listed pages, log name, company, price
text = open("database.txt", "w+")

for x in range(num_pages):
    url = 'https://www.amiami.com/eng/search/list/?s_keywords=nendoroid&s_st_condition_flg=1&s_sortkey=preowned&pagecnt=' + \
        str(x + 1)

    driver.get(url)

    # print(url)

    sleep(3)
    get_html = driver.execute_script(
        "return document.getElementsByTagName('html')[0].innerHTML")

    html = BeautifulSoup(get_html, 'html.parser')

    listings = html.findAll(
        "p", attrs={"class": "newly-added-items__item__name"})
    brands = html.findAll(
        "p", attrs={"class": "newly-added-items__item__brand"})
    prices = html.findAll(
        "p", attrs={"class": "newly-added-items__item__price"})

    for child in html.findAll(
            "span", attrs={"class": "newly-added-items__item__price_state_discount mleft"}):
        child.decompose()

    for listing, brand, price in zip(listings, brands, prices):
        text.write(listing.text + " \n" + brand.text + "\n" +
                   price.text.strip().replace('JPY', '').replace('~', '').replace(' ', '').replace('\n', '') + " JPY\n")

text.close()
