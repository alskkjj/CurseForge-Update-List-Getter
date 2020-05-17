import GmailQuerys

from curse_forge import CurseForgeUpdateApp
from curse_forge import UpgradableMailsFilter

def gmail_querys():
    service_obj = GmailQuerys.service_mk()
    return GmailQuerys.GmailQuerys(service_obj)

#from TEST_main import StickQuerys

querys_obj = gmail_querys()
#querys_obj = StickQuerys()
filter_obj = UpgradableMailsFilter()

# load Google Mail Labels, the google mail labels only works for gmail

app = CurseForgeUpdateApp(querys=querys_obj, _filter=filter_obj, labelIds=GmailQuerys.googleMailLablesIds)
app.process()

res = app.res

import json
with open('Result_list.json', 'w') as fd:
    json.dump(res, fd)
