
from dpla.api import DPLA
import fields

"""
allitems

Demonstrate the use of Python generators with the DPLA API
"""


def search(query, api_key, limit=10):
    """Yield search results item by item"""
    page_size = _page_size(limit)
    dpla = DPLA(api_key)
    page = 0
    yielded = 0
    while yielded < limit:
        page += 1
        result = dpla.search(query, page_size=page_size, page=page,
                             fields=['sourceResource'])
        if len(result.items):
            for item in result.items:
                yield item
                yielded += 1
        else:
            raise StopIteration

def _page_size(limit):
    """Return suitable API page size for desired query limit"""
    if limit > 500:
        return 500
    else:
        return limit

def strings_from_field(field_token, search):
    """Yield strings from a given field defined by the specified function

    The field in the MAP hierarchy is specified in dotted notation; for
    example, `sourceResource.subject.name'.  Note that the field-parsing
    function is assumed to be smart enough to apply the logic necessary for
    that specific field.  In this example, sourceResource.subject may be a
    list (JSON array) of dictionaries (JSON objects) that have 'name' keys.
    That's fine.  Just name the property name regardless of cardinality.

    Example:
        import allitems
        search = allitems.search('fizz', 'YOUR_KEY)
        ff = allitems.strings_from_field('sourceResource.subject.name',
                                         search)
        print "\n".join([subj for subj in ff])
    """
    try:
        f = getattr(fields, field_token.replace('.', '_'))
        for item in search:
            for s in _strings(f(item)):
                yield s
    except AttributeError, e:
        # No function matching field_token
        raise StopIteration

def _strings(thing):
    """Yield strings from elements that could be strings or lists of them"""
    if isinstance(thing, basestring):
        yield thing
    elif type(thing) == list:
        for el in thing:
            for s in _strings(el):
                yield s
    else:
        raise StopIteration
