# scrapepub-ng
python3 remake of raylu's [scrapepub](https://github.com/raylu/scrapepub)

## Features

- Eventual code duplication due to maximum lazyness!
- Stores local copy of scrapes so you only download new chapters
- Supports ongoing releases - always redownloads last chapter to ensure there are no new chapters

## Requirements

* Python 3
* requests
* ebooklib

## Usage

Right now this is hardcoded to rip Age of Adepts from gravitytales

1) Scrape the website: `./scraper.py`
2) Create the epub: `./binder.py`

### Notes
Do not delete the raw dump directory, otherwise you will rescrape all chapters from the start (stuff like AoE takes >15m)



