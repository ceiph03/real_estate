import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# # Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode
chrome_options.add_argument("--window-size=1920x1080")  # Set window size for headless mode
chrome_options.add_argument("--disable-dev-shm-usage")  # Fixes issues with /dev/shm

# Set a User-Agent header to mimic a legitimate browser request
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)

def htmlsoup(url):

    # Use Selenium to open the page and let JavaScript render it
    driver = webdriver.Chrome(executable_path = '/Users/dolee/repo/chromedriver/chromedriver', options = chrome_options)  # You need to have ChromeDriver installed and in your PATH
    driver.get(url)

    # Get the page source after JavaScript rendering
    page_source = driver.page_source

    # Close the Selenium browser
    driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Now you can use BeautifulSoup as usual
    # For example: soup.find('a'), soup.find_all('a'), etc.

    return soup

# Example usage:
zip_code = "95136"
url = f'https:\\www.redfin.com/zipcode/{zip_code}'
soup = htmlsoup(url)

properties = []
for i in range(5):
    property = soup.find_all('a',class_="slider-item")[i]['href']
    properties.append(property)

# Step 1: Perform a search
search_result = search_redfin(zip_code)

if search_result:
    # Step 2: Extract details from the first property (assuming there are results)
    soup = BeautifulSoup(search_result, 'html.parser')
    first_property_link = soup.find('a', class_="slider-item")['href']
    property_url = f"https://www.redfin.com{first_property_link}"
    
    # Step 3: Get details from the property page
    property_details = get_property_details(property_url)

    # Add your code to extract and print specific details from property_details

    # For demonstration purposes, let's print the HTML content of the property page
    print(property_details.prettify())