import json


def write_json(filename, data):
    try:
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'


def append_json(filename, data):
    try:
        with open(filename, 'a+') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'