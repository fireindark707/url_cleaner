from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

class Url(object):
    """
    The following methods are used to modify the url
    """
    def __init__(self, url=None):
        self.scheme = None
        self.netloc = None
        self.host = None
        self.path = None
        self.params = None
        self.query = None
        self.fragment = None
        self.query_dict = None
        if url:
            self.original_url = url
            self.parse_url()
            self.parse_query()

    def parse_url(self):
        """
        Parse the url and set the attributes
        """
        if not self.original_url.startswith('http'):
            self.original_url = 'http://' + self.original_url
        u = urlparse(self.original_url)
        self.scheme = u.scheme
        self.netloc = u.netloc
        self.host = u.hostname
        self.path = u.path
        self.params = u.params
        self.query = u.query
        self.fragment = u.fragment
        return u

    def parse_query(self):
        """
        Parse the query string and set the query_dict attribute
        """
        self.query_dict = parse_qs(self.query)
        return self.query_dict

    def get_query_by_dict(self):
        """
        Return the query string by the query dict
        """
        return urlencode(self.query_dict, doseq=True)

    def get_url(self):
        """
        Unparse the url and return the url
        """
        self.query = self.get_query_by_dict()
        return urlunparse((self.scheme,self.netloc, self.path, self.params, self.query, self.fragment))

    def __str__(self):
        return self.get_url()

    def copy(self):
        """
        Return a copy of the Url object
        """
        return Url(self.get_url())

    def get_dict(self):
        """
        transform the object to dict
        """
        return {
            'scheme': self.scheme,
            'netloc': self.netloc,
            'host': self.host,
            'path': self.path,
            'params': self.params,
            'query': self.query,
            'fragment': self.fragment,
            'query_dict': self.query_dict,
        }
