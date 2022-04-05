import io
import json
from typing import Any
import pandas as pd
from requests import Response

EXAMPLE_URL = "http://api.example.com/"


def is_example_url(url: str) -> bool:
    return url == EXAMPLE_URL


def load_json(path: str) -> Any:
    with open(path, "r") as file:
        json_obj = json.load(file)
    return json_obj


def write_json(obj: object, path: str, **kwargs: Any) -> None:
    with open(path, "w") as file:
        json.dump(obj, file, indent=4, **kwargs)


def generate_file_response(
        date: str,
        harvested_after: str,
        mode: str,
        encoding: str = "utf-8") -> Response:
    response_obj = Response()
    date_dt = pd.to_datetime(date, utc=True)
    harvested_after_dt = pd.to_datetime(harvested_after, utc=True)
    if mode == "csv":
        df = pd.read_csv("tests/data/data-2022.csv")
        df["harvested_at"] = pd.to_datetime(df["harvested_at"])
        df["published_at"] = pd.to_datetime(df["published_at"])

        filtered = df[
            (df["published_at"] == date_dt) &
            (df["harvested_at"] > harvested_after_dt)
        ]
        obj = io.BytesIO()
        filtered.to_csv(obj, index=False)
    else:
        json_obj = load_json("tests/data/data-2022.json")
        filtered = {
            key: val
            for key, val in json_obj.items()
            if key != "signals"
        }
        filtered["signals"] = []
        for record in json_obj["signals"]:
            if (
                    pd.to_datetime(record["published_at"]) == date_dt
                    and
                    pd.to_datetime(record["harvested_at"]) > harvested_after_dt
                    ):
                filtered["signals"].append(record)
        obj = io.BytesIO(json.dumps(filtered).encode(encoding))
    obj.seek(0)
    response_obj._content = obj.read(-1)  # or readall?
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = f"tests/data/data-2022.{mode}"
    return response_obj
