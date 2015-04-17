

def sourceResource_subject_name(el):
    return [s['name'] for s in list(el['sourceResource']['subject'])]

def sourceResource_title(el):
    t = el['sourceResource']['title']
    if type(t) == list:
        return [t for t in el['sourceResource']['title']]
    else:
        return t

