import json
import os
import re
import logging

from url_cleaner.url import Url

logger = logging.getLogger(__name__)

class Ruler(object):
    rules_remote_specific = "https://github.com/AdguardTeam/AdguardFilters/raw/master/TrackParamFilter/sections/specific.txt"
    rules_remote_general = "https://github.com/AdguardTeam/AdguardFilters/raw/master/TrackParamFilter/sections/general_url.txt"
    def __init__(self, module_path):
        self.rules_file = os.path.join(module_path, 'rules.json')
        self.module_path = module_path
        self.load_rules()

    def check_rules_exists(self):
        return os.path.exists(self.rules_file)
    
    def load_rules(self):
        if self.check_rules_exists():
            with open(self.rules_file) as f:
                self.rules = json.load(f)
        else:
            raise FileNotFoundError('Rules file not found')

    def save_rules(self):
        with open(self.rules_file, 'w') as f:
            json.dump(self.rules, f, indent=4,ensure_ascii=False)
    
    def download_remote_rules(self,mode=""):
        import requests
        if mode == "specific" or mode == "":
            r = requests.get(self.rules_remote_specific)
            if r.status_code == 200:
                with open(os.path.join(self.module_path, 'rules_remote_specific.txt'), 'w') as f:
                    f.write(r.text)
            else:
                raise Exception('Download remote specific rules failed:{}'.format(self.rules_remote_specific))
        if mode == "general" or mode == "":
            r = requests.get(self.rules_remote_general)
            if r.status_code == 200:
                with open(os.path.join(self.module_path, 'rules_remote_general.txt'), 'w') as f:
                    f.write(r.text)
            else:
                raise Exception('Download remote general rules failed:{}'.format(self.rules_remote_general))

    def update_rules(self,mode=""):
        add_cnt = {"specific":0,"general":0}
        if mode not in ['general', 'specific','']:
            raise Exception('Invalid mode:{}'.format(mode))
        if mode == "specific" or mode == "":
            self.download_remote_rules(mode="specific")
            with open(os.path.join(self.module_path, 'rules_remote_specific.txt')) as f:
                rules_remote_specific = f.read()
            for line in rules_remote_specific.split('\n'):
                ru = re.search(r"^\|\|([^\^]+)\^\$removeparam=([^\,\|]+)",line)
                if ru:
                    url = ru.group(1)
                    query = ru.group(2)
                    url_parsed = Url("http://"+url)
                    host = url_parsed.host
                    pathname = url_parsed.path
                    if host not in self.rules.keys():
                        self.rules[url_parsed.host] = []
                    if len(pathname) >= 1 and pathname != "/":
                        new_rule = {"pathname":pathname,"search":query}
                    else:
                        new_rule = query
                    if new_rule not in self.rules[host]:
                        self.rules[host].append(new_rule)
                        add_cnt["specific"] += 1
                        logger.info('Add specific rule:{} {}'.format(host,str(new_rule)))
        if mode == "general" or mode == "":
            self.download_remote_rules(mode="general")
            with open(os.path.join(self.module_path, 'rules_remote_general.txt')) as f:
                rules_remote_general = f.read()
            for line in rules_remote_general.split('\n'):
                ru = re.search(r'^\$removeparam=([\w\-\_]+)$',line)
                if ru and ru.group(1) not in self.rules["GENERAL"]:
                    self.rules["GENERAL"].append(ru.group(1))
                    add_cnt["general"] += 1
                    logger.info('Add general rule:{}'.format(ru.group(1)))
        logger.info('Update rules finished, add {} specific rules, add {} general rules'.format(add_cnt["specific"],add_cnt["general"]))
        self.save_rules()

    def host_rules(self,host):
        hosts_rules = []
        for rule_host in self.rules.keys():
            if re.search(rule_host,host):
                hosts_rules += self.rules[rule_host]
        return hosts_rules

    def get_general_rules(self):
        return self.rules["GENERAL"]