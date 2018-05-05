from flask import request, current_app
from flask_restplus import Namespace, Resource, reqparse, fields
import os

import glam_io

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

    @api.response(201, 'Category successfully created.')
    @api.expect(repository_model)
    def post(self):

        repository_data = request.json
        config_filename = os.path.join(current_app.instance_path, 'config', 'settings.json')
        data = glam_io.read_json(config_filename)

        data['repository'] = repository_data
        repository_list = data.get('repository_list') or []
        repository_list.append(repository_data)
        data['repository_list'] = repository_list

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