import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# # Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size for headless mode
chrome_options.add_argument("--disable-dev-shm-usage")  # Fixes issues with /dev/shm
chrome_options.add_argument("--pageLoadStrategy=none") # page load strategy

# Set a User-Agent header to mimic a legitimate browser request
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

def htmlsoup(url):

        # Use Selenium to open the page and let JavaScript render it
    # driver = webdriver.Chrome(executable_path = '/Users/dolee/repo/chromedriver/chromedriver', options = chrome_options)  # You need to have ChromeDriver installed and in your PATH
    driver = webdriver.Chrome(options = chrome_options)  # You need to have ChromeDriver installed and in your PATH
    driver.get(url)

    # Get the page source after JavaScript rendering
    page_source = driver.page_source

    # Close the Selenium browser
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup

# Example usage:
zip_code = "95136"
soup = htmlsoup(f'https:\\www.redfin.com/zipcode/{zip_code}')

properties = []
for i in range(5):
    property = soup.find_all('a',class_="slider-item")[i]['href']
    properties.append(property)
    print(i)

def getinfo(property1):
    url1 = f'https:\\www.redfin.com{property1}'
    soup = htmlsoup(url1)

    photo = soup.find('img', class_ = 'landscape widenPhoto')['src']
    address = soup.find('h1', class_='full-address').text
    street = soup.find('div', class_='street-address').text
    citystatezip = soup.find('div', class_='dp-subtext bp-cityStateZip').text
    status = soup.find('div', class_='ListingStatusBannerSection remodel').text #status
    key1 = [x.get_text(strip=True) for x in soup.find_all(class_='statsValue')] #price, bd,bath, sqf
    key2 = [key.get_text(strip = True) for key in soup.find_all('div', class_='keyDetails-row') ] #listing period, type, year, lot, ppsq, ac, wd, fee, city
    content = [x.text for x in soup.find_all('div', class_='sectionContent')]
    school = [x.text for x in soup.find_all('div', class_='schools-content')]
    estimate = soup.find('div', class_='price').text

    # Build a dictionary with the extracted information
    info_dict = {
        'photo': photo,
        'address': address,
        'street': street,
        'citystatezip': citystatezip,
        'status': status,
        'key1': key1,
        'key2': key2,
        'content': content,
        'school': school,
        'estimate': estimate
    }

    return info_dict

infos = []
for property in properties:
    info = getinfo(property)
    infos.append(info)


print('done')