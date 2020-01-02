#!/usr/bin/env python

import os

from bs4 import BeautifulSoup
from ebooklib import epub


ebook_filename = "age_of_adepts.epub"
dirname = 'raw_aoa/'
chapter_files = os.listdir(dirname)


book = epub.EpubBook()

# set metadata
book.set_identifier('ff08be0e-fc84-448e-913e-f65e943f48cb') # literally just used uuidgen
book.set_title('Age of Adepts')
book.set_language('en')
book.add_author('真的老狼 ZhenDeLaoLang (Real Old Wolf)', file_as='ZhenDeLaoLang')
book.add_author('Eris', file_as='Eris', role='English TL', uid='coauthor')
book.add_author('TsukikageRyu', file_as='TsukikageRyu', role='English Editor', uid='coauthor')

chapters = []

for cf in chapter_files:
    with open(dirname+cf, 'rb') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')
    chapter_body = "".join(str(soup.find('div', id='chapterContent')).split("\n")[1:-1])

    ch = epub.EpubHtml(title='Chapter {}'.format(cf.split("-")[-1]), file_name=dirname+cf, lang='en')
    ch.set_content(chapter_body)
    book.add_item(ch)
    chapters.append(ch)


# define Table Of Contents
book.toc = ((epub.Section('Age of Adepts'),"" ),(epub.Section('Chapters'), chapters ))
        

book.spine = chapters

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)


# write to the file
epub.write_epub(ebook_filename, book, {})