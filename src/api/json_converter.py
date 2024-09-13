from datetime import datetime
import json

import src.api.constants as c
from src.api.datetime_handler import custom_json_encoder


def convert_list_to_json(data_list: list[dict], title: str):
    try:
        file_path = f"E:\\DB_API\\src\\frontend\\export\\{title}.json"

        # Verwende json.dumps mit dem benutzerdefinierten Encoder
        json_data = json.dumps(data_list, indent=4, default=custom_json_encoder, ensure_ascii=False)

        # Schreibe die JSON-Daten in die Datei
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)

    except (TypeError, ValueError) as e:
        print(e)


def dataframe_to_json(df, title: str):
    try:
        json_data = df.to_json(orient='records', indent=c.JSON_INDENT)
        file_path = f"E:\\DB_API\\src\\frontend\\export\\{title}.json"

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(json_data)

    except (TypeError, ValueError) as e:
        print(e)
