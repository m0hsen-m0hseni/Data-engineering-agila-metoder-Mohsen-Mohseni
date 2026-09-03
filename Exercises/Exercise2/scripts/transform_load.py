import json
from datetime import datetime
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent.parent
POKEBELT_DIR = BASE_DIR / "pokedata" / "pokebelt"
OBSERVATIONS_DIR = BASE_DIR / "pokedata" / "observations"


def transform():
    observations = []

    for json_file in POKEBELT_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        observations.append(
            {
                "pokemon": data["name"],
                "happiness": data["base_happiness"]
            }
        )

    return observations


def load(observations):
    timestamp = datetime.now().strftime("%y-%m-%d_%H_%M")

    output_file = (
        OBSERVATIONS_DIR /
        f"observation_{timestamp}.csv"
    )

    df = pd.DataFrame(observations)

    df.to_csv(output_file, index=False)

    print(f"Saved observations to {output_file}")


if __name__ == "__main__":
    observations = transform()
    load(observations)
