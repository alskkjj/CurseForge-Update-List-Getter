
import re
from html import parser

__p_re_lst = {
    'curseforge_match' : re.compile('[cC]urse\s*[fF]orge')
    }
def is_curse_forge_related(string):
    if not isinstance(string, str):
        raise TypeError('is_curse_forge: parameters wrong')

    #if ( host_name.count('curseforge') and
    #   string.count('been going on lately with CurseForge:') ):
    if __p_re_lst['curseforge_match'].search(string):
        return True

    return False

# soft checker for future's update
__update_sementics = {
    0.60 :re.compile('Followed Project'),
    0.60 : re.compile('are new files in'),
    0.25 :re.compile('Files'),
    0.15 : re.compile('New'),
    0.15 : re.compile('added'),
    0.17 : re.compile('Added'),
    0.67 : re.compile('project-notification'),
    0.90 : re.compile('New files have been added to project')
    }

import math

def is_curse_forge_update(subject, strings):
    assert( isinstance(strings, list) )
    #Possibility are calculated by the formula:
    #   possible = 1 - Product_for_i(1 - Ai*P(Ai))
    possible = 1.0
    if is_curse_forge_related(subject): possible *= 1 - 0.6
    max_possible = -1
    for string in strings:
        for k, v in __update_sementics.items():
            if v.search(string): possible *= 1 - k
        possible = 1 - possible
        if max_possible < possible: max_possible = possible

                                        # 75%
    return math.isclose(max_possible, 1.0, rel_tol=0.25, abs_tol=0.0)


class UpgradableFecth(parser.HTMLParser):
    __tag_with_attrs = {'div' :
                       lambda a : a == [ ('class', 'project-notification') ],
                       'a' :
                        lambda a : a[0][0] =='href' and a[0][1].startswith('https://www.curseforge.com'),
                       'p' :
                        lambda a : a == [ ('class', 'subject')],
                       'strong' :
                        lambda a : a == [('class', 'title')]
                       }


    def __init__(self):
        super(UpgradableFecth, self).__init__(convert_charrefs=True)

        self.__in_sequence = 0 # step index
        self.__now_url = ''
        self.__results_dict = {}

    def __helper(self, tag, s: str, attrs):
        return tag == s and self.__tag_with_attrs[s](attrs)

    def handle_starttag(self, tag, attrs):
        if self.__helper(tag, 'div', attrs) and \
                self.__in_sequence == 0:
            self.__in_sequence = 1;
        if self.__helper(tag, 'a', attrs) and \
                self.__in_sequence == 1:
            self.__now_url = attrs[0][1]
            self.__in_sequence = 2
        if self.__helper(tag, 'p', attrs) and \
                self.__in_sequence == 2:
            self.__in_sequence = 3
        if self.__helper(tag, 'strong', attrs) and \
                self.__in_sequence == 3:
            self.__in_sequence = 4


    def handle_data(self, data):
        if self.__in_sequence == 4:
            self.__results_dict[data] = self.__now_url
            self.__in_sequence = 0

    def fetch(self):
        if not self.__results_dict: return None
        res = self.__results_dict
        self.__results_dict = {}
        return res
        
__curse_upgradable_fecth_dict = UpgradableFecth()

# html -> name, url
def extract_update_items(html: str) -> dict:
    __curse_upgradable_fecth_dict.feed(html)
    tmp = __curse_upgradable_fecth_dict.fetch()

    res = {}
    for k, v in tmp.items():
    # 1. key left and right space delete
        key = k.strip()
    # 2. value tail delete
            # ../../
        i = len(v) - 1
        if v[i] == '/': i -= 1
        flag = 0
        while i > 0:
            if v[i] == '/' and flag == 0:
                flag += 1
            if v[i] == '/' and flag == 1:
                break
            i -= 1
        value = v[0:i]
        res[key] = value

    return res


from IFilter import IFilter
import eMailUtils

class UpgradableMailsFilter(IFilter):
    def filter(self, mail)->bool:
        subject = eMailUtils.get_mail_subject(mail)
        string = eMailUtils.get_html_payloads(mail)
        res = is_curse_forge_update(subject, string)
        return res

import IQuerys
from App import App

class CurseForgeUpdateApp(App):

    def __init__(self,
        querys: IQuerys,
        _filter: IFilter,
        labelIds=['UNREAD', 'INBOX', 'CATEGORY_UPDATES'],
        maxPrePage=10,
        maxPages=None):

        super(CurseForgeUpdateApp, self).__init__(querys, _filter, labelIds, maxPrePage, maxPages)

    def process_html(self, html)->dict:
        ret = extract_update_items(html)
        return ret


"""
import json
import base64
import pprint

with open('test_forder1_raw/172011db28090b2e.json', 'r') as fd:
    tmp = json.load(fd).get('raw', b'')
    bts = base64.urlsafe_b64decode(tmp.encode('ASCII'))

mail = eMailUtils.get_email_object(bts)
hml = eMailUtils.get_html_payloads(mail)
print(hml[0])
pprint.pprint(extract_update_items(hml[0]))
"""
