#!/usr/bin/env python3

import os, sys, errno, argparse, time, yaml
import os.path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


parser = argparse.ArgumentParser(description='Scraper for WuxiaWorld')
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
end_chapter = book_info['end_chapter']
dirname = book_info['raw_dirname']

try:
    os.mkdir(dirname)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# ck = MozillaCookieJar()
# ck.load(filename="cookies.txt", ignore_expires=True)
# for cookie in ck:
#     cookie.expires = time.time() + 14 * 24 * 3600

# def read_cookies(p = 'cookies.txt'):
#     cookies = []
#     with open(p, 'r') as f:
#         for e in f:
#             e = e.strip()
#             if e.startswith('#'): continue
#             k = e.split('\t')
#             if len(k) < 3: continue	# not enough data
#             # with expiry
#             cookies.append({'name': k[-2], 'value': k[-1], 'expiry': int(k[4])})
#     return cookies
# cookies = read_cookies()
#print('[+] Read {} cookies'.format(len(cookies)))
#print(cookies)

firefox_profile = FirefoxProfile('/home/lbatalha/.mozilla/firefox/9pyn999h.default-release')
#firefox_profile.set_preference()

options = webdriver.FirefoxOptions()
options.page_load_strategy = "none"
options.profile = firefox_profile
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(2)

# Boostrap loop
url = url_base + chapter_base + str(start_chapter)
i = start_chapter
driver.get(url_base)
while True:
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

        driver.get(url)

        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='shadow-chapter-lock']")))
        # print("done waiting")
        time.sleep(1)
        content = driver.page_source

        with open(dirname + filename, 'w') as f:
            f.write(content)

    i += 1
    if i <= end_chapter:
        url = url_base + chapter_base + str(i)
    else:
        print("Last chapter downloaded")
        sys.exit(0)
