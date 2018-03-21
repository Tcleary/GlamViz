from sickle import Sickle, oaiexceptions
import json

repository_url = 'http://archives.laguardia.edu/oai2'
#repository_url = 'http://commons.clarku.edu/do/oai/'
#repository_url = 'http://academicworks.cuny.edu/do/oai/'

sickle = Sickle(repository_url)


def write_all_records():
    
    setlist = list_sets()
    set_records = []
    all_records = []
    try:
        for s in setlist:
            set_records = list_set_records(s.get('setSpec'))
            all_records.extend(set_records)
    except oaiexceptions.NoRecordsMatch:
        pass
    except Exception as e:
        print(e)

    write_json('all_sets.json', all_records)
    return setlist


def write_json(filename, data):
    try:
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'


def append_json(filename, data):
    try:
        with open(filename, 'a+') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'


def get_record_metadata(identifier):
    rec = sickle.GetRecord(
        identifier=identifier,
        metadataPrefix='oai_dc'
    )
    return rec.metadata


def list_sets():
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
        print(e)

    return setlist


def get_identifiers_in_set(setSpec):
    return sickle.ListIdentifiers(
        metadataPrefix='oai_dc',
        ignore_deleted=True,
        set=setSpec,
    )


def list_sets_with_counts():
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
        print(e)

    return setlist


def list_identifiers(setSpec=None):
    keys = ['setSpec', 'setName']
    identifiers_list = []

    identifiers = get_identifiers_in_set(setSpec)

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
        print(e)

    return identifiers_list
    """
    return {
        'record_count': len(identifiers_list),
        'record_list': identifiers_list,
    }
    """

def list_set_records(setSpec):
    recs = []
    set_rec_idents = []
    try:
        set_rec_idents = list_identifiers(setSpec)
    except oaiexceptions.NoRecordsMatch:
        pass

    for ident in set_rec_idents:
        ident['setSpec'] = setSpec
        ident['dc'] = get_record_metadata(ident.get('identifier'))
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



write_all_records()

