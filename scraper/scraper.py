#!/usr/bin/env python3
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as BS
from config.config import Config, DEFAULT_TO_CSV, DEFAULT_TO_JSON, DEFAULT_TO_EXCEL, DEFAULT_LOAD_TIME_ALLOWED
from time import localtime, strftime
from utils.utils import print_to_log

import json
import os
import pandas as pd
import pathlib
import re


def output_folder():
    unique_name_folder = strftime("%Y-%m-%d %H-%M-%S", localtime())
    folder_path = pathlib.Path('output').joinpath(unique_name_folder)
    if not folder_path.exists():
        print(f"The output files will be located in the folder : \"{str(folder_path)}\".")
        try:
            os.makedirs(folder_path)
        except OSError:
            raise

    return folder_path


def single_search(city, state):
    scraper = Scraper()
    return scraper.fetch_sales_from(city, state)


def file_search(input_file):
    try:
        with open(pathlib.Path('input', input_file), 'r') as location_list:
            scraper = Scraper()
            output_folder_path = output_folder()

            lines = location_list.readlines()
            line_no = 0
            pattern = re.compile("^[^,]*,[^,]*$")
            for line in lines:
                line_no += 1

                if '#' in line:
                    line = line.split('#')[0]
                line = line.strip()

                if line == '':
                    continue

                if not pattern.match(line):
                    msg = (f"Input \"{line}\" on line {line_no}"
                           f"does not respect format : city, state. It has been skipped.")
                    print_to_log(output_folder_path, msg)
                    print(msg)
                    continue

                location = line.split(',')
                city = location[0].strip()
                state = location[1].strip()
                scraper.fetch_sales_from(city, state)
    except IOError:
        print(f"Cannot find file named : {input_file}")
        return 'failed'

    return 'success'


def menu_single_search():
    msg = ('*** Single Search ***\n'
           'NOTE : An empty answer will return to the main menu.\n')
    print(msg)
    city = input("Which city? : ").strip()
    if city == '':
        return 'main menu'
    state = input("Which state? : ").strip()
    if state == '':
        return 'main menu'
    return single_search(city, state)


def menu_search_from_file():
    msg = ('*** Search From List ***\n'
           'NOTE : An empty answer will return to the main menu.\n')
    print(msg)
    input_file = input("Name of input file? (must be in input folder) : ").strip()

    if input_file == '':
        return 'main menu'

    return file_search(input_file)


class Scraper:

    def __init__(self):
        # Webdriver options
        self._firefox_options = Options()
        self._firefox_options.add_argument("-headless")
        self._firefox_options.page_load_strategy = "eager"

        # Scraper config
        self._GSF_URL = "https://garagesalefinder.com/yard-sales/"
        self.output_folder_path = output_folder()

        # User config
        self.to_csv = DEFAULT_TO_CSV
        self.to_json = DEFAULT_TO_JSON
        self.to_excel = DEFAULT_TO_EXCEL
        self.sleeptime = DEFAULT_LOAD_TIME_ALLOWED
        self.get_config()

    def get_config(self):
        config = Config()
        key = ''

        def get_bool_value(k, default_value):
            val_in = config.json[k]
            val_out = val_in.lower().strip() if type(val_in) is str else None
            val_out = True if val_out == 'true' else False if val_out == 'false' else None
            if val_out is None:
                raise ValueError(f"Error in config.json: value '{val_in}' of key '{k}' is invalid. "
                                 f"Must be either 'true' or 'false'. Using default value of {default_value}.")
            return val_out

        try:
            key = 'output to csv'
            self.to_csv = get_bool_value(key, DEFAULT_TO_CSV)
        except KeyError:
            msg = f"Error in config.json: key '{key}' not found. Using default value of '{self.to_csv}.'"
            print(msg)
            print_to_log(self.output_folder_path, msg)
        except ValueError as valerr:
            print(valerr)
            print_to_log(self.output_folder_path, repr(valerr))

        try:
            key = 'output to json'
            self.to_json = get_bool_value(key, DEFAULT_TO_JSON)
        except KeyError:
            msg = f"Error in config.json: key '{key}' not found. Using default value of '{self.to_json}.'"
            print(msg)
            print_to_log(self.output_folder_path, msg)
        except ValueError as valerr:
            print(valerr)
            print_to_log(self.output_folder_path, repr(valerr))

        try:
            key = 'output to excel'
            self.to_excel = get_bool_value(key, DEFAULT_TO_EXCEL)
        except KeyError:
            msg = f"Error in config.json: key '{key}' not found. Using default value of '{self.to_excel}.'"
            print(msg)
            print_to_log(self.output_folder_path, msg)
        except ValueError as valerr:
            print(valerr)
            print_to_log(self.output_folder_path, repr(valerr))

        try:
            key = 'load time allowed'
            value = config.json[key]
            if type(value) is not int:
                raise ValueError(f"Error in config.json: value '{value}' of key '{key}' is invalid. "
                                 f"Must be a number. Using default value of {self.sleeptime}.")
            self.sleeptime = value
        except KeyError:
            msg = f"Error in config.json: key '{key}' not found. Using default value of '{self.sleeptime}.'"
            print(msg)
            print_to_log(self.output_folder_path, msg)
        except ValueError as valerr:
            print(valerr)
            print_to_log(self.output_folder_path, repr(valerr))

        msg = "Files that will be generated :"
        msg += " .csv" if self.to_csv else ""
        msg += " .json" if self.to_json else ""
        msg += " .xlsx" if self.to_excel else ""
        print(msg)

    def fetch_sales_from(self, city, state):
        location = city + ', ' + state
        msg = f'[{strftime("%H:%M:%S", localtime())}] STARTED Scraping for location : {location}'
        print(msg)
        print_to_log(self.output_folder_path, msg)

        with webdriver.Firefox(options=self._firefox_options) as driver:
            driver.get(self._GSF_URL)

            # Send location to search box
            try:
                element_located = EC.presence_of_element_located((By.NAME, "cityZipSearch"))
                searchbox = WebDriverWait(driver, 10).until(element_located)
                searchbox.send_keys(location)
                searchbox.send_keys(Keys.RETURN)
                time.sleep(self.sleeptime)
            except TimeoutError:
                msg = f"Timed out while waiting for page to load for location : {location}"
                print_to_log(self.output_folder_path, msg)
                print(msg)

            # Parse html
            soup = BS(driver.page_source.encode("utf-8"), "lxml")
            sales = soup.find_all("div", id=re.compile("record"))

            if not sales:
                msg = f"No search result for city: {city} ; state: {state}"
                print(msg)
                print_to_log(self.output_folder_path, msg)
                return 'no result'

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
            output_path = pathlib.PurePath(self.output_folder_path, pathlib.Path(file_name))

            if self.to_csv:
                DF.to_csv(str(output_path) + '.csv')
            if self.to_json:
                DF.to_json(str(output_path) + '.json')
            if self.to_excel:
                DF.to_excel(str(output_path) + '.xlsx')

            msg = f'[{strftime("%H:%M:%S", localtime())}] COMPLETED Scraping for location : {location}'
            print(msg)
            print_to_log(self.output_folder_path, msg)

            return 'success'
