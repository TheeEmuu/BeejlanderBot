import requests
import json
import random
import sqlite3

def _connect():
    conn = sqlite3.connect('cards.db')
    return conn

def get_bulk_data():
    url = "https://api.scryfall.com/bulk-data"
    r = requests.get(url)
    data = json.loads(r.text)

    for x in data["data"]:
        if x["name"] == "Default Cards":
            r = requests.get(x["download_uri"])
            ret = json.loads(r.text)
            return ret

def update_db():
    conn = _connect()

    conn.execute("DELETE FROM Cards")

    fails = 0
    for x in get_bulk_data():
        excluded_cards = ["island", "plains", "forest", "swamp", "mountain"]
        excluded_set_types = ["alchemy", "masterpiece", "vanguard", "token", "memorabilia"]
        if (x["legalities"]["vintage"] != "not_legal" or x["border_color"] == "silver") and (not "token" in x["layout"] and (not (x["name"].lower() in excluded_cards)) and not(x["set_type"].lower() in excluded_set_types)):
            try:
                sql = ("INSERT OR REPLACE INTO Cards ("
                    "name,"
                    "isLegalStandard,"
                    "isLegalPioneer,"
                    "isLegalModern,"
                    "isLegalPauper,"
                    "isLegalPenny,"
                    "isLegalLegacy,"
                    "rarity,"
                    "priceUsd,"
                    "priceEur,"
                    "priceTix"
                    ")"
                    " VALUES ("
                    '\"{name}\",'
                    '{isLegalStandard},'
                    '{isLegalPioneer},'
                    '{isLegalModern},'
                    '{isLegalPauper},'
                    '{isLegalPenny},'
                    '{isLegalLegacy},'
                    '\"{rarity}\",'
                    '{priceUsd},'
                    '{priceEur},'
                    '{priceTix})'
                ).format(
                    name = x["name"].replace("\"", "\"\""),
                    isLegalStandard = x["legalities"]["standard"] == "legal",
                    isLegalPioneer = x["legalities"]["pioneer"] == "legal",
                    isLegalModern = x["legalities"]["modern"] == "legal",
                    isLegalPauper = x["legalities"]["pauper"] == "legal",
                    isLegalPenny = x["legalities"]["penny"] == "legal",
                    isLegalLegacy = x["legalities"]["legacy"] == "legal",
                    rarity = x["rarity"],
                    priceUsd = x["prices"]["usd"] or "NULL",
                    priceEur = x["prices"]["eur"] or "NULL",
                    priceTix = x["prices"]["tix"] or "NULL",
                )
                conn.execute(sql)
            except:
                print(x["name"] + " failed")
                fails+=1
    conn.commit()
    print(fails)

def get_list(query = None):
    conn = _connect()
    ret = ""
    if query is None:
        sql = "SELECT name FROM Cards GROUP BY name ORDER BY RANDOM() LIMIT 1"
    else:
        sql = "SELECT name FROM Cards WHERE (" + query + ") GROUP BY name ORDER BY RANDOM() LIMIT 1"
    for i in range (100):
        cursor = conn.execute(sql)
        for row in cursor:
            ret += str(row[0]) + "\n"
    return ret

def get_beej_list():
    conn = _connect()
    ret = ""
    