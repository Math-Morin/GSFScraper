#!/usr/bin/env python3

import json

class Config:

    def __init__(self):
        self.json = None
        self.get_user_config()

    def get_user_config(self):
        try:  # Get config from file
            with open('config.json', 'r') as config_file:
                # TODO verbose
                self.json = json.load(config_file)

        except IOError:
            print("Error: config.json not found. Generating a new file with default values.")
            try:  # Generate default config file
                with open('config.json', 'w+') as config_file:
                    config = {
                        'output_to_csv': 'False',
                        'output_to_excel': 'True',
                        'output_to_json': 'False'
                    }
                    json.dump(config, config_file, sort_keys=True, indent=4, ensure_ascii=False)

            except IOError:
                print("Error: could not generate default config file.")

            else:
                self.get_user_config()

    def set_user_config(self, new_config):
        try:
            with open('config.json', 'w+') as config_file:
                # TODO verbose, print changes
                json.dump(new_config, config_file, sort_keys=True, indent=4, ensure_ascii=False)
        except IOError:
            print("Error: config.json not found. Using default values.")
