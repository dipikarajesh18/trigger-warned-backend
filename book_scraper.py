import time
from builtins import IndexError
import json
from urllib import request
from bs4 import BeautifulSoup
import re

def get_title(soup):
    try:
        title = soup.select_one("meta[property='og:title']")['content']
        return title
    except:
        return "title not found"

def get_author_names(soup):
    try:
        author_name = soup.select('.authorName')[0].text.strip()
        return author_name
    except:
       return "author name not found"

def get_genres(soup):
    try:
        genres = []
        for node in soup.find_all('div', {'class': 'left'}):
            current_genres = node.find_all('a', {'class': 'actionLinkLite bookPageGenreLink'})
            current_genre = ' > '.join([g.text for g in current_genres])
            if current_genre.strip():
                genres.append(current_genre)
        return genres
    except:
        return "genres not found"


def get_isbn(soup):
    try:
        isbn = soup.select_one("meta[property='books:isbn']")['content']
        return isbn
    except:
        return "isbn not found"

def get_description(soup):
    book_description = []
    try:
        # span = soup.find("span", {"class": "displaytext"})
        description_divs = soup.find_all("div", {"class": "readable stacked", "id": "description"})
        try:
            description_text = description_divs[0].find_all("span")[1].text
        except IndexError:
            try:
                description_text = description_divs[0].find_all("span")[0].text
            except IndexError:
                description_text = "Nil"
        book_description.append(description_text)
        return book_description
        # description = soup.select_one("meta[property='og:description']")['content']
        # return description
    except:
        return "description not found"

def get_page_count(soup):
    try:
        page_count = soup.select_one("meta[property='books:page_count']")['content']
        return page_count
    except:
        return 'page count not found'


def get_year_published(soup):
    try:
        year_first_published = soup.find('nobr', attrs={'class': 'greyText'}).string
        return re.search('([0-9]{3,4})', year_first_published).group(1)
    except:
        return 'year published not found'

def get_image_cover(soup):
    try:
        image = soup.find('img', id='coverImage')
        return image.text
    except:
        return 'image not found'


def scrape_book(book_id):
    with request.urlopen("https://www.goodreads.com/book/show/" + str(book_id)) as client:
        page_html = client.read()
        client.close()

    soup = BeautifulSoup(page_html, 'html.parser')
    if not soup: return ''

    time.sleep(2)

    return {'book_title': get_title(soup),
            'authors' : get_author_names(soup),
            'isbn': get_isbn(soup),
            'year_published': get_year_published(soup),
            'page_count': get_page_count(soup),
            'description': get_description(soup),
            'genres': get_genres(soup),
            'cover': get_image_cover(soup)}


def main():
    first_id = 1
    # last_id = 2
    last_id = 100000     # Last book is 8,630,000
    book_dictionary = []

    for book_id in range(first_id, last_id):
        try:
            book = scrape_book(book_id)
            # print(book)
            book_dictionary.append(book)


        except request.HTTPError as e:
            print('bookid: ', book_id, '\n', e)
            # exit(0)


    with open('book_list_dict_dump', 'w') as fout:
        json.dump(book_dictionary, fout)

    print("done!!")

if __name__ == '__main__':
    main()