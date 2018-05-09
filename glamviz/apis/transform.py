import os

from flask_restplus import Namespace, Resource, reqparse
from flask_restplus import abort
from flask import request, current_app

import admin
import glam_io
import transformer

api = Namespace('transform', description='transform data for use in visualizations')

transform_arguments = reqparse.RequestParser()

transform_arguments.add_argument(
    'subject_count_min',
    type=int,
    required=True,
    choices=tuple([
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        500,
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
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        500,
        1000
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
        repository_label = admin.get_repository_label()
        harvested_datadir = os.path.join(
            current_app.instance_path,
            'data',
            'harvested',
            repository_label
        )
        transformed_datadir = os.path.join(
            current_app.instance_path,
            'data',
            'transformed',
            repository_label
        )

        harvested_datafilepath = os.path.join(harvested_datadir, 'all_sets.json')

        print(harvested_datafilepath)
        return_data = transformer.flare(harvested_datafilepath, subject_count_min, subject_count_max)
        file_suffix = '_'.join(('','min', str(subject_count_min), 'max', str(subject_count_max)))
        try:
            filename = os.path.join(transformed_datadir,
                                    ''.join(('all_sets', file_suffix, '.json')))
            print(filename)
            glam_io.write_json(filename, return_data)
        except Exception as e:
            abort(400, e)



        return [
            {'filepath': transformer.unescape_filepath(filename)},
            {'data': return_data},
        ]

