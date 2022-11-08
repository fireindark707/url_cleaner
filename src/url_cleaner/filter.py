import re

class Filter(object):
    def __init__(self, rules):
        self.rules = rules

    def filter_url(self, url):
        self.url = url
        for rule in self.rules:
            if isinstance(rule,str):
                self.remove_query(rule)
            elif isinstance(rule,dict):
                assert rule.keys() == {'pathname','search'}
                if self.check_pathname(rule['pathname']):
                    assert isinstance(rule['search'],str)
                    self.remove_query(rule['search'])
        return self.url.get_url()

    def remove_query(self, query):
        if query.startswith('/') and query.endswith('/'):
            self.remove_query_by_regex(query)
        elif self.url.query_dict.get(query):
            self.url.query_dict.pop(query)

    def check_pathname(self, pathname):
        if pathname.startswith('/') and pathname.endswith('/'):
            return bool(re.search(pathname[1:-1],self.url.path))
        else:
            return pathname in self.url.path

    def remove_query_by_regex(self, regex):
        regex = r"{}".format(regex[1:-1])
        cleaned_query_dict = {}
        for k in self.url.query_dict.keys():
            if bool(re.search(regex,k)):
                continue
            cleaned_query_dict[k] = self.url.query_dict[k]
        self.url.query_dict = cleaned_query_dict