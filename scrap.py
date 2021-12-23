import requests
from bs4 import BeautifulSoup
from math import ceil

def create_csv(csv_title):
    with open(csv_title, 'w', encoding="utf-8-sig") as file:
        file.write("title;upc;price_including_taxe;price_excluding_taxe;number_available;product_description;category;review_ratings;image_url")

def find_book(url):
    category_page = requests.get(url)
    soup_category_page = BeautifulSoup(category_page.text, 'html.parser')
    links_books = soup_category_page.findAll('div', class_="image_container")
    for product in links_books:
        a = product.find('a')
        link_book = a['href'].replace('../../..', '')
        books.append('http://books.toscrape.com/catalogue' + link_book)

def write_book(category, url):
    with open(category, 'a', encoding="utf-8-sig") as file:
        response = requests.get(url)
        soup2 = BeautifulSoup(response.text, 'html.parser')
        title = soup2.find('div', class_="product_main").find('h1').text.replace(",", "").replace("\"", "")
        upc = soup2.find(text='UPC').next.text
        price_including_taxe = soup2.find(text='Price (incl. tax)').next.text.replace('Â', '')
        price_excluding_taxe = soup2.find(text='Price (excl. tax)').next.text.replace('Â', '')
        number_available = soup2.find('p', class_='instock').text.replace('In stock (', '').replace('available)',
                                                                                                    '').strip()
        product_description = soup2.findAll('p')[3].text.strip().replace(',', '').replace("\"", "")
        category = soup2.find('ul', class_='breadcrumb').findAll('li')[2].text.strip()
        review_ratings = soup2.find(text='Number of reviews').next.next.text
        """# recupere l'image
        image_url = soup2.find('img')['src'].replace('../..', 'https://books.toscrape.com/')
        # on recupere le alt de l'image pour en faire son nom
        name = soup2.find('img')['alt'] + ".png"
        # on rajoute tout dans les tableaux"""
        file.write(title + ';' + upc + ';' + price_including_taxe + ';' + price_excluding_taxe + ';' + number_available + ';' + product_description + ';' + category + ';' + review_ratings + '\n')


urls_categories = []
books = []


url = "https://books.toscrape.com/"
page = requests.get(url)
soup_page = BeautifulSoup(page.text, 'html.parser')


links_categories = soup_page.find('ul', class_="nav-list").find('ul').findAll('a')
for category in links_categories:
    href = category['href'].replace('index.html', '')
    urls_categories.append(url + href)
"""Ici nous avons récupéré tous les liens de toutes les catégories de livre"""

for category in urls_categories:
    page_category = requests.get(category)
    soup_category = BeautifulSoup(page_category.text, "html.parser")
    title = soup_category.find('h1').text + ".csv"
    create_csv(title)
    number_of_books = soup_category.find('form', class_="form-horizontal").find('strong').text
    category_pages = []
    if int(number_of_books) > 20:
        number_of_pages = ceil(int(number_of_books) / 20)
        for i in range(1, number_of_pages + 1):
            url_page = category + "page-" + str(i) + ".html"
            category_pages.append(url_page)
    if int(number_of_books) <= 20:
        category_pages.append(category)
    for page in category_pages:
        find_book(page)
        for book in books:
            write_book(title,book)

