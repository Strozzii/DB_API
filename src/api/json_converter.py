"""Takes care of the export of data to JSON files."""

import json
import os

import pandas as pd

import src.api.constants as c
from src.api.datetime_handler import custom_json_encoder


def convert_list_to_json(data_list: list[dict], title: str):
    """Exports a JSON file from a list of dictionaries."""

    try:
        file_path = os.path.join(c.EXPORT_DIR, f"{title}.json")

        json_data = json.dumps(data_list, indent=c.JSON_INDENT, default=custom_json_encoder, ensure_ascii=False)

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)

    except (TypeError, ValueError) as e:
        print(e)


def dataframe_to_json(df: pd.DataFrame, title: str):
    """Exports a JSON file from a Pandas DataFrame."""

    try:
        json_data = df.to_json(orient='records', indent=c.JSON_INDENT)
        file_path = os.path.join(c.EXPORT_DIR, f"{title}.json")

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)

    except (TypeError, ValueError) as e:
        print(e)
