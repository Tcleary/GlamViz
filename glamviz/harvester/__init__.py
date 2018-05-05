import os

from sickle import Sickle, oaiexceptions
from flask_restplus import abort, reqparse
from flask import current_app

import glam_io

repository_url = 'http://archives.laguardia.edu/oai2'
#repository_url = 'http://commons.clarku.edu/do/oai/'
#repository_url = 'http://academicworks.cuny.edu/do/oai/'


def get_repository_url():
    app = current_app
    config_filename = os.path.join(app.instance_path, 'config', 'settings.json')
    data = glam_io.read_json(config_filename)

    repository_url = ''

    if data:
        if data.get('repository'):
            repository_url = data.get('repository').get('url')

    return repository_url


def get_record_metadata(repository_url, identifier):
    sickle = Sickle(repository_url)
    rec = sickle.GetRecord(
        identifier=identifier,
        metadataPrefix='oai_dc'
    )
    return rec.metadata


def list_sets(repository_url=None):
    repository_url = repository_url or get_repository_url()
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

def get_identifiers_in_set(repository_url, setSpec):
    sickle = Sickle(repository_url)
    return sickle.ListIdentifiers(
        metadataPrefix='oai_dc',
        ignore_deleted=True,
        set=setSpec,
    )

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


def list_identifiers(repository_url, setSpec=None):
    keys = ['setSpec', 'setName']
    identifiers_list = []

    identifiers = get_identifiers_in_set(repository_url, setSpec)

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

def list_set_records(repository_url, setSpec):
    recs = []
    set_rec_idents = []
    try:
        set_rec_idents = list_identifiers(repository_url, setSpec)
    except oaiexceptions.NoRecordsMatch:
        pass

    for ident in set_rec_idents:
        ident['setSpec'] = setSpec
        ident['dc'] = get_record_metadata(repository_url, ident.get('identifier'))
        recs.append(
             ident
        )
    return recs


def subject_counts(repository_url, setSpec):
    subjects = {}
    subject_ranks = {}
    recs = list_set_records(repository_url, setSpec)
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


