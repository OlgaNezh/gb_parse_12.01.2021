import requests
from bs4 import BeautifulSoup
from hw2.db import BlogDb
from hw2.model import Writer
import time


url = 'https://geekbrains.ru/posts'
source = 'https://geekbrains.ru'

def get_data_from_post(bp_url: str, db:BlogDb):
    response = requests.get(bp_url)
    soup_post = BeautifulSoup(response.text, 'html.parser')
    bp_title = soup_post.find('h1', attrs = {'class':'blogpost-title text-left text-dark m-t-sm'}).text
    bp_time = soup_post.find('time', attrs={'class':'text-md text-muted m-r-md'}).text

    writer_name = soup_post.find('div', attrs={'itemprop':"author"}).text
    writer_url = source + soup_post.find('div', attrs={'itemprop':"author"}).parent.parent.find('a')['href']

    key_words = soup_post.find('i', attrs={'class':'i i-tag m-r-xs text-muted text-xs'})['keywords']
    tags = [word.strip() for word in key_words.split(',')]

    writer = Writer(name=writer_name, url=writer_url)
    db.add_post(bp_title,bp_time,bp_url,writer,tags)

if __name__ == "__main__":
    db_url = 'sqlite:///blogpost.sqlite'
    db = BlogDb(db_url)
    # writer = Writer(name='wr1', url='url1')
    # tags1 = ['tag1', 'tag2']
    # tags2 = ['tag2', 'tag3']
    # db.add_post('titl1', 'date1', 'url2', writer, tags1)

    print(1)

    next_page = 'next'
    while next_page != None:
        respose = requests.get(url)
        soup = BeautifulSoup(respose.text, 'html.parser')

        div = soup.find('div', attrs={'class':"post-items-wrapper"})
        div_posts = div.find_all('div', attrs={'class': 'post-item event'})
        for post in div_posts:
            post_url = source + post.find('a')['href']
            get_data_from_post(post_url,db)
            time.sleep(0.1)
        print('Страница {} добавлена в базу'.format(url))
        try:
            ul = soup.find('ul', attrs={'class': 'gb__pagination'})
            next_page = list(ul.find_all('li', attrs={'class':'page'}))[-1].find('a', attrs={'rel': 'next'})['href']
            url = source + next_page
        except:
            next_page = None
    print(1)