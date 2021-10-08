#!/usr/bin/env python

import os, argparse

import yaml

from bs4 import BeautifulSoup
from ebooklib import epub


parser = argparse.ArgumentParser(description='binder for readnoveful')
parser.add_argument('book', help='book name (from books.yml) to scrape')
args = parser.parse_args()

books = None
book_info = None
with open('books.yml', 'r') as f:
  books = yaml.load(f.read(), Loader=yaml.Loader)

for book in books:
    if args.book in book.keys():
        book_info = book[args.book]

ebook_filename = book_info['ebook_filename']
dirname = book_info['raw_dirname']
chapter_files = os.listdir(dirname)


book = epub.EpubBook()

# set metadata
book.set_identifier(book_info['uuid']) # literally just used uuidgen
book.set_title(book_info['title'])
book.set_language(book_info['language'])
book.add_author(book_info['author'])

chapters = []

for cf in chapter_files:
    with open(dirname+cf, 'rb') as f:
        content = f.read()
    print(cf)
    soup = BeautifulSoup(content, 'lxml')

	# Delete the chapter nav hrefs and other stray crap
    for crap in soup.find_all('p', {"style":"text-align: center;"}):
        crap.decompose()

    chapter_body = "".join(str(soup.find('div', {"id":"chr-content"})).split("\n")[1:-1])
    print(chapter_body)
    ch = epub.EpubHtml(title='Chapter {}'.format(cf.split(".")[0].split("-")[-1]), file_name=dirname+cf, lang='en')
    ch.set_content(chapter_body)
    book.add_item(ch)
    chapters.append(ch)


# define Table Of Contents
book.toc = ((epub.Section(book_info['title']),"" ),(epub.Section('Chapters'), chapters ))


book.spine = chapters

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
#style = 'BODY {color: black;}'
#nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# # add CSS file
#book.add_item(nav_css)
# basic spine
#book.spine = ['nav', c1]

# write to the file
epub.write_epub(ebook_filename, book, {})
