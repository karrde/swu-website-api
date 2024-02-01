#!/usr/bin/env python3
import swuapi
import json
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def main():
    card_table = swuapi.CardTable()
    card_table.load()
    traits = card_table.traits()
    spacer = " "*36
    print(f"ID\tName{spacer}\tDescription")
    for id in traits:
        print(f"{id}:\t{traits[id]['name']:40}\t{traits[id]['description']}")

if __name__ == "__main__":
    main()