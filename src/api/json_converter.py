import json

import src.api.constants as c


def convert_list_to_json(data_list: list[dict], title: str):
    try:
        file_path = f"E:\\DB_API\\src\\frontend\\export\\{title}.json"
        json_data = json.dumps(data_list, indent=c.JSON_INDENT)

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
