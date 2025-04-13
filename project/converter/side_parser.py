import json
from typing import Dict, List


def parse_side_file(file_path: str) -> Dict:
    """Парсинг .side файла и преобразование в унифицированный формат"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            "features": [{
                "name": test["name"],
                "scenarios": [{
                    "steps": [
                        {
                            "command": cmd["command"],
                            "target": cmd["target"],
                            "value": cmd.get("value", "")
                        } for cmd in test.get("commands", [])
                    ]
                }]  # Сценарий формируется из команд текущего теста
            } for test in data.get("tests", [])]  # Цикл по тестам для создания features
        }

    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Invalid .side file: {str(e)}")
