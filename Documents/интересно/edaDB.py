# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
from time import time
import requests
import re

def PageCount(soup_url):
    check_arr = soup_url.find('div', class_='el_paginate')
    if check_arr:
        str_count = re.findall('\d+$', check_arr.find('div', class_='signature').get_text())
        return str_count[0]
    else:
        str_count = 0
        return str_count

def ProdAdd(goods_view_box, prod_cat):
    global products
    for prod in goods_view_box:
        prod_name = prod.find('div', class_='goods_view_box-caption').get_text()
        prod_price = prod.find('div', class_='goods_price-item current').get_text()
        products.append([prod_cat, prod_name, prod_price])
    print("Текущая категория - {}, Прогресс - {}%".format(prod_cat, round(len(products)/45000,0)))

category, products = [], []

url = "https://www.utkonos.ru/cat"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find_all('a', class_='module_catalogue_icons-item'):
    category.append(['https://www.utkonos.ru' + str(cat.get('href')), cat.get_text()])

for ref, name in category:
    fts_page = requests.get(ref)
    meta_soup = BeautifulSoup(fts_page.text, 'html.parser')
    ProdAdd(meta_soup.find_all('div', class_='goods_pos_bottom'), name)
    for page_num in range(2, int(PageCount(meta_soup))):
        link = "{}/page/{}".format(ref, page_num)
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        ProdAdd(soup.find_all('div', class_='goods_pos_bottom'), name)

with open('products.txt', 'w') as file:
    for b in products:
        file.write("{w[0]}, {w[1]}, {w[2]}".format(w = b))
    file.close()
