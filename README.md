# WebScrapper

A project for scrapping static and dynamic pages using Selenium, Beautiful Soup and Openpyxl.

## Modules

- Pages: pages to be scrapped with the tools on `webscrapper/src` module.
- WebScrapper: main module for webscrapping:
  - Utils: tools related to files, logging and time
  - Browser: Selenium manager class
  - Scrapper: Beautiful Soup manager class
  - Excel: Openpyxl manager class

## Set Up

1. Download project files
1. Create path "application/chrome/chrome_driver"
   1. Save there the _Chrome Driver_ version **129.0.6668.70** files
1. Create path "application/chrome/chrome_for_testing"
   1. Save there the _Chrome For Testing_ version **129.0.6668.70** files
1. Install [Python 3.12.6](https://docs.python.org/release/3.12.6/).
   1. Run command `py -m venv venv` to install a new virtual environment
   1. Activate environment: `venv\scripts\activate`
   1. Install modules: `pip install -r requirements-pro.txt`
1. Run project with `py webscrapper`

## Pages

You can web scrape the pages you want by doing the logic in a file inside "pages" and running the scrap command in the main.py
