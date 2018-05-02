from flask_restplus import Namespace, Resource, reqparse
from flask_restplus import abort
from flask import request

import config
import glam_io
import transformer

api = Namespace('transform', description='transform data for use in visualizations')

transform_arguments = reqparse.RequestParser()

transform_arguments.add_argument(
    'repository_label',
    type=str,
    required=True,
    choices=tuple(config.repositories.keys()),
    help='Choose a repository label'
)

transform_arguments.add_argument(
    'subject_count_min',
    type=int,
    required=True,
    choices=tuple([
        1,
        2,
        3,
    ]),
    help='Choose minimum subject count'
)

transform_arguments.add_argument(
    'subject_count_max',
    type=int,
    required=True,
    choices=tuple([
        1,
        2,
        10,
        100,
    ]),
    help='Choose maximum subject count'
)


@api.route('/FlareRecords')
class FlareRecords(Resource):

    @api.expect(transform_arguments)
    def get(self):
        args = transform_arguments.parse_args(request)
        subject_count_min = args.get('subject_count_min')
        subject_count_max = args.get('subject_count_max')
        repository_label = args.get('repository_label')
        datadir = '/'.join(('.', 'data', 'transformed', repository_label))
        print(datadir)
        return_data = transformer.flare('all_sets.json', subject_count_min, subject_count_max)
        file_suffix = '_'.join(('','min', str(subject_count_min), 'max', str(subject_count_max)))
        try:
            filename = '/'.join((datadir, ''.join(('all_sets',file_suffix, '.json'))))
            print(filename)
            glam_io.write_json(filename, return_data)
        except Exception as e:
            abort(400, e)

        return return_data

