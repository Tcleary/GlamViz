import json

from glam_io import write_json


def limit_size(data, key, lowest_value ):
    return data

def find_limit (data):
    return data

def ceiling (value, limit):
    value = value
    return value

def times (value, number):
    value = number * value
    return value


def flare(filename, subject_count_min, subject_count_max):
    try:
        with open(filename) as json_data:
            d = json.load(json_data)
    except Exception as e:
        print(e)

    flare_data = {}

    for rec in d:
        spec=rec.get('setSpec')
        dc=rec.get('dc')
        subject = dc.get('subject')
        if subject:
            setmap = flare_data.get(spec) or {}
            for subj in subject:
                subj_recs = setmap.get(subj) or []
                subj_recs.append(dc.get('identifier')[0])
                setmap[subj] = subj_recs
            flare_data[spec] = setmap

    flare_children = []

    for num, spec in enumerate(flare_data.keys()):
        if True:  # num < 10000:
            subjects = flare_data.get(spec)
            cluster_children = []
            if subjects:
                for subj in subjects.keys():
                    if subject_count_max >= len(subjects.get(subj)) >= subject_count_min:
                        cluster_children.append(
                            {"name": subj or 'NONAME',
                             "size": times (len(subjects.get(subj)), 1000)
                             }

                        )
            if cluster_children:
                spec_children = {
                    "name": spec,
                    "children": [
                        {"name": "subject",
                         "children": cluster_children}
                    ]
                }
                flare_children.append(spec_children)

    flare = {
        "name": "flare",
        "children": flare_children
    }

    subject_size_min_str = './GlamCodeTest{}.json'.format(subject_count_min)
    glam_size_test_filename = subject_size_min_str
    write_json(glam_size_test_filename, flare)
    return flare