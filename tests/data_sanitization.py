import argparse
import os
import random
import re

import pandas as pd
from accern_data.util import load_json, write_json


def combine_json(src_path: str, dest_path: str, master_file: str) -> None:
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
        json_var = load_json(os.path.join(src_path, filename))
        signals.extend(json_var)
        total += len(json_var)
    full_json["signals"] = signals
    full_json["total"] = total
    full_json["overall_total"] = total
    write_json(full_json, os.path.join(dest_path, f"{master_file}.json"))


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


def redacted_text(string: str) -> str:  # pylint: disable=unused-argument
    return "[redacted]"


def truncate_precision(value: float, dps: int = 10) -> float:
    return float(f"{value:0.{dps}f}")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="accern_data", description="Accern feed API library")
    argparser.add_argument(
        "--directory",
        default="tests/data/",
        type=str,
        help=(
            "The location for the data directory with appropriate directory "
            "structure."))

    argparser.add_argument(
        "--master-file",
        type=str,
        help=(
            "The name for master data file. Should be same for both csv "
            "& json file."))
    args = argparser.parse_args()

    combine_json(
        os.path.join(args.directory, "json"), args.directory, args.master_file)

    # Combined files
    master_csv_file = os.path.join(args.directory, f"{args.master_file}.csv")
    df = pd.read_csv(master_csv_file)
    for col in {"doc_title", "doc_url", "event_text", "entity_text"}:
        df[col] = df[col].apply(redacted_text)
    for col in {"event_sentiment", "signal_sentiment"}:
        df[col] = df[col].apply(truncate_precision)
    df.to_csv(master_csv_file, index=False)

    master_json_file = os.path.join(args.directory, f"{args.master_file}.json")
    json_obj = load_json(master_json_file)
    for rec in json_obj["signals"]:
        for key in {"doc_title", "doc_url", "event_text", "entity_text"}:
            rec[key] = redacted_text(rec[key])
        for key in {"event_sentiment", "signal_sentiment"}:
            rec[key] = truncate_precision(rec[key])
    write_json(json_obj, master_json_file)

    # Separate Files
    csv_date_dir = os.path.join(args.directory, "csv_date")
    for file_name in os.listdir(csv_date_dir):
        file_dir = os.path.join(csv_date_dir, f"{file_name}")
        df = pd.read_csv(file_dir)
        for col in {"doc_title", "doc_url", "event_text", "entity_text"}:
            df[col] = df[col].apply(redacted_text)
        for col in {"event_sentiment", "signal_sentiment"}:
            df[col] = df[col].apply(truncate_precision)
        df.to_csv(file_dir, index=False)

    json_dir = os.path.join(args.directory, "json")
    for file in os.listdir(json_dir):
        file_dir = os.path.join(csv_date_dir, f"{file}")
        json_obj = load_json(file_dir)
        for rec in json_obj:
            for key in {"doc_title", "doc_url", "event_text", "entity_text"}:
                rec[key] = redacted_text(rec[key])
            for key in {"event_sentiment", "signal_sentiment"}:
                rec[key] = truncate_precision(rec[key])
        write_json(json_obj, file_dir)
