#!/usr/bin/env python3

import os, sys, errno, argparse
import os.path

import requests, yaml
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Scraper for Gravitytales')
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
    content = None
    overwrite = False
    name = chapter_base + str(i)
    filename = name
    existing_files = os.listdir(dirname)
    existing_files.sort(key=lambda s: int(s.rsplit('-')[-1]))
    if filename in existing_files:
        print('already have', filename)
        with open(dirname + filename, 'rb') as f:
            content = f.read()
        if existing_files[-1] == filename:
            print("This is the last file, overwriting")
            overwrite = True
    
    if not content or overwrite:
        print('getting', filename)
        response = rs.get(url)
        try: 
            response.raise_for_status()
        except requests.exceptions.HTTPError as e: 
            print(e)
            sys.exit()
        content = response.content
        with open(dirname + filename, 'wb') as f:
            f.write(content)

    soup = BeautifulSoup(content, 'lxml')
    next_el = soup.find('span', text='Next Chapter')
    if next_el is None:
        print("No next chapter element found")
        break
    else:
        url = next_el.find_parent('a')['href']

    i += 1