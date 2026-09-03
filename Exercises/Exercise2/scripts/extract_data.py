import json
import random
import time
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "pokedata"
POKEBELT_DIR = DATA_DIR / "pokebelt"
POKELIST_FILE = DATA_DIR / "pokelist.json"


def create_pokelist():
    url = "https://enwikipedia.org/wiki/List_of_generation_I_Pok%C3%A9mon"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="wikitable")

    names = []

    for row in table.find_all("tr")[1:]:
        links = row.find_all("a")

        for link in links:
            text = link.get_text(strip=True)

            if text and not text.isdigit():
                name = text.split(" (")[0].strip()
                names.append(name)
                break

    names = names[:151]

    pokelist = {
        str(index): name
        for index, name in enumerate(names, start=1)
    }

    with open(POKELIST_FILE, "w", encoding="utf-8") as file:
        json.dump(pokelist, file, indent=4)

    print("pokelist.json created!")


def catch_pokemons():
    with open(POKELIST_FILE, "r", encoding="utf-8") as file:
        pokelist = json.load(file)

    selected_numbers = random.sample(range(1, 152), 6)

    for number in selected_numbers:
        pokemon = pokelist[str(number)].lower()

        print(f"Catching {pokemon}...")

        time.sleep(2)

        url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}"

        response = requests.get(url)
        response.raise_for_status()

        pokemon_data = response.json()

        output_file = POKEBELT_DIR / f"{pokemon}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(pokemon_data, file, indent=4)


if __name__ == "__main__":
    create_pokelist()
    catch_pokemons()
