# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
import requests

token = ''
booksArr = []
for pageNum in range(1,5):
    url = 'https://www.litres.ru/page-' + str(pageNum) + '/'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for book in soup.find_all('div', class_='cover'):
        for line in book.get('data-obj'):
            if line not in ['\n', '\t', '{']:
                token = token + str(line)
booksArr = token.split('}')
with open('books.txt', 'w') as file:
    for b in booksArr:
        file.write(b + '\n')
    file.close()