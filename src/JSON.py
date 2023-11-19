import json

def save_JSON(obj, name = 'untitled'):
    json_object = json.dumps(obj, indent=4)
    with open(f"{name}.json", "w") as f:
        f.write(json_object)
    return

def read_JSON(name = 'untitled'):
    with open(f"{name}.json", "r") as f:
        json_object = json.load(f)
    return json_object