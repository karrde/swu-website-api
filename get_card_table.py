#!/usr/bin/env python3
import swuapi



def main():
    card_table = swuapi.CardTable()
    card_table.load()
    card_table.update()
    card_table.save()

if __name__ == "__main__":
    main()