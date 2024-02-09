#!/usr/bin/env python

import os, sys, argparse
import yaml

from bs4 import BeautifulSoup
from ebooklib import epub
from natsort import os_sorted

parser = argparse.ArgumentParser(description='Scraper for chrysanthemumgarden')
parser.add_argument('book', help='book name (from books.yml) to scrape')
args = parser.parse_args()

books = None
book_info = None
with open('books.yml', 'r') as f:
  books = yaml.load(f.read(), Loader=yaml.Loader)

for book in books:
    if args.book in book.keys():
        book_info = book[args.book]

# Validate alphabet cipher config options
decipher = False
alpha_configured = len({'cipher_alpha', 'base_alpha'}.intersection(set(book_info)))
if alpha_configured == 2:
    if len(book_info['cipher_alpha']) != len(book_info['base_alpha']):
        print("Configured Base and Ciphered alphabets have different lengths, aborting")
        sys.exit()
    decipher = True
elif alpha_configured != 0:
    print("Only one of `cipher_alpha` or `base_alpha` configured. Either both or none must be configured for each book, Aborting")
    sys.exit()


ebook_filename = book_info['ebook_filename']
dirname = book_info['raw_dirname']
chapter_files = os_sorted(os.listdir(dirname))


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

    soup = BeautifulSoup(content, 'lxml')
    novel_content = soup.find('div', id='novel-content')
    try:
        # Strip dumb watermarks
        for i in (novel_content.find_all(attrs={'style': 'height:1px;width:0;overflow:hidden;display:inline-block'})
                + novel_content.find_all(attrs={'class': 'publift'})):
            i.decompose()
        # Dejumble
        if decipher:
            for block in novel_content.find_all(attrs={'class': 'jum'}):
                t = block.string
                tt = t.maketrans(book_info['base_alpha'], book_info['cipher_alpha'])
                block.string.replace_with(t.translate(tt))

    except AttributeError:
        pass
    chapter_body = "".join(str(novel_content).split("\n"))
    print(cf.split(".")[0].split("-")[-1])
    ch_title = soup.find('span', {'class': 'chapter-title'}).get_text()
    ch = epub.EpubHtml(title=ch_title, file_name=dirname+cf, lang='en')
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
# style = 'BODY {color: black;}'
# nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# # add CSS file
# book.add_item(nav_css)


# write to the file
epub.write_epub(ebook_filename, book, {})
