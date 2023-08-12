#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BS
from datetime import datetime
import json
import pandas as pd
import re
import requests
import time


GSF_URL = "https://garagesalefinder.com/yard-sales/"

firefox_options = Options()
firefox_options.add_argument("-headless")
firefox_options.page_load_strategy = "eager"


def fetch_states() :

    with webdriver.Firefox(options=firefox_options) as driver :
        driver.get(GSF_URL)
        print(driver.page_source)

def fetch_sales_from(city, state) :
    location = city + ', ' + state

    with webdriver.Firefox(options=firefox_options) as driver :
        driver.get(GSF_URL)

        # Send location to search box
        searchbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cityZipSearch")))
        searchbox.send_keys(location)
        searchbox.send_keys(Keys.RETURN)
        time.sleep(5) #TODO find better way to handle load time

        # Parse html
        soup = BS(driver.page_source.encode("utf-8"), "lxml")
        sales = soup.find_all("div", id=re.compile("record"))

        # Gather data
        data = []
        for sale in sales :
            data_sale = json.loads(sale.attrs["data-sale"])

            sale_id = data_sale["id"]
            address = sale.find("div", class_="sale-address").text.strip()
            lat = data_sale["lat"]
            lon = data_sale["lon"]
            sale_date = sale.find("div", class_="sale-date")
            date_from = sale_date["data-date-from"]
            date_to = sale_date["data-date-to"]
            title = sale.find("div", class_="sale-title").text.strip()
            desc = sale.find("div", class_="sale-desc").text.strip()

            data.append([sale_id, address, lat, lon, date_from, date_to, title, desc])

        # Build dataframe
        DF = pd.DataFrame(data)
        DF.columns = ['sale-id', 'address', 'lat', 'lon', 'date-from', 'date-to', 'title', 'desc']

        # Print to files
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + " " + location
        DF.to_json(file_name + '.json')
        DF.to_csv(file_name + '.csv')


# if __name__ == "__main__" :
#     fetch_sales_from("new york", "ny")
