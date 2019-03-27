"""
Handling redirecting to external data source website.
"""
from paste import httpexceptions
from paste.response import header_value

class _ExternalRedirect(httpexceptions.HTTPRedirection):
    """
    redirections which require a Location field
    Since a 'Location' header is a required attribute of 301, 302, 303,
    305 and 307 (but not 304), this base class provides the mechanics to
    make this easy.  While this has the same parameters as HTTPException,
    if a location is not provided in the headers; it is assumed that the
    detail _is_ the location (this for backward compatibility, otherwise
    we'd add a new attribute).
    """
    required_headers = ('location',)
    explanation = 'Please Click'
    template = (
        '%(explanation)s <a href="%(detail)s">%(detail)s</a> to be redirected to external data source website;\r\n'
        '<!-- %(comment)s -->')

    def __init__(self, detail=None, headers=None, comment=None):
        assert isinstance(headers, (type(None), list))
        headers = headers or []
        location = header_value(headers,'location')
        if not location:
            location = detail
            detail = ''
            headers.append(('location', location))
        assert location, ("HTTPRedirection specified neither a "
                          "location in the headers nor did it "
                          "provide a detail argument.")
        httpexceptions.HTTPRedirection.__init__(self, location, headers, comment)
        if detail is not None:
            self.detail = detail
            
class HTTPFound(_ExternalRedirect):
    code = 302
    title = 'Found'