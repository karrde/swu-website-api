#!/usr/bin/env python3
import swuapi
import json
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    card_table = swuapi.CardTable()
    card_table.load()
    sets = card_table.sets()
    for id in sets:
        print(f"{id}:\t{sets[id]['name']}\t{sets[id]['code']}")

if __name__ == "__main__":
    main()