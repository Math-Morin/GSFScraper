#!/usr/bin/env python3

import pathlib


def print_to_log(path, msg):
    try:
        with open(pathlib.Path(path, "log.txt"), 'a+') as log_file:
            log_file.write(msg + '\n')

    except IOError:
        print("Error: could not create or write log file.")
