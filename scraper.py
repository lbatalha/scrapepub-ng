#!/usr/bin/env python3

import os, sys, errno
import os.path

import requests
from bs4 import BeautifulSoup

url_base = 'http://gravitytales.com/novel/age-of-adepts/'
chapter_base = 'aoa-chapter-'
start_chapter = 0

dirname = 'raw_aoa/'
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