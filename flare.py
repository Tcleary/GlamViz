import json

def write_json(filename, data):
    try:
        with open(filename, 'w') as outfile:
            outfile.write(json.dumps(data, indent=4))
    except Exception as e:
        return 'Error writing JSON file:', e
    return 'JSON file written'


def flare(filename):
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

    for spec in flare_data.keys():
        subjects = flare_data.get(spec)
        cluster_children = []
        if subjects:
            for subj in subjects.keys():
                cluster_children.append(
                    {"name": subj,
                     "size": len(subjects.get(subj))}

                )
        spec_children = {
            "name": spec,
            "children": [
                {"name": "cluster",
                 "children": cluster_children}
            ]
        }
        flare_children.append(spec_children)

    flare = {
        "name": "flare",
        "children": flare_children
    }

    write_json('flare.json', flare)
    return flare


flare('all_sets.json')
