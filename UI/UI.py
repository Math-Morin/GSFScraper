#!/usr/bin/env python3

from abc import ABC, abstractmethod
import math
import os
from scraper.scraper import manual_search, search_from_file


class UI(ABC):

    def __init__(self, title, options):
        self._title = title
        self._options = options
        self._menu = ""

    def display(self):
        status = 0
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            if status == 1:
                print('Last scraping session completed successfully. See log file for more info.')
                print()
            for line in self._menu:
                print(line)

            status = self._process_choice(input("Your choice? "))
            if status == 0:
                os.system('cls' if os.name == 'nt' else 'clear')
                return

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
            return 0
        elif choice == '1':
            print("help")
        elif choice == '2':
            return manual_search()
        elif choice == '3':
            return search_from_file()
        else:
            print("Invalid choice.")

