repositories = {
    'Laguardia': 'http://archives.laguardia.edu/oai2',
    'Clark': 'http://commons.clarku.edu/do/oai/',
    'CUNY': 'http://academicworks.cuny.edu/do/oai/',
}

def add_repository (label, url):
    repositories[label] = url
    return {
        'label': label,
        'url': url,
    }