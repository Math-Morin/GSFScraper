#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BS
import requests
import time
import json
import re


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

        searchbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cityZipSearch")))
        print(searchbox.get_attribute("name"))

        searchbox.send_keys(location)
        searchbox.send_keys(Keys.RETURN)
        time.sleep(5)

        soup = BS(driver.page_source.encode("utf-8"), "lxml")
        sales = soup.find_all("div", id=re.compile("record"))
        for sale in sales :
            attrs = sale.attrs
            i = attrs["data-iteration"]
            id = attrs["id"]
            data_sale = json.loads(attrs["data-sale"])
            lon = data_sale["lon"]
            lat = data_sale["lat"]

            print(i)
            print(id)
            print(lon)
            print(lat)

            break


    # with webdriver.Firefox(options=firefox_options) as driver :
    #     driver.get(GSF_URL + city + '-' + state)
    #     print(driver.page_source)


if __name__ == "__main__" :
    fetch_sales_from("new york", "ny")
