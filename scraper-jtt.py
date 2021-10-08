#!/usr/bin/env python3

import os, sys, errno, argparse
import os.path

import requests, yaml
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Scraper for justatranslatortranslations.com')
parser.add_argument('book', help='book name (from books.yml) to scrape')
args = parser.parse_args()

books = None
book_info = None
with open('books.yml', 'r') as f:
  books = yaml.load(f.read(), Loader=yaml.Loader)

for book in books:
    if args.book in book.keys():
        book_info = book[args.book]

url_base = book_info['url_base']
chapter_base = book_info['chapter_base']
start_chapter = book_info['start_chapter']
dirname = book_info['raw_dirname']

try:
    os.mkdir(dirname)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

rs = requests.Session()

# Boostrap loop
url = url_base + chapter_base + str(start_chapter)
i = start_chapter

while True:
    #url = top_url + str(i)
    content = None
    overwrite = False
    name = chapter_base + str(i)
    filename = name + '.html'
    existing_files = os.listdir(dirname)
    existing_files.sort(key=lambda s: int(s.rsplit('.')[0].rsplit('-')[-1]))
    if filename in existing_files:
        print('already have', filename)
        with open(dirname + filename, 'rb') as f:
            content = f.read()
        if existing_files[-1] == filename:
            print("This is the last file, overwriting")
            overwrite = True

    if not content or overwrite:
        print('getting', filename)
        print(url)
        response = rs.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            sys.exit()
        content = response.content
        with open(dirname + filename, 'wb') as f:
            f.write(content)
            print()

    soup = BeautifulSoup(content, 'lxml')
    next_el = soup.find('a', text='[Next Chapter]')
    debug_chapter = soup.find('h1', {"class": "entry-title"}).text.split(' ')[1].rstrip(':')	
    print(debug_chapter, " ", i)
    if int(debug_chapter) != i:
        print("Mismatching Chapter number in document!")
        sys.exit()

    if next_el is None:
        print("No next chapter element found")
        break
    else:
        print(next_el)
        url = next_el['href']

    i += 1
