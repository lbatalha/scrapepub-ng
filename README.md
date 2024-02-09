# scrapepub-ng
python3 remake of raylu's [scrapepub](https://github.com/raylu/scrapepub)

## Features

- Eventual code duplication due to maximum lazyness!
- Stores local copy of scrapes so you only download new chapters
- Supports ongoing releases - always redownloads last chapter to ensure there are no new chapters

## Requirements

- bs4
- requests
- ebooklib
- pyyaml
- selenium
- natsort
- pyicu*

## Usage

Scrapers/binders for different sites, use whatever fits

1) Scrape the website: `./scraper.py`
2) Create the epub: `./binder.py`

### Notes
Do not delete the raw dump directory if you dont want to rescrape all chapters from the start

# Extras

Chyrsanteum Garden uses a custom font with a replacement cipher, there is a sample OCR script to use that font to generate an alphabet in order, and use OCR to generate the replaced variant. the binder then translates the characters as needed.

Wuxiaworld currently has dynamic content so selenium is needed, they will also 403 based on user-agent. Sometimes the pages dont load on time, so adjust the sleep and check for the string "(Teaser)" in the raw files, if present, it didnt unlock the chapter on time.
