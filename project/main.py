# project/converters/selenium_converter.py
import json

def parse_selenium_side(file_path: str):
    with open(file_path) as f:
        data = json.load(f)
    
    scenarios = []
    for test in data["tests"]:
        steps = []
        for cmd in test["commands"]:
            if cmd["command"] == "type":
                steps.append(("When", f'I enter "{cmd["value"]}" into "{cmd["target"]}"'))
            elif cmd["command"] == "click":
                steps.append(("When", f'I click on "{cmd["target"]}"'))
            elif cmd["command"] == "assertText":
                steps.append(("Then", f'I should see "{cmd["value"]}" in "{cmd["target"]}"'))
        scenarios.append({"name": test["name"], "steps": steps})
    return scenarios