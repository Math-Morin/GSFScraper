#!/usr/bin/env python3
import sys
from scraper.scraper import Scraper
from UI import UI



#TODO: use argsparse library
#TODO: ajout options: Path to driver, path to output, retirer doublons toggle,
#TODO: short/long desc

if __name__ == "__main__":
    main_menu = UI.MainMenu()
    main_menu.display()
