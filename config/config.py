#!/usr/bin/env python3

import json

DEFAULT_TO_CSV = 'true'
DEFAULT_TO_JSON = 'true'
DEFAULT_TO_EXCEL = 'true'
DEFAULT_LOAD_TIME_ALLOWED = 5


class Config:

    def __init__(self):
        self.json = None
        self.get_user_config()

    def get_user_config(self):
        try:  # Get config from file
            with open('config.json', 'r') as config_file:
                self.json = json.load(config_file)

        except IOError:
            print("Error: config.json not found. Generating a new file with default values.")
            try:  # Generate default config file
                with open('config.json', 'w+') as config_file:
                    config = {
                        'output to csv': DEFAULT_TO_CSV,
                        'output to json': DEFAULT_TO_JSON,
                        'output to excel': DEFAULT_TO_EXCEL,
                        'load time allowed': DEFAULT_LOAD_TIME_ALLOWED
                    }
                    json.dump(config, config_file, sort_keys=True, indent=4, ensure_ascii=False)

            except IOError:
                print("Error: could not generate default config file.")

            else:
                self.get_user_config()
