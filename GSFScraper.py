#!/usr/bin/env python3

import argparse
from scraper.scraper import single_search, file_search
from UI import UI

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='GSFScraper.py',
        description=('For interactive mode, launch without any argument. '
                     'Arguments which have a space character in them need to be put between double quotation marks, e.g. "new york". '
                     'Files used in list mode must be located in the input folder'))
    scrape_method = parser.add_mutually_exclusive_group()
    scrape_method.add_argument('-s', '--single', nargs=2, metavar=('CITY', 'STATE'), action='store', type=str,
                               help='Scrape for the given location. Example: python3 GSFScraper.py -s "new york" "new york"')
    scrape_method.add_argument('-l', '--list', metavar='FILE_NAME', action='store', type=str,
                               help='Scrape all listed locations in the given file. Example: python3 GSFScraper.py -l example.txt')
    args = parser.parse_args()

    if args.single:
        city = args.single[0]
        state = args.single[1]
        single_search(city, state)

    elif args.list:
        file_search(args.list)

    else:
        main_menu = UI.MainMenu()
        main_menu.display()
