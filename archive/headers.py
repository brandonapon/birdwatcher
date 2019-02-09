#!/usr/bin/env python3

import os, os.path

def init():
    global CSV_PATH
    CSV_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..","..","api/bird_unofficial_api/csv_output.csv")
    IMG_PATH = None
    LOG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..","..")
