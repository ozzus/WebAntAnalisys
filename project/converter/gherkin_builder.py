from typing import Dict

COMMAND_MAPPING = {
    "open": ("Given", "I open the URL '{target}'"),
    "type": ("When", "I enter '{value}' into the element '{target}'"),
    "click": ("And", "I click the element '{target}'"),
    "doubleClick": ("When", "I double click the element '{target}'"),
    "select": ("When", "I select option '{value}' in '{target}'"),
    "assertText": ("Then", "The element '{target}' should contain text '{value}'"),
    "assertTitle": ("Then", "The page title should be '{value}'")
}

def normalize_selector(selector: str) -> str:  # Перемещено выше build_gherkin
    """Нормализация селекторов для лучшей читаемости"""
    if "=" in selector:
        strategy, locator = selector.split("=", 1)
        strategy = strategy.lower()
        
        if strategy == "id":
            return f"#{locator}"
        elif strategy == "css":
            return locator
        elif strategy == "xpath":
            return f"xpath: {locator}"
    
    return selector

def build_gherkin(data: Dict) -> str:
    """Генерация Gherkin-кода из структурированных данных"""
    features = []
    
    for feature in data.get("features", []):
        feature_lines = [f"Feature: {feature['name']}"]
        
        for scenario_idx, scenario in enumerate(feature.get("scenarios", []), 1):
            scenario_lines = [f"  Scenario: {feature['name']} - {scenario_idx}"]
            
            for step in scenario.get("steps", []):
                command = step["command"]
                if command not in COMMAND_MAPPING:
                    continue  # Пропускаем неизвестные команды
                
                step_type, template = COMMAND_MAPPING[command]
                selector = normalize_selector(step["target"])
                formatted_value = step["value"].replace('"', '\\"')
                
                formatted_step = template.format(
                    target=selector,
                    value=formatted_value
                )
                scenario_lines.append(f"    {step_type} {formatted_step}")
            
            feature_lines.append("\n".join(scenario_lines))
        
        features.append("\n".join(feature_lines))
    
    return "\n\n".join(features)