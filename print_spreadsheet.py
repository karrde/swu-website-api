#!/usr/bin/env python3
import swuapi
import json
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    card_table = swuapi.CardTable()
    card_table.load()
    card_table.spreadsheet()

if __name__ == "__main__":
    main()