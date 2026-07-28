import os 
import yaml

# For much later

def grid_patterns(pattern : str):
    file_path = os.path.dirname(__file__)
    file_path = os.path.join(file_path, "grid_patterns.yaml")
    
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    
    if pattern in data:
        return data[pattern]
    
    else:
        print("Pattern not found, using default")
        return data["default"]
        