from datetime import datetime


def convert_timestamp(value):
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d')  # Zeitstempel in 'yyyy-mm-dd' Format
    return value


def custom_json_encoder(obj):
    # Überprüfe, ob das Objekt ein Standard-Python-datetime-Objekt ist
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d')
    # Versuch, falls es ein nicht direkt erkennbarer Zeitstempel (z.B. Neo4j DateTime) ist
    try:
        return obj.isoformat()[:10]  # Versuch, mit isoformat() zu konvertieren und das Datum zu extrahieren
    except AttributeError:
        pass
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")