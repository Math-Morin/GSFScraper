#!/usr/bin/env python3

import json
import math
import pathlib
from scraper.scraper import Scraper

TITLE = "Garage Sales Finder Scraper"

class UI:

    def __init__(self):
        self._options = {
            '0' : "Help",
            '1' : "Select city from list",
            '2' : "Enter city name(s)",
            '3' : "Customize config",
        }
        self._NB_OPTIONS = len(self._options)
        self._main_menu = self.build_main_menu()


    def build_main_menu(self):
        options = []
        max_len = len(TITLE)
        for k,v in self._options.items():
            option = k + ' : ' + v
            new_len = len(option)
            if new_len > max_len:
                max_len = new_len
            options.append(option)

        menu = []
        menu.append((max_len+4) * '*')

        spaces_to_add = max_len - len(TITLE)
        menu.append('* ' + math.floor(spaces_to_add/2) * ' ' + TITLE + math.ceil(spaces_to_add/2) * ' ' + ' *')

        menu.append((max_len+4) * '*')
        for o in options:
            spaces_to_add = max_len - len(o)
            menu.append('* ' + o + spaces_to_add * ' ' + ' *')
        menu.append((max_len+4) * '*')

        return menu


    def customize_config(self):
        try: # Get config form file
            with open('config.json', 'r') as config_file:
                #TODO verbose
                print("Here is the actual configuration:\n")
                config = json.load(config_file)

                i = 0
                for k,v in config.items():
                    print(f"({i}) {k} : {v}")
                    i += 1

                print(f"({i}) Return to main menu")
                choice = input("Your choice? ")



        except IOError:
            print("Error: config.json not found. Generating a new file with default values.")
            try: # Generate default config file
                with open('config.json', 'w') as config_file:
                    config = {
                        'output_folder_path' : 'output',
                        'output_to_csv'      : 'True',
                        'output_to_json'     : 'True'
                    }
                    json.dump(config, config_file, sort_keys=True, indent=4, ensure_ascii=False)

            except IOError:
                print("Error: could not generate default config file.")
                answer = input("Try again (y/n) ? ")
                if answer.strip().lower() == 'y':
                    self.customize_config()



    def main_menu(self):
        for l in self._main_menu:
            print(l)

        choice = input("Your choice? ")

        if choice == '0':
            print(0)
        elif choice == '1':
            print(1)
        elif choice == '2':
            city = input("Which city? ")
            state = input("Which state? ")
            scraper = Scraper()
            scraper.fetch_sales_from(city, state)
        elif choice == '3':
            self.customize_config()
        else:
            print(4)
