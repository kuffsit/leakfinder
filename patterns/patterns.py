import yaml
import os

def load_patterns(config_file="patterns.yaml"):
    config_path = os.path.join(os.path.dirname(__file__), "..", config_file)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            patterns = {}
            if isinstance(data, dict):
                for section in data.values():
                    if isinstance(section, dict):
                        patterns.update(section)
            return patterns
    except Exception as e:
        print(f"Ошибка загрузки паттернов из {config_file}: {e}")
        return {}

PATTERNS = load_patterns()
