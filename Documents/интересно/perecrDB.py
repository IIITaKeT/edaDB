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
        prod_name = " ".join(re.findall("\w+", prod.find("div", class_='xf-product__title xf-product-title').get_text()))
        try:
            prod_price = re.findall("\w+",prod.find('div', class_='xf-price').get_text())
        except AttributeError:
            prod_price = [0,0]
        products.append([prod_cat, prod_name, float('{pr[0]}.{pr[1]}'.format(pr = prod_price))])
    print("������� ��������� - {}, ���������� ������� - {}".format(prod_cat, len(products)))

category, products = [], []
req_head = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"}
url = "https://www.perekrestok.ru/catalog"

page = requests.get(url, headers = req_head)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find_all('a', class_='xf-catalog-categories__link'):
    category.append(['https://www.perekrestok.ru' + str(cat.get('href')), cat.get_text()])

for ref, name in category:
    fts_page = requests.get(ref, headers = req_head)
    meta_soup = BeautifulSoup(fts_page.text, 'html.parser')
    need_soup = meta_soup.find('div', class_="catalog__items-wrap js-catalog-wrap")
    ProdAdd(need_soup.find_all('div', class_='xf-product js-product '), re.sub('\n', '', name))
    for page_num in range(2, int(PageCount(meta_soup))):
        link = "{}?page={}".format(ref, page_num)
        page = requests.get(link, headers = req_head)
        soup = BeautifulSoup(page.text, 'html.parser')
        trg_soup = soup.find('div', class_="catalog__items-wrap js-catalog-wrap")
        ProdAdd(trg_soup.find_all('div', class_='xf-product js-product '), re.sub('\n', '', name))

with open('prc_products.txt', 'w') as file:
    for b in products:
        file.write("{w[0]}; {w[1]}; {w[2]}\n".format(w = b))
    file.close()