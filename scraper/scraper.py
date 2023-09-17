#!/usr/bin/env python3
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BS
from config.config import Config
from time import localtime, strftime
from utils.utils import print_to_log

import json
import os
import pandas as pd
import pathlib
import re


def output_folder():
    unique_name_folder = strftime("%Y-%m-%d %H-%M-%S", localtime())
    output_folder = pathlib.Path('output').joinpath(unique_name_folder)
    if not output_folder.exists():
        print(f"The output files will be located in the folder : \"{str(output_folder)}\".")
        try:
            os.makedirs(output_folder)
        except OSError:
            raise

    return output_folder

def manual_search():
    msg = ('*** Single Search ***\n'
    'NOTE : An empty answer will return to the main menu.\n')
    print(msg)
    city = input("Which city? ").strip()
    if city == '':
        return 'main menu'
    state = input("Which state? ").strip()
    if state == '':
        return 'main menu'
    scraper = Scraper()
    scraper.fetch_sales_from(city, state, output_folder())
    return 'success'

def search_from_file():
    msg = ('*** Search From List ***\n'
           'NOTE : An empty answer will return to the main menu.\n')
    print(msg)
    input_file = input("Name of input file (must be in input folder)? : ").strip()

    if input_file == '':
        return 'main menu'

    try:
        with open(pathlib.Path('input', input_file), 'r') as location_list:
            scraper = Scraper()
            output_folder_path = output_folder()

            lines = location_list.readlines()
            line_no = 0
            pattern = re.compile("^[^,]*,[^,]*$")
            for line in lines:
                line_no += 1
                line = line.strip()

                if line == '' or line[0] == '#':
                    continue

                if not pattern.match(line):
                    msg = f"Input \"{line}\" on line {line_no} does not respect format : city, state"
                    print_to_log(output_folder_path, msg)
                    print(msg)
                    continue

                location = line.split(',')
                city = location[0].strip()
                state = location[1].strip()
                scraper.fetch_sales_from(city, state, output_folder_path)
    except IOError:
        print(f"Cannot find file named : {input_file}")

    return 'success'


class Scraper:

    def __init__(self):
        # Webdriver options
        self._firefox_options = Options()
        self._firefox_options.add_argument("-headless")
        self._firefox_options.page_load_strategy = "eager"

        # Scraper config
        self._GSF_URL = "https://garagesalefinder.com/yard-sales/"

        # User config
        self.config = Config()

    def fetch_sales_from(self, city, state, output_folder_path):
        location = city + ', ' + state
        msg = f'[{strftime("%H:%M:%S", localtime())}] STARTED Scraping for location : {location}'
        print(msg)
        print_to_log(output_folder_path, msg)

        with webdriver.Firefox(options=self._firefox_options) as driver:
            driver.get(self._GSF_URL)

            # Send location to search box
            try:
                element_located = EC.presence_of_element_located((By.NAME, "cityZipSearch"))
                searchbox = WebDriverWait(driver, 10).until(element_located)
                searchbox.send_keys(location)
                searchbox.send_keys(Keys.RETURN)
                time.sleep(5)
            except TimeoutError:
                msg = f"Timed out while waiting for page to load for location : {location}"
                print_to_log(output_folder_path, msg)
                print(msg)

            # Parse html
            soup = BS(driver.page_source.encode("utf-8"), "lxml")
            sales = soup.find_all("div", id=re.compile("record"))

            if not sales:
                msg = f"No search result for city: {city} ; state: {state}"
                print(msg)
                print_to_log(output_folder_path, msg)
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
            file_name = strftime("%Y-%m-%d %H-%M-%S", localtime()) + " " + location
            output_path = pathlib.PurePath(output_folder_path, pathlib.Path(file_name))
            if self.config.json['output_to_csv'].lower().strip() == "true":
                DF.to_csv(str(output_path) + '.csv')
            if self.config.json['output_to_json'].lower().strip() == "true":
                DF.to_json(str(output_path) + '.json')
            if self.config.json['output_to_excel'].lower().strip() == "true":
                DF.to_excel(str(output_path) + '.xlsx')

            msg = f'[{strftime("%H:%M:%S", localtime())}] COMPLETED Scraping for location : {location}'
            print(msg)
            print_to_log(output_folder_path, msg)
