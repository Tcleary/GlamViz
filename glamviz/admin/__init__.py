import os
from flask import current_app

import glam_io

def get_repository_url():
    config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
    data = glam_io.read_json(config_filename)

    repository_url = ''

    if data:
        if data.get('repository'):
            repository_url = data.get('repository').get('url')

    return repository_url


def get_repository_label():
    config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
    data = glam_io.read_json(config_filename)

    repository_label = ''

    if data:
        if data.get('repository'):
            repository_label = data.get('repository').get('label')

    return repository_label


def get_repository_sets():
    config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
    data = glam_io.read_json(config_filename)

    repository_sets = ''

    if data:
        if data.get('repository'):
            repository_sets = data.get('repository').get('sets')

    return repository_sets
