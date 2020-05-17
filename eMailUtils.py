
from email.parser import BytesParser

import re
__mail_address_pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)" )

def is_mail_addr(addr):
    if not isinstance(addr, str):
        raise TypeError('input type is not str')
    if len(addr) < 1:
        return False

    return re.match(__mail_address_pattern, addr)
    
def mail_addr_hostname(addr):
    if not is_mail_addr(addr): raise RuntimeError('mail address is not correct')
    return addr.split('@')[1]

def mail_addr_name(addr):
    if not is_mail_addr(addr): raise RuntimeError('mail address is not correct')
    return addr.split('@')[0]
 
__bytes_parser = BytesParser()

def get_mail_subject(mail):
    return mail.get('Subject', None)

def get_mail_from(mail):
    return mail.get('From', None)

def get_sender(mail):
    return get_mail_from(mail)

def get_payloads(mail):
    return mail.get_payload()

def get_html_payloads(mail):
    lst = []
    pl = mail.get_payload()
    if isinstance(pl, str):
        return [ pl ] 

    for i in pl:
        if i.get_content_type().count('html') > 0:
            lst.append(i.get_payload()) 
    return lst

def get_plain_payloads(mail):
    lst = []
    for i in mail.get_payload():
        if i.get_content_type().count('plain') > 0:
            lst.append(i.get_payload())
    return lst


def get_email_object(mbts: bytes):
    return __bytes_parser.parsebytes(mbts)

"""
import base64
import json
from pprint import pprint
with open('test_forder1_raw/172065cf7d1bd769.json', 'r') as fd:
    tmp = json.load(fd).get('raw', b'')
    bts = base64.urlsafe_b64decode(tmp.encode('ASCII'))

#print(bts)
mail = get_email_object(bts)#, headersonly=True)
print(get_html_payloads(mail)[0])

import curse_forge
subject = get_mail_subject(mail)
strings = get_html_payloads(mail)

pprint(strings)
print(curse_forge.is_curse_forge_update(subject, strings))
"""