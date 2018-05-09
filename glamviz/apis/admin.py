import os
from flask import request, current_app
from flask_restplus import Namespace, Resource, reqparse, fields

import glam_io
import harvester

api = Namespace('admin', description='configure data repository')

repository_admin_arguments = reqparse.RequestParser()
repository_admin_arguments.add_argument(
    'repository_label',
    type=str,
    required=True,
    help='Add repository label'
)

repository_admin_arguments.add_argument(
    'repository_url',
    type=str,
    required=True,
    help='Add repository URL'
)

repository_model = api.model('Repository', {
    'label': fields.String(required=True, description='Repository label'),
    'url': fields.String(required=True, description='Repository url'),
})

resource_fields = {}
resource_fields['set'] = {}
resource_fields['set']['setSpec'] = fields.String
resource_fields['set']['setName'] = fields.String

set_model = api.model('Set', {
    'setSpec': fields.String,
    'setName': fields.String,
})

repository_sets_model = api.model('RepositorySets',
    {'sets': fields.List(fields.Nested(set_model))}
)


@api.route('/Repository')
class AdminRepository(Resource):

    def get(self):

        app = current_app
        config_filename = os.path.join(app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename)

        if data is None:
            repository = 'No settings and respository configured'
        else:
            repository = data.get('repository') or 'No repository configured.'

        return repository

    @api.response(201, 'Repository successfully registered.')
    @api.expect(repository_model)
    def post(self):
        repository_data = request.json
        repository_sets = harvester.list_sets()
        repository_data['sets'] = repository_sets
        config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename) or {}



        repository_list = []
        if data:
            repository_list = data.get('repository_list')



        data['repository'] = repository_data

        # Add to repository list
        matching_labels = 0

        for repo in repository_list:
            if repo.get('label') == repository_data.get('label'):
                matching_labels = matching_labels + 1

        if matching_labels == 0:
            repository_list.append(repository_data)

        data['repository_list'] = repository_list

        glam_io.write_json(config_filename, data)

        return None, 201


@api.route('/RepositorySets')
class AdminRepositorySets(Resource):

    def get(self):

        app = current_app
        config_filename = os.path.join(app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename)

        if data is None:
            repository_sets = 'No settings and respository configured'
        else:
            repository_sets = data.get('repository').get('sets') or 'No repository configured.'

        return repository_sets

    @api.response(201, 'Repository sets successfully registered.')
    @api.expect(repository_sets_model)
    def post(self):
        repository_sets = request.json

        config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename) or {}
        if data:
            repository_data = data.get('repository')
            repository_data['sets'] = repository_sets.get('sets')
            data['repository'] = repository_data

        glam_io.write_json(config_filename, data)

        return None, 201


@api.route('/RepositoryList')
class AdminRepository(Resource):

    def get(self):

        app = current_app
        config_filename = os.path.join(app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename)

        if data is None:
            repository_list = 'No settings and respository_list configured'
        else:
            repository_list = data.get('repository_list') or 'No repository_list configured.'

        return repository_list