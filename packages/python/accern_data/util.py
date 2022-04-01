import io
import pandas as pd
from requests import Response

EXAMPLE_URL = "http://api.example.com/"


def is_example_url(url: str) -> bool:
    return url.startswith(EXAMPLE_URL)


def get_file_name(filename: str) -> str:
    if filename.endswith(".csv"):
        return f"tests/examples/csv/{filename}"
    if filename.endswith(".json"):
        return f"tests/examples/json/{filename}"
    raise ValueError("Invalid file extension.")


def generate_file_response(
        filepath: str,
        date: str,
        harvested_after: str,
        encoding: str = "utf-8") -> Response:
    response_obj = Response()
    df = pd.read_csv("tests/examples/data-2022.csv")
    df["harvested_at"] = pd.to_datetime(df["harvested_at"])
    df["published_at"] = pd.to_datetime(df["published_at"])

    filtered = df[
        (df["published_at"] == pd.to_datetime(date, utc=True)) &
        (df["harvested_at"] > pd.to_datetime(harvested_after, utc=True))
    ]
    print("filtered", len(filtered), date, harvested_after)
    obj = io.BytesIO()
    filtered.to_csv(obj, index=False)
    obj.seek(0)

    response_obj._content = obj.read(-1)  # or readall?
    response_obj.encoding = encoding
    response_obj.status_code = 200
    response_obj.url = filepath
    return response_obj
