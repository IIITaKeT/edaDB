# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
from time import time
import requests
import re

def PageCount(soup_url):
    check_arr = soup_url.find('div', class_='xf-sort__total js-list-total')
    if check_arr:
        str_count = int(check_arr.find('span', class_='js-list-total__total-count').get_text())//24 + 1
        return str_count
    else:
        str_count = 0
        return str_count

def ProdAdd(goods_view_box, prod_cat):
    global products
    for prod in goods_view_box:
        # prod_name = " ".join(re.findall("\w+", prod.find("h3").get_text()))
        try:
            prod_name = prod.find("h3").get_text()
        except AttributeError:
            prod_name = "Empty"
        try:
            prod_price = re.findall("\w+",prod.find('span', class_='new_pr').get_text())
        except AttributeError:
            prod_price = [0,0]
        products.append([prod_cat, prod_name, float('{pr[0]}.{pr[1]}'.format(pr = prod_price))])
    print("Текущая категория - {}, Количество товаров - {}".format(prod_cat, len(products)))

category, products = [], []
req_head = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
url = "http://www.abri-kos.ru"

page = requests.get(url, headers = req_head)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find('div', class_='catalog-menu open').find_all('a'):
    category.append([url + str(cat.get('href')), cat.get_text()])

for ref, name in category:
    fts_page = requests.get(ref, headers = req_head)
    meta_soup = BeautifulSoup(fts_page.text, 'html.parser')
    need_soup = meta_soup.find('div', class_="catalog")
    ProdAdd(need_soup.find_all('div', class_='item'), name)
    for page_num in range(2, 100):
        link = "{}page_{}/".format(ref, page_num)
        page = requests.get(link, headers = req_head)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.find('div', class_="mainContent").find('h1').get_text() == "Товар отсутствует":
            break
        else:
            trg_soup = soup.find('div', class_="catalog")
            ProdAdd(trg_soup.find_all('div', class_='item'), name)

with open('abi_products.txt', 'w', encoding="utf-8") as file:
    for b in products:
        file.write("{w[0]}\t{w[1]}\t{w[2]}\n".format(w = b))
    file.close()