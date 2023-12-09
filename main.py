import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd
import cufflinks as cf
import datetime
import requests
from bs4 import BeautifulSoup

# App title
st.markdown('''
# Real estate profit estimator
- Built in `Python` using `streamlit`,`yfinance`, `cufflinks`, `pandas` and `datetime`
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
zipcode = st.sidebar.text_input("zipcode", 95136)
st.sidebar.button('find info..')


# redfin function
def get_redfin_info(address):
    url = f"https://www.redfin.com/zipcode/{zipcode}"
    
    # Make a request to the Redfin autocomplete API
    response = requests.get(url)
    data = response.json()

    if "payload" in data and "exactMatch" in data["payload"]:
        property_url = data["payload"]["exactMatch"]["url"]

        # Make a request to the property details page
        property_response = requests.get(property_url)
        property_soup = BeautifulSoup(property_response.content, "html.parser")

        # Extract information (replace with actual HTML tags and structure)
        price = property_soup.find("span", class_="price").text
        mortgage = property_soup.find("span", class_="mortgage").text
        rental_income = property_soup.find("span", class_="rental-income").text

        return {
            "price": price,
            "mortgage": mortgage,
            "rental_income": rental_income
        }
    else:
        return None

# Example usage
zipcode = 95136
info = get_redfin_info(zipcode)

if info:
    print("Property Price:", info["price"])
    print("Monthly Mortgage:", info["mortgage"])
    print("Rental Income:", info["rental_income"])
else:
    print("Property information not found.")



# Ticker data
st.header('**Ticker data**')
st.write(tickerDf)

# Create a layout with two columns
col1, col2 = st.columns([2, 1])

# Create a checkbox for toggling Bollinger Bands
bollinger_days = col1.selectbox('Period', [20,40,60,120])
add_bollinger_button = col2.button('Add Bollinger Bands')

fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)

