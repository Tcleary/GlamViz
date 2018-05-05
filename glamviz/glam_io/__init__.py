import json
import os
import errno
import re

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def write_json(filepath, data):

    dir_name = os.path.dirname(filepath)
    make_sure_path_exists(dir_name)
    basename = os.path.basename(filepath)
    filename = re.sub(r'[\\/*?:"<>|]', "_", basename)

    try:
        with open('/'.join((dir_name, filename)), 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'

def read_json(filename):
    data = {}
    try:
        with open(filename, 'r') as infile:
            data = json.load(infile)
    except Exception as e:
        pass
        #return 'Error reading JSON file:', e
    return data

def append_json(filename, data):
    try:
        with open(filename, 'a+') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'