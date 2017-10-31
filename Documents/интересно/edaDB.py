from bs4 import BeautifulSoup
from time import time
import requests
import re

def PageCount(soup_url):
    check_arr = soup_url.find('div', class_='el_paginate')
    if check_arr:
        str_count = int(re.findall('\d+$', check_arr.find('div', class_='signature').get_text()))
        return str_count
    else:
        str_count = 0
        return str_count

def ProdAdd(goods_view_box):
    global products
products = []
category, list_count = [], []
min_work, x = 0.0, 0
# max_time = 0.0

url = "https://www.utkonos.ru/cat"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find_all('a', class_='module_catalogue_icons-item'):
    category.append(['https://www.utkonos.ru' + str(cat.get('href')), cat.get_text()])

for ref, name in category:
    page = requests.get(ref)
    soup = BeautifulSoup(page.text, 'html.parser')
    for page_num in range(2, PageCount(ref)):
        link = "{}/page/{}".format(ref, page_num)
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        token = soup.find_all('div', class_='goods_pos_bottom')