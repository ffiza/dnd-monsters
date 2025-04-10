import pandas as pd
import numpy as np
import json

from config import Config

np.random.seed(42)


def generate_dummy_data(n_data: int) -> pd.DataFrame:
    CHALLENGE_RATINGS = ["0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5",
                         "6", "7", "8", "9", "10", "11", "12", "13", "14",
                         "15", "16", "17", "18", "19", "20", "21", "22", "23",
                         "24", "25", "26", "27", "28", "29", "30"]
    TYPES = ["Aberration", "Beast", "Celestial", "Construct", "Dragon",
             "Elemental", "Fey", "Fiend", "Giant", "Humanoid", "Monstrosity",
             "Ooze", "Plant", "Undead"]
    SIZES = ["Tiny", "Small", "Medium", "Large", "Huge", "Gargantuan"]
    ALIGNMENTS = ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE", "U"]

    df = pd.DataFrame({
        "Name": [f"Monster{i}" for i in range(n_data)],
        "ChallengeRating": np.random.choice(CHALLENGE_RATINGS, n_data),
        "Type": np.random.choice(TYPES, n_data),
        "Size": np.random.choice(SIZES, n_data),
        "Strength": np.random.randint(1, 21, n_data),
        "Dexterity": np.random.randint(1, 21, n_data),
        "Constitution": np.random.randint(1, 21, n_data),
        "Intelligence": np.random.randint(1, 21, n_data),
        "Wisdom": np.random.randint(1, 21, n_data),
        "Charisma": np.random.randint(1, 21, n_data),
        "Alignment": np.random.choice(ALIGNMENTS, n_data),
        "Speed": np.random.randint(20, 41, n_data),
        "SwimSpeed": np.random.randint(0, 41, n_data),
        "FlySpeed": np.random.randint(0, 41, n_data),
    })

    return df


def parse_speed_line(s: str) -> dict:
    """
    Parses the `Speed` string in a monster block.

    Parameters
    ----------
    s : str
        The `Speed` string of the monster block.

    Returns
    -------
    dict
        A dictionary with all the speeds of the monster.
    """
    data = {"walk": 0, "swim": 0, "fly": 0, "burrow": 0, "climb": 0}
    s_split = s.split(".")
    for e in s_split:
        if "ft" in e:
            if "swim" in e:
                data["swim"] = e.split(" ")[2]
            elif "fly" in e:
                data["fly"] = e.split(" ")[2]
            elif "burrow" in e:
                data["burrow"] = e.split(" ")[2]
            elif "climb" in e:
                data["climb"] = e.split(" ")[2]
            else:
                data["walk"] = e.split(" ")[0]
    return data


def parse_monster_block(block: dict) -> list:
    """
    Parses the monster block.

    Parameters
    ----------
    block : dict
        The block to parse.

    Returns
    -------
    list
        A list with relevant values.
    """
    speed_data = parse_speed_line(block["Speed"])
    if block["name"] == "Werebear":
        data = [block["name"],
                block["Challenge"].split(" (")[0],
                block["meta"].split(" ")[1].split(",")[0],
                block["meta"].split(" ")[0],
                int(block["STR"]),
                int(block["DEX"]),
                int(block["CON"]),
                int(block["INT"]),
                int(block["WIS"]),
                int(block["CHA"]),
                block["meta"].split(", ")[1],
                int(block["Speed"][8:10]),
                0,
                0,
                0,
                int(block["Speed"][22:24]),
                ]
    elif block["name"] == "Wereboar":
        data = [block["name"],
                block["Challenge"].split(" (")[0],
                block["meta"].split(" ")[1].split(",")[0],
                block["meta"].split(" ")[0],
                int(block["STR"]),
                int(block["DEX"]),
                int(block["CON"]),
                int(block["INT"]),
                int(block["WIS"]),
                int(block["CHA"]),
                block["meta"].split(", ")[1],
                int(block["Speed"][8:10]),
                0,
                0,
                0,
                0,
                ]
    elif block["name"] == "Weretiger":
        data = [block["name"],
                block["Challenge"].split(" (")[0],
                block["meta"].split(" ")[1].split(",")[0],
                block["meta"].split(" ")[0],
                int(block["STR"]),
                int(block["DEX"]),
                int(block["CON"]),
                int(block["INT"]),
                int(block["WIS"]),
                int(block["CHA"]),
                block["meta"].split(", ")[1],
                int(block["Speed"][8:10]),
                0,
                0,
                0,
                0,
                ]
    elif block["name"] == "Werewolf":
        data = [block["name"],
                block["Challenge"].split(" (")[0],
                block["meta"].split(" ")[1].split(",")[0],
                block["meta"].split(" ")[0],
                int(block["STR"]),
                int(block["DEX"]),
                int(block["CON"]),
                int(block["INT"]),
                int(block["WIS"]),
                int(block["CHA"]),
                block["meta"].split(", ")[1],
                int(block["Speed"][8:10]),
                0,
                0,
                0,
                0,
                ]
    else:
        data = [block["name"],
                block["Challenge"].split(" (")[0],
                block["meta"].split(" ")[1].split(",")[0],
                block["meta"].split(" ")[0],
                int(block["STR"]),
                int(block["DEX"]),
                int(block["CON"]),
                int(block["INT"]),
                int(block["WIS"]),
                int(block["CHA"]),
                block["meta"].split(", ")[1],
                int(speed_data["walk"]),
                int(speed_data["swim"]),
                int(speed_data["fly"]),
                int(speed_data["burrow"]),
                int(speed_data["climb"]),
                ]
    return data


def map_alignment(alignment):
    good_evil_map = {'good': 1, 'neutral': 0, 'evil': -1}
    lawful_chaotic_map = {'lawful': -1, 'neutral': 0, 'chaotic': 1}
    if alignment in ('any', 'unaligned'):
        return np.nan, np.nan
    parts = alignment.split()
    if len(parts) == 2:
        lc, eg = parts
    else:
        lc = eg = 'neutral'
    return good_evil_map[eg], lawful_chaotic_map[lc]


def process_data() -> None:
    """
    Reads the raw data and saves a new CSV file with the results of the
    processing.
    """
    with open('data/raw/srd_5e_monsters.json', 'r') as file:
        monsters = json.load(file)

    cols = ["Name", "ChallengeRating", "Type", "Size", "Strength", "Dexterity",
            "Constitution", "Intelligence", "Wisdom", "Charisma", "Alignment",
            "WalkSpeed", "SwimSpeed", "FlySpeed", "BurrowSpeed", "ClimbSpeed"]
    data = []
    for monster in monsters:
        data.append(parse_monster_block(monster))
    data = np.array(data)

    df = pd.DataFrame(data, columns=cols)
    df["Type"] = df["Type"].str.title()

    df.to_csv("data/processed/srd_5e_monsters.csv", index=False)


def read_data() -> pd.DataFrame:
    """
    Reads the processed data CSV and returns a data frame.

    Returns
    -------
    pd.DataFrame
        The processed data.
    """
    config = Config()
    df = pd.read_csv("data/processed/srd_5e_monsters.csv")

    def cr_to_int(cr: str) -> int:
        return config.CHALLENGE_RATINGS.index(cr)

    # Add aux data for plotting
    df["ChallengeRatingInt"] = df["ChallengeRating"].apply(cr_to_int)
    df[['Alignment_EG', 'Alignment_LC']] = df['Alignment'].apply(
        lambda x: pd.Series(map_alignment(x))
        )

    return df


if __name__ == "__main__":
    process_data()
