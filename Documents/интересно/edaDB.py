from bs4 import BeautifulSoup
from time import time
import requests
import re
import asyncio

async def resolve_url(url, result_array):
    page = await requests.get(url)
    soup = await BeautifulSoup(page.text, 'html.parser')
    check_arr = soup.find('div', class_='el_paginate')
    if check_arr:
        result_array.append(int(re.findall('\d+$', check_arr.find('div', class_='signature').get_text())))


products, category, list_count = [], [], []
min_work = 0.0
# max_time = 0.0

url = "https://www.utkonos.ru/cat"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find_all('a', class_='module_catalogue_icons-item'):
    category.append(['https://www.utkonos.ru' + str(cat.get('href')), cat.get_text()])

for ref, name in category:
    # t = time()
    page = requests.get(ref)
    soup = BeautifulSoup(page.text, 'html.parser')
    check_arr = soup.find('div', class_='el_paginate')
    # test_t = round(time() - t, 1)
    if check_arr:
        token = re.findall('\d+$', check_arr.find('div', class_='signature').get_text())
        # min_work = round(int(token[0]) * test_t / 60, 2 )
        list_count.append(int(token[0]))
        # print(str(name) + " - время полного запроса: " + str(min_work) + "мин.")
        # max_time += min_work
    else:
        list_count.append(0)
        # print(str(name) + " - время полного запроса: " + str(test_t))
        # max_time += round(test_t/60,2)

# print(str(max_time) + 'минут')

