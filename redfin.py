import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import requests

def bs4soup(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def random_delay():
    delay = random.uniform(1,5)  # Adjust the range as needed
    time.sleep(delay)

def opendriver(headless):
    # # Set up Chrome options
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
    chrome_options.add_argument("--window-size=1920x1080")  # Set window size for headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fixes issues with /dev/shm
    chrome_options.add_argument("--pageLoadStrategy=eager") # page load strategy
    chrome_options.add_argument("--incognito") # incognico
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") # Set a User-Agent header to mimic a legitimate browser request

    # Use Selenium to open the page and let JavaScript render it
    driver = webdriver.Chrome(options = chrome_options)  # You need to have ChromeDriver installed and in your PATH

    return driver

def htmlsoup(url, driver):
    random_delay()  # add random delay to avoid bot scrapping filtering
    driver.get(url) # get url page

    # Get the page source after JavaScript rendering
    page_source = driver.page_source

    # Close the Selenium browser
    # driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    return soup


def getinfo(property1, driver, max_attempts = 5): #will return detail info of each property1
    attempts = 0

    while attempts < max_attempts:
        url1 = f'https://www.redfin.com{property1}'
        print(url1)
        driver.get(url1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        soup = htmlsoup(url1, driver)

        if soup.find('img', class_ = 'landscape widenPhoto'):

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

            break # exit the loop once we get all the info

        else:
            attempts += 1
            print(f"Element not found. Refreshing and retrying. Attempt {attempts} of {max_attempts}")
            # driver = opendriver(False)
            # driver.get('https://www.redfin.com')
            # driver.refresh() #refresh
            # random_delay() # repeat after some delay
            # driver.get(url1)
            # driver.refresh() #refresh
            # random_delay() # repeat after some delay
            bs4soup(url1)
      

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

# filter
def gen_url(zip = 95136, type = None, minprice = None, maxprice = None, minbeds = None, maxbeds = None, minbaths = None):
    url = f'https://www.redfin.com/zipcode/{zip}'

    filters = []
    filters.append(f'property-type={"+".join(type)}') if type else None
    filters.append(f'min-price={minprice}k') if minprice else None
    filters.append(f'max-price={maxprice}k') if maxprice else None
    filters.append(f'min-beds={minbeds}')   if minbeds else None
    filters.append(f'max-beds={maxbeds}')   if maxbeds else None
    filters.append(f'min-baths={minbaths}') if minbaths else None
    url = f'{url}/filter/{",".join(filters)}' if filters else url

    print(f'the base url was generated with filtering statement: \n {url}')

    return url

# main

#filter
# url = gen_url(zip = 27695, 
#               type = ['house'], 
#               minprice = None, maxprice = 1100, 
#               minbeds = 2, maxbeds = None, minbaths = 2)

# driver = opendriver(False)
# soup = htmlsoup(url, driver)

#get the properties
properties = []
for i in range(5):
    property = soup.find_all('a', class_="slider-item")[i]['href']
    properties.append(property)
print('generating 5 properties...')

#get each infos
infos = []
for property in properties:
    print(f'navigating to ... {property}')
    # driver = opendriver(False)
    info = getinfo(property, driver)
    infos.append(info)

#take infos to df
df = pd.DataFrame(infos)
df[['price','beds','baths', 'sqf']] = df['key1'].apply(lambda x : pd.Series(x))

if len(df['key2'][0]) == 9:
    df[['daysonredfin','type','year','lotsize','ppsf','op1','op2','agentfee','city']] = df['key2'].apply(lambda x : pd.Series(x))

elif len(df['key2'][0]) == 8:
    df[['daysonredfin','type','year','ppsf','op1','op2','agentfee','city']] = df['key2'].apply(lambda x : pd.Series(x))

df.drop(columns = ['key1','key2'], inplace = True)

print('done')