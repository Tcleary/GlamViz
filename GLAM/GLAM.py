from flask import Flask
from flask_restplus import Api, Resource, abort
from sickle import oaiexceptions

import Harvester as harv
import IO
import Transform

app = Flask(__name__)
api = Api(app)


@api.route('/language')
class Lanquage(Resource):
    def get(self):
        return {'hey' : 'there'}


@api.route('/metadata/<string:identifier>')
class Metadata(Resource):
    def get(self, identifier):
        try:
            metadata = harv.get_record_metadata(identifier)
        except Exception as e:
            abort(400, e)
        return metadata


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

        IO.write_json(filename, idents)
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
        setlist = harv.list_sets()
        set_records = []
        try:
            for s in setlist:
                set_records = harv.list_set_records(s.get('setSpec'))
                IO.write_json('.'.join((s.get('setSpec'), 'json')), set_records)
        except oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            abort(400, e)

        return setlist


@api.route('/FlareRecords')
class FlareRecords(Resource):
    def get(self):
        return Transform.flare('all_sets.json', 3)


@api.route('/WriteAllRecords')
class WriteAllRecords(Resource):
    def get(self):
        setlist = harv.list_sets()
        set_records = []
        all_records = []
        try:
            for s in setlist:
                set_records = harv.list_set_records(s.get('setSpec'))
                all_records.extend(set_records)
        except oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            abort(400, e)

        IO.write_json('all_sets.json', all_records)
        return setlist

@api.route('/WriteSetRecords/<string:setSpec>')
class ListSetRecords(Resource):
    def get(self, setSpec):
        set_records = []
        try:
            set_records = harv.list_set_records(setSpec)
        except Exception as e:
            abort(400, e)
        IO.write_json('.'.join((setSpec, 'json')), set_records)

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


if __name__ == '__main__':
    app.run(debug=True)


