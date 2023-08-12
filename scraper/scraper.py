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
import os
import pandas as pd
import pathlib
import re
import requests
import time


class Scraper:

    def __init__(self):
        # Webdriver options
        self._firefox_options = Options()
        self._firefox_options.add_argument("-headless")
        self._firefox_options.page_load_strategy = "eager"

        # Scraper options
        self._GSF_URL = "https://garagesalefinder.com/yard-sales/"

        # Customizable config
        self.get_scraper_config()

    def get_scraper_config(self):
        try:  # Get config form file
            with open('config.json', 'r') as config_file:
                # TODO verbose
                config = json.load(config_file)
                self._output_folder_path = config['output_folder_path']
                self._output_to_csv = config['output_to_csv']
                self._output_to_json = config['output_to_json']

        except IOError:
            print("Error: config.json not found. Generating a new file with default values.")
            try:  # Generate default config file
                with open('config.json', 'w') as config_file:
                    config = {
                        'output_folder_path': 'output',
                        'output_to_csv': 'True',
                        'output_to_json': 'True'
                    }
                    json.dump(config, config_file, sort_keys=True, indent=4, ensure_ascii=False)

                # Set self to default values
                self._output_folder_path = ''
                self._output_to_csv = True
                self._output_to_json = True

            except IOError:
                print("Error: could not generate default config file.")

    def set_scraper_config(self, new_config):
        try:
            with open('config.json', 'rw') as config_file:
                # TODO verbose, print changes
                json.dump(new_config, config_file, sort_keys=True, indent=4, ensure_ascii=False)
        except IOError:
            print("Error: config.json not found. Using default values.")

    # def fetch_states() :

    #     with webdriver.Firefox(options=firefox_options) as driver :
    #         driver.get(GSF_URL)
    #         print(driver.page_source)

    def fetch_sales_from(self, city, state):
        location = city + ', ' + state

        path = pathlib.Path(self._output_folder_path)
        if not path.exists():
            a = "x"
            while a not in "yn":
                a = input(f"The \"{str(path)}\" directory does not exist. Create it (y/n)? ").strip().lower()

            if a == 'y':
                try:
                    os.makedirs(path)
                except OSError:
                    raise

            else:
                print("Output files will be created in local project folder.")
                path = ''

        with webdriver.Firefox(options=self._firefox_options) as driver:
            driver.get(self._GSF_URL)

            # Send location to search box
            searchbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "cityZipSearch")))
            searchbox.send_keys(location)
            searchbox.send_keys(Keys.RETURN)
            time.sleep(5)  # TODO find better way to handle load time

            # Parse html
            soup = BS(driver.page_source.encode("utf-8"), "lxml")
            sales = soup.find_all("div", id=re.compile("record"))

            if not sales:
                print(f"No search result for city: {city} ; state: {state}")
                return

            # Gather data
            data = []
            for sale in sales:
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
            path = pathlib.PurePath(path, pathlib.Path(file_name))
            DF.to_json(str(path) + '.json')
            DF.to_csv(str(path) + '.csv')
