import os
import random
import re

import pandas as pd
from accern_data.util import load_json, write_json


def combine_json(src_path: str, dest_path: str) -> None:
    full_json = {
        "start_harvested_at": "",
        "end_harvested_at": "",
        "start_published_at": "",
        "end_published_at": "",
        "total": 0,
        "overall_total": 0,
    }
    signals = []
    total = 0
    for filename in sorted(os.listdir(src_path)):
        print(os.path.join(src_path, filename))
        json_var = load_json(os.path.join(src_path, filename))
        signals.extend(json_var)
        total += len(json_var)
    full_json["signals"] = signals
    full_json["total"] = total
    full_json["overall_total"] = total
    write_json(full_json, os.path.join(dest_path, "data-2022.json"))


def shuffle_str(string: str, seed: int = 200) -> str:
    characters = list(string)
    random.seed(seed)
    random.shuffle(characters)
    return "".join(characters)


def url_sub(string: str, seed: int = 300) -> str:
    splits = string.split("/")
    splits[-2] = shuffle_str(splits[-2], seed)
    file_split = splits[-1].split(".")
    splits[-1] = f"{shuffle_str(file_split[0], seed)}.{file_split[1]}"
    url = "/".join(splits)
    return re.sub(r"www\.[a-z-]+\.(com|gov)", "www.dummy-url.com", url)


def event_text(string: str) -> str:  # pylint: disable=unused-argument
    return "[redacted]"


def truncate_precision(value: float, dps: int = 10) -> float:
    return float(f"{value:0.{dps}f}")


# Combined files
df = pd.read_csv("./tests/data/data-2022.csv")
df["doc_url"] = df["doc_url"].apply(url_sub)
df["event_text"] = df["event_text"].apply(event_text)
for col in {"event_sentiment", "signal_sentiment"}:
    df[col] = df[col].apply(truncate_precision)
df.to_csv("./tests/data/data-2022.csv", index=False)

json_obj = load_json("./tests/data/data-2022.json")
for rec in json_obj["signals"]:
    rec["doc_url"] = url_sub(rec["doc_url"])
    rec["event_text"] = event_text(rec["event_text"])
    for key in {"event_sentiment", "signal_sentiment"}:
        rec[key] = truncate_precision(rec[key])
write_json(json_obj, "./tests/data/data-2022.json")

# Separate Files
for file_name in os.listdir("./tests/data/csv_date/"):
    df = pd.read_csv(f"./tests/data/csv_date/{file_name}")
    df["doc_url"] = df["doc_url"].apply(url_sub)
    df["event_text"] = df["event_text"].apply(event_text)
    for col in {"event_sentiment", "signal_sentiment"}:
        df[col] = df[col].apply(truncate_precision)
    df.to_csv(f"./tests/data/csv_date/{file_name}", index=False)

for file in os.listdir("./tests/data/json/"):
    json_obj = load_json(f"./tests/data/json/{file}")
    for rec in json_obj:
        rec["doc_url"] = url_sub(rec["doc_url"])
        rec["event_text"] = event_text(rec["event_text"])
        for key in {"event_sentiment", "signal_sentiment"}:
            rec[key] = truncate_precision(rec[key])
    write_json(json_obj, f"./tests/data/json/{file}")
