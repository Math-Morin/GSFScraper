#!/usr/bin/env python3

from abc import ABC, abstractmethod
import json
import math
import pathlib
from scraper.scraper import Scraper


class UI(ABC):

    def __init__(self):
        self._options = {}
        self._title = ""
        self._menu = ""
        self._selectables = []

    def _build(self):
        options = []
        max_len = len(self._title)
        for k, v in self._options.items():
            option = f"({k}) {v}"
            new_len = len(option)
            if new_len > max_len:
                max_len = new_len
            options.append(option)

        menu = [(max_len + 4) * '*']
        spaces_to_add = max_len - len(self._title)
        menu.append(
            '* ' + math.floor(spaces_to_add / 2) * ' ' + self._title + math.ceil(spaces_to_add / 2) * ' ' + ' *')

        menu.append((max_len + 4) * '*')
        for o in options:
            spaces_to_add = max_len - len(o)
            menu.append('* ' + o + spaces_to_add * ' ' + ' *')
        menu.append((max_len + 4) * '*')

        return menu

    def display(self):
        for l in self._menu:
            print(l)

        self._process_choice(input("Your choice? "))

    def _build_options(self):
        options = {}
        i = 0
        for s in self._selectables:
            options[i] = s
            i += 1
        return options

    @abstractmethod
    def _process_choice(self, choice):
        pass


class MainMenu(UI):
    def __init__(self):
        super().__init__()
        self._title = "Garage Sales Finder Scraper"
        self._selectables = [
            "Help",
            "Enter single location",
            "Customize config",
        ]
        self._options = self._build_options()
        self._menu = self._build()

    def _process_choice(self, choice):
        if choice == '0':
            print(0)
        elif choice == '1':
            city = input("Which city? ")
            state = input("Which state? ")
            scraper = Scraper()
            scraper.fetch_sales_from(city, state)
        elif choice == '2':
            ConfigMenu().display()
        else:
            print("Invalid choice.")


class ConfigMenu(UI):

    def _process_choice(self, choice):
        pass

    def __init__(self):
        super().__init__()
        self._selectables = self._get_selectables()
        self._options = self._build_options()
        self._title = "Configuration"
        self._menu = self._build()

    def _get_selectables(self):
        try:  # Get config form file
            with open('config.json', 'r') as config_file:
                # TODO verbose
                selectables = []
                max_key_len = 0
                config = json.load(config_file)
                for k, v in config.items():
                    selectable = f"{k} : {v}"
                    pos = selectable.find(":")
                    if pos > max_key_len:
                        max_key_len = pos
                    selectables.append(selectable)

                for i, s in enumerate(selectables):
                    pos = s.find(":")
                    if pos < max_key_len:
                        selectables[i] = s[:pos] + (max_key_len - pos) * ' ' + s[pos:]

                return selectables

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

            except IOError:
                print("Error: could not generate default config file.")
                answer = input("Try again (y/n) ? ")
                if answer.strip().lower() == 'y':
                    self._get_selectables()
