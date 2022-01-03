import requests
from bs4 import BeautifulSoup
from math import ceil
import csv
import os


def create_csv(csv_title):
    """
    Cette fonction créé un fichier csv avec pour chacun le header
    le fichier est créé avec le nom de la catégorie

    Args:
        csv_title (str): titre de chaque catégorie scrapé
    """
    with open(csv_title, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        header = ["title","upc","price_including_taxe","price_excluding_taxe","number_available","product_description","category_book","review_ratings"]
        writer.writerow(header)


def find_book(url):
    """ cette fonction va dans toutes les pages de la catégorie pour récupérer les urls de tous les livres

    Args:
        url (string): lien de la page dans une catégorie

    Returns:
        liste : la fonction retourne la liste de tous les livres de la catégorie
    """
    books = []
    category_page = requests.get(url)
    soup_category_page = BeautifulSoup(category_page.text, 'html.parser')
    links_books = soup_category_page.findAll('div', class_="image_container")
    for product in links_books:
        a = product.find('a')
        link_book = a['href'].replace('../../..', '')
        books.append('http://books.toscrape.com/catalogue' + link_book)
    return books


images = []
images_names = []
def write_book(category, url):
    """Cette fonction récupère les informations que nous voulons sur chaque livre et les écrit dans le csv de la catégorie

    Args:
        category (string): titre de la catégorie et du fichier pour le modifier
        url (string): url du livre à scraper
    """
    with open(category, 'a', encoding="utf-8-sig") as file:
        response = requests.get(url)
        writer = csv.writer(file, delimiter=',')
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('div', class_="product_main").find('h1').text.replace(",", "").replace("\"", "")
        upc = soup.find(text='UPC').next.text
        price_including_taxe = soup.find(text='Price (incl. tax)').next.text.replace('Â', '')
        price_excluding_taxe = soup.find(text='Price (excl. tax)').next.text.replace('Â', '')
        number_available = soup.find('p', class_='instock').text.replace('In stock (', '').replace('available)','').strip()
        product_description = soup.findAll('p')[3].text.strip().replace(',', '').replace("\"", "")
        category_book = soup.find('ul', class_='breadcrumb').findAll('li')[2].text.strip()
        review_ratings = soup.find(text='Number of reviews').next.next.text
        image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com/')
        name = soup.find('img')['alt'] + ".png"
        informations = [title, upc, price_including_taxe, price_excluding_taxe, number_available, product_description, category_book, review_ratings, image_url]
        images.append(image_url)
        images_names.append(name)
        writer.writerow(informations)

def scrap_images(images, images_names):
    """ cette fonction créé un fichier image avec le contenu de l'image

    Args:
        images (liste): liste des urls des images
        images_names (liste): liste des noms récupérés des images
    """
    for image, name in zip(images, images_names):
        with open(name.replace(' ', '-').replace("/", " "), 'wb') as f:
            im = requests.get(image)
            f.write(im.content) 



urls_categories = []
url = "https://books.toscrape.com/"
page = requests.get(url)
soup_page = BeautifulSoup(page.text, 'html.parser')
links_categories = soup_page.find('ul', class_="nav-list").find('ul').findAll('a')
for category in links_categories:
    href = category['href'].replace('index.html', '')
    urls_categories.append(url + href)


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
        books = find_book(page)
        for book in books:
            write_book(title,book)


os.mkdir(os.path.join(os.getcwd(), 'images'))
os.chdir(os.path.join(os.getcwd(), 'images'))
scrap_images(images,images_names)