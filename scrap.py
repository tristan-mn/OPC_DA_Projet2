import requests
from bs4 import BeautifulSoup
from math import ceil
import csv
import os



def create_csv(csv_title):
    with open(csv_title, 'w') as file:
        writer = csv.writer(file, delimiter=',')
        header = ["title","upc","price_including_taxe","price_excluding_taxe","number_available","product_description","category_book","review_ratings"]
        writer.writerow(header)


def find_book(url):
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
        # recupere l'image
        image_url = soup.find('img')['src'].replace('../..', 'https://books.toscrape.com/')
        # on recupere le alt de l'image pour en faire son nom
        name = soup.find('img')['alt'] + ".png"
        # on rajoute tout dans les tableaux
        informations = [title, upc, price_including_taxe, price_excluding_taxe, number_available, product_description, category_book, review_ratings, image_url]
        images.append(image_url)
        images_names.append(name)
        writer.writerow(informations)

def scrap_images(images, images_names):
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