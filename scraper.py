import string
import requests
import os
from bs4 import BeautifulSoup


def get_file_name(name):
    for i in (string.punctuation + '—' + '’'):
        if i in name:
            name = name.replace(i, '')
    # split and join are used to delete 2 or more whitespaces INSIDE the text
    return '_'.join(name.strip().split()) + '.txt'


def save_article(title, body):
    file_name = get_file_name(title)
    f = open(f'Page_{p + 1}\\{file_name}', 'w', encoding="utf-8")
    f.write(body)
    f.close()


def find_articles():
    articles = soup.find_all('article')
    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'}).text.strip()
        if article_type == required_type:
            a_url = article.find('a', {'data-track-action': "view article"}).get('href')
            a_resp = requests.get('https://www.nature.com' + a_url)
            a_soup = BeautifulSoup(a_resp.content, "html.parser")
            a_title = a_soup.find('h1', {'class': "c-article-magazine-title"}).text
            a_body = a_soup.find('div', {'class': "c-article-body"}).text.strip()

            save_article(a_title, a_body)


page_num = int(input())
required_type = input().strip()

for p in range(page_num):
    if not os.access(f'Page_{p + 1}', os.F_OK):
        os.mkdir(f'Page_{p + 1}')
    response = requests.get(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={p + 1}')
    soup = BeautifulSoup(response.content, "html.parser")
    find_articles()

print('Saved all articles.')