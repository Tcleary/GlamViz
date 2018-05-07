import os

from sickle import Sickle, oaiexceptions
from flask_restplus import abort, reqparse
from flask import current_app

import glam_io
import admin


def get_record_metadata(repository_url, identifier):
    sickle = Sickle(repository_url)
    rec = sickle.GetRecord(
        identifier=identifier,
        metadataPrefix='oai_dc'
    )
    return rec.metadata


def list_sets(repository_url=None):
    repository_url = repository_url or admin.get_repository_url()
    sickle = Sickle(repository_url)
    setlist = []
    listsets = sickle.ListSets()

    try:
        for i in range(500):
            s = listsets.next()
            setlist.append(
                {
                    'setSpec': s.setSpec,
                    'setName': s.setName,
                }
            )
    except StopIteration:
        pass
    except Exception as e:
        abort(400, e)

    return setlist


def get_identifiers_in_set(setSpec):
    sickle = Sickle(admin.get_repository_url())
    return sickle.ListIdentifiers(
        **{ 'metadataPrefix': 'oai_dc',
            'set': setSpec,
    })


def list_sets_with_counts(repository_url):
    sickle = Sickle(repository_url)
    setlist = []
    listsets = sickle.ListSets()

    try:
        for i in range(500):
            s = listsets.next()
            #identifiers = get_identifiers_in_set(s.setSpec)
            cnt = 'Ha' #len(identifiers)

            set_identifiers = list_identifiers(s.setSpec)

            setlist.append(
                {
                    'setSpec': s.setSpec,
                    'setName': s.setName,
                    'set_identifiers': set_identifiers,
                }
            )
    except StopIteration:
        pass
    except Exception as e:
        abort(400, e)

    return setlist


def list_identifiers(setSpec=None):
    keys = ['setSpec', 'setName']
    identifiers_list = []

    identifiers = get_identifiers_in_set(admin.get_repository_url(), setSpec)

    try:
        while(True):
            h = identifiers.next()
            identifiers_list.append(
                {
                    'identifier': h.identifier,
                    'datestamp': h.datestamp,
                }
            )
    except StopIteration:
        pass
    except Exception as e:
        abort(400, e)

    return identifiers_list
    """
    return {
        'record_count': len(identifiers_list),
        'record_list': identifiers_list,
    }
    """


def list_set_records(setSpec):
    set_recs = []
    sickle = Sickle(admin.get_repository_url())
    try:
        recs = sickle.ListRecords(metadataPrefix='oai_dc', set=setSpec)
        for rec in recs:
            #rec = recs.next()
            set_recs.append({
            "identifier": rec.header.identifier,
            "datestamp": rec.header.datestamp,
            "setSpec": rec.header.setSpecs,
            "dc": rec.metadata,
        })
    except Exception as e:
        pass
    #return [rec_type, rec.metadata, rec.header.identifier, rec.header.setSpecs, rec.header.datestamp, rec.header.deleted, rec.raw]
    return set_recs


def list_set_records_save(setSpec):
    recs = []
    set_rec_idents = []
    try:
        set_rec_idents = list_identifiers(admin.get_repository_url(), setSpec)
    except oaiexceptions.NoRecordsMatch:
        pass

    for ident in set_rec_idents:
        ident['setSpec'] = setSpec
        ident['dc'] = get_record_metadata(admin.get_repository_url(), ident.get('identifier'))
        recs.append(
             ident
        )
    return recs


def subject_counts(setSpec):
    subjects = {}
    subject_ranks = {}

    recs = list_set_records(setSpec)
    for r in recs:
        subject = r.get('subject')
        if subject:
            for s in subject:
                count = subjects.get(s) or 0
                subjects[s] = count + 1

    for s in subjects.keys():
        rank = subjects.get(s)
        rank_subjects = subject_ranks.get(rank) or []
        rank_subjects.append(s)

        subject_ranks[rank] = rank_subjects

    sorted_ranks = []
    for i in sorted(subject_ranks.keys(), reverse=True):
        sorted_ranks.append({
            'occurences': i,
            'subjects': subject_ranks.get(i),
        })

    return {
        'records_in_set': len(recs),
        'subject_rankings': sorted_ranks,
    }

def combine_all_sets_file(bundle_path=None):

    bundle_path = bundle_path or 'publication_bb'
    from os import listdir
    from os.path import isfile, join
    datadir = os.path.join(
        current_app.instance_path,
        'data',
        'harvested',
        admin.get_repository_label()
    )

    all_recs = {}
    counts = {}
    onlyfiles = [f for f in listdir(datadir) if isfile(join(datadir, f))]

    for f in onlyfiles:
        if f != 'all_sets.json':
            filepath = os.path.join(datadir, f)
            data = glam_io.read_json(filepath)
            counts[f] = len(list(data))
            for item in data:
                identifier = item.get('identifier')
                if all_recs.get(identifier):
                    pass
                else:
                    all_recs[identifier] = item

    unique_identifiers = len(all_recs.keys())
    all_set_records = []
    for identifier in all_recs.keys():
        all_set_records.append(all_recs.get(identifier))

    glam_io.write_json(os.path.join(datadir, 'all_sets.json'), all_set_records)

    return [{'unique_identifiers': unique_identifiers}, counts ]