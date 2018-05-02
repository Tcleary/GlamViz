from flask import request, current_app
from flask_restplus import Namespace, Resource, reqparse

import glam_io
import config
import harvester as harv

api = Namespace('harvest', description='harvest data from repository')


repository_arguments = reqparse.RequestParser()
repository_arguments.add_argument(
    'repository_label',
    type=str,
    required=True,
    choices=tuple(config.repositories.keys()),
    help='Choose repository'
)

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


@api.route('/Admin/Repository')
class AdminRepository(Resource):

    #@api.expect(repository_admin_arguments)
    def get(self):
        return config.repositories
        """
        args = repository_admin_arguments.parse_args(request)
        repository_label = args.get('repository_label')
        repository_url = args.get('repository_url')
        session.get('repositories')[repository_label] = repository_url
        """


@api.route('/ListSets')
class ListSets(Resource):
    def get(self):
        s = []
        try:
            s = harv.list_sets()
        except Exception as e:
            abort(400, e)
        except Exception as e:
            abort(400, e)

        return {
            'set_count': len(s),
            'set_lists': s,
        }


@api.route('/ListIdentifiers')
class ListIdentifiers(Resource):
    def get(self):
        idents = []
        try:
            idents = harv.list_identifiers()
        except Exception as e:
            abort(400, e)
        return idents


@api.route('/WriteListIdentifiers/<string:filename>')
class WriteListIdentifiers(Resource):
    def get(self, filename):
        idents = []
        try:
            idents = harv.list_identifiers()
        except Exception as e:
            abort(400, e)

        glam_io.write_json(filename, idents)
        return idents


@api.route('/ListSetRecords/<string:setSpec>')
class ListSetRecords(Resource):
    def get(self, setSpec):
        set_records = []
        try:
            set_records = harv.list_set_records(setSpec)
        except Exception as e:
            abort(400, e)
        return set_records


@api.route('/WriteAllSetRecords')
class WriteAllSetRecords(Resource):
    def get(self):
        repository_arguments.add_argument(
            'repository_label',
            type=str,
            required=True,
            choices=tuple(config.repositories.keys()),
            help='Choose repository'
        )
        setlist = harv.list_sets()
        set_records = []
        try:
            for s in setlist:
                set_records = harv.list_set_records(s.get('setSpec'))
                glam_io.write_json('.'.join((s.get('setSpec'), 'json')), set_records)
        except oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            abort(400, e)

        return setlist


@api.route('/WriteAllRecords')
class WriteAllRecords(Resource):

    @api.expect(repository_arguments)
    def get(self):
        args = repository_arguments.parse_args(request)
        repository_label = args.get('repository_label')
        repository_url = config.repositories.get(repository_label)
        setlist = harv.list_sets(repository_url)
        set_records = []
        all_records = []
        datadir = '/'.join(('.', 'data', 'harvested', repository_label))
        print(datadir)
        try:
            for s in setlist:
                setSpec = s.get('setSpec') or 'unknown'
                set_records = harv.list_set_records(repository_url, setSpec)
                filename = '/'.join((datadir, ''.join((setSpec,'.json'))))
                print(filename)
                glam_io.write_json(filename, set_records)
                all_records.extend(set_records)
        except harv.oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            harv.abort(400, e)

        filename = '/'.join((datadir, 'all_sets.json'))
        glam_io.write_json(filename, all_records)
        return setlist


@api.route('/WriteSetRecords/<string:setSpec>')
class WriteSetRecords(Resource):
    def get(self, setSpec):
        set_records = []
        try:
            set_records = harv.list_set_records(setSpec)
        except Exception as e:
            abort(400, e)
        glam_io.write_json('.'.join((setSpec, 'json')), set_records)

        return set_records


@api.route('/SubjectCounts/<string:setSpec>')
class SubjectCounts(Resource):
    def get(self, setSpec):
        result = []
        try:
            result = harv.subject_counts(setSpec)
        except Exception as e:
            abort(400, e)
        return result


@api.route('/metadata/<string:identifier>')
class Metadata(Resource):
    def get(self, identifier):
        try:
            metadata = harv.get_record_metadata(identifier)
        except Exception as e:
            abort(400, e)
        return metadata



