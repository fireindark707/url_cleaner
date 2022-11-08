from url_cleaner.url import Url
from url_cleaner.filter import Filter
from url_cleaner.ruler import Ruler
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

class UrlCleaner(object):

    def __init__(self,rule_path=MODULE_DIR):
        self.ruler = Ruler(rule_path)

    def clean(self,url):
        url_parsed = Url(url)
        logger.debug('URL parsed:{}'.format(url_parsed.get_dict()))
        rules = self.ruler.get_general_rules() + self.ruler.host_rules(url_parsed.host)
        logger.debug("Rules:{}".format(rules))
        filter = Filter(rules)
        cleaned_url = filter.filter_url(url_parsed)
        return cleaned_url