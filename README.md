# Livemint News Article Scraper using Scrapy

This project scrapes news articles from the Livemint website using Scrapy. The scraped data includes the headline, link, author name, publication date, and article content, formatted as a JSON file.

## Requirements

- Python 3.7+
- Scrapy 2.5+

## Steps to Follow:

1. Install Scrapy: If you haven’t installed Scrapy yet, use:
   pip install scrapy

2. Create a Scrapy Project: In the terminal, navigate to the directory where you want your project and create a new Scrapy project:
   scrapy startproject news_scraper
   
4. Navigate to the Project Directory:
   cd news_scraper

5. Create the Spider File: Create a spider for website by running the command:
   scrapy genspider livemint livemint.com
6. Modify the Spider: Inside spider file (e.g., livemint_spider.py), write the code to scrape articles.
7. Step 5: Output to JSON:
   scrapy crawl livemint -o livemint_articles.json


