from bs4 import BeautifulSoup
import requests

products, category, list_count = [], [], []

url = "https://www.utkonos.ru/cat"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

for cat in soup.find_all('a', class_='module_catalogue_icons-item'):
    category.append('https://www.utkonos.ru' + str(cat.get('href')))

for prod in category:
    page = requests.get(prod)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_count.append(soup.find('div', class_='signature').get_text())

for i in range(len(category)):
    print(category[i] + " - внизу - " + list_count[i])