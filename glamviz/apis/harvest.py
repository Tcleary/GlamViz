import os
from flask import request, current_app
from flask_restplus import Namespace, Resource, reqparse, abort
from sickle import oaiexceptions

import glam_io
import admin
import harvester as harv

api = Namespace('harvest', description='harvest data from repository')

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
@api.doc(False)
class ListIdentifiers(Resource):
    def get(self):
        idents = []
        try:
            idents = harv.list_identifiers()
        except Exception as e:
            abort(400, e)
        return idents


@api.route('/CountSetIdentifiers/<string:setSpec>')
@api.doc(False)
class CountSetIdentifiers(Resource):
    def get(self, setSpec):
        idents = []
        try:
            idents = harv.get_identifiers_in_set(setSpec)
        except Exception as e:
            abort(400, e)
        return len(list(idents))


@api.route('/WriteListIdentifiers/<string:filename>')
@api.doc(False)
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
@api.doc(False)
class ListSetRecords(Resource):
    def get(self, setSpec):
        set_records = []
        try:
            set_records = harv.list_set_records(setSpec)
        except Exception as e:
            abort(400, e)
        return set_records


@api.route('/WriteSetRecords/<string:setSpec>')
@api.doc(False)
class WriteAllSetRecords(Resource):
    def get(self, setSpec):

        set_records = []
        try:
            set_records = harv.list_set_records(setSpec)
            datadir = '/'.join((current_app.instance_path, 'data', 'harvested', admin.get_repository_label()))
            filename = '/'.join((datadir, ''.join((setSpec, '.json'))))
            glam_io.write_json(filename, set_records)
        except oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            abort(400, e)

        return {
            'setSpec': setSpec,
            'set_record_count': len(list(set_records)),
        }


@api.route('/WriteAllRecords')
class WriteAllRecords(Resource):

    def get(self):

        setlist = harv.list_sets(admin.get_repository_url())
        set_records = []
        all_records = []
        datadir = os.path.join(
            current_app.instance_path,
            'data',
            'harvested',
            admin.get_repository_label()
        )
        print(datadir)
        try:
            for s in setlist:
                setSpec = s.get('setSpec') or 'unknown'
                filepath = glam_io.clean_filepath(
                    os.path.join(datadir, ''.join((setSpec, '.json')))
                )

                if os.path.isfile(filepath):
                    print('Testing existence of:', filepath)
                else:
                    print('preparing new file:', filepath)
                    set_records = harv.list_set_records(setSpec)
                    glam_io.write_json(filepath, set_records)
                #all_records.extend(set_records)
        except harv.oaiexceptions.NoRecordsMatch:
            pass
        except Exception as e:
            harv.abort(400, e)

        #filename = '/'.join((datadir, 'all_sets.json'))
        #glam_io.write_json(filename, all_records)
        return setlist


@api.route('/WriteSetRecords/<string:setSpec>')
@api.doc(False)
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
@api.doc(False)
class SubjectCounts(Resource):
    def get(self, setSpec):
        result = []
        try:
            result = harv.subject_counts(setSpec)
        except Exception as e:
            abort(400, e)
        return result


@api.route('/metadata/<string:identifier>')
@api.doc(False)
class Metadata(Resource):
    def get(self, identifier):
        try:
            metadata = harv.get_record_metadata(identifier)
        except Exception as e:
            abort(400, e)
        return metadata


@api.route('/WriteAllSetsFile')
class WriteAllSetsFile(Resource):
    def get(self):
        return harv.combine_all_sets_file()


