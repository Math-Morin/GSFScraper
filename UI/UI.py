#!/usr/bin/env python3

from abc import ABC, abstractmethod
import json
import math
from scraper.scraper import single_search, search_from_file


class UI(ABC):

    def __init__(self, title, options):
        self._title = title
        self._options = options
        self._menu = ""

    def display(self):
        for l in self._menu:
            print(l)

        self._process_choice(input("Your choice? "))

    def _build_menu(self):
        options = self._get_options()
        max_len = len(self._title)
        selectable_lines = []
        for k, v in options.items():
            option = f"({k}) {v}"
            new_len = len(option)
            if new_len > max_len:
                max_len = new_len
            selectable_lines.append(option)

        self._menu = [(max_len + 4) * '*']
        spaces_to_add = max_len - len(self._title)
        self._menu.append('* ' + math.floor(spaces_to_add / 2) * ' ' + self._title + math.ceil(spaces_to_add / 2) * ' ' + ' *')
        self._menu.append((max_len + 4) * '*')

        for s in selectable_lines:
            spaces_to_add = max_len - len(s)
            self._menu.append('* ' + s + spaces_to_add * ' ' + ' *')
        self._menu.append((max_len + 4) * '*')

    def _get_options(self):
        options = {}
        for i, s in enumerate(self._options):
            options[i] = s

        return options

    @abstractmethod
    def _process_choice(self, choice):
        pass


class MainMenu(UI):
    def __init__(self):
        title = "Garage Sales Finder Scraper"
        options = [
            "Quit",
            "Help",
            "Enter single location",
            "Multiple locations from file",
        ]
        super().__init__(title, options)
        self._build_menu()

    def _process_choice(self, choice):
        if choice == '0':
            return
        elif choice == '1':
            print("help")
        elif choice == '2':
            city = input("Which city? ")
            state = input("Which state? ")
            single_search(city, state)
        elif choice == '3':
            input_file = input("Name of input file (must be in input folder)? : ")
            search_from_file(input_file)
        else:
            print("Invalid choice.")

#
# class ConfigMenu(UI):
#
#     def _process_choice(self, choice):
#         pass
#
#     def __init__(self):
#         super().__init__()
#         self._title = "Configuration"
#         self._populate_selectables()
#         self._build_options()
#         self._build_menu()
#
#     def _populate_selectables(self):
#         try:  # Get config form file
#             with open('config.json', 'r') as config_file:
#                 # TODO verbose
#                 max_key_len = 0
#                 config = json.load(config_file)
#                 for k, v in config.items():
#                     selectable = f"{k} : {v}"
#                     pos = selectable.find(":")
#                     if pos > max_key_len:
#                         max_key_len = pos
#                     self.selectables.append(selectable)
#
#                 for i, s in enumerate(selectables):
#                     pos = s.find(":")
#                     if pos < max_key_len:
#                         self.selectables[i] = s[:pos] + (max_key_len - pos) * ' ' + s[pos:]
#
#
#         except IOError:
#             print("Error: config.json not found. Generating a new file with default values.")
#             try:  # Generate default config file
#                 with open('config.json', 'w') as config_file:
#                     config = {
#                         'output_folder_path': 'output',
#                         'output_to_csv': 'True',
#                         'output_to_json': 'False'
#                     }
#                     json.dump(config, config_file, sort_keys=True, indent=4, ensure_ascii=False)
#
#             except IOError:
#                 print("Error: could not generate default config file.")
#                 answer = input("Try again (y/n) ? ")
#                 if answer.strip().lower() == 'y':
#                     self._get_selectables()
