#!/usr/bin/env python3
import sys
import scraper

NB_OPTS = 3
intro_menu = """
    *******************************
    * Garage Sales Finder Scraper *
    *******************************
    * 0 : Display help text       *
    * 1 : Select city from list   *
    * 2 : Enter city name         *
    *******************************
    Note that you can skip this selection step by giving your selection as an argument to GSFScraper.py
    Ex.: python3 GSFScraper 2 "New York" "2023-12-31"
    """

def main(argv) :
    #TODO: use argsparse library
    #TODO: ajout options: Path to driver
    if len(argv) <= 1 or argv[1] not in range(0, NB_OPTS):
        print(intro_menu)

    choice = input("""Please select an option from above.""")
    if choice == "0" :
        print(0)
    elif choice == "1" :
        scraper.fetch_states()
    else :
        print("default")

if __name__ == "__main__" :
    main(sys.argv)
