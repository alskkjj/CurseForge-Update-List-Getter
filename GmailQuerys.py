
import IQuerys

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
import base64
import os

def service_mk():
    print('init gmail service...')
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_pickle = 'token.pickle'
    if os.path.exists(token_pickle):
        with open(token_pickle, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            cred_json = 'credentials.json'
            if not os.path.isfile(cred_json):
                raise RuntimeError("""Please follow the tutorials of Google Mail API,
                Register your own Google Mail Service, and place the \"credentials.json\" at root directory.
                See https://developers.google.com/gmail/api/quickstart/python""")
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_json, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_pickle, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    print('gmail service initialized')
    return service


googleMailLablesIds = ['UNREAD', 'INBOX', 'CATEGORY_UPDATES']
class GmailQuerys(IQuerys.IQuerys):
    def __init__(self, service):
        self.__service = service
        self.__page_count = 0

    def get_messageIds_list_and_pageToken(self,
        labelIds,
        maxPrePage,
        pageToken=None) -> (list, object):
        try:
            results = self.__service.users().messages().list(
                                             userId='me',
                                             labelIds=labelIds,
                                             pageToken=pageToken,
                                             maxResults=maxPrePage,
                                             ).execute()
        except errors.HttpError as err:
            print(err)
            print('    at GmailQuerys::get_messageIds_list_and_pageToken')
            exit()

        lst = []
        for i in results.get('messages', []):
            lst.append(i.get('id', ''))

        pageToken = results.get('nextPageToken', None)
        print('No.', self.__page_count, ' : get %d messages' % len(lst))
        self.__page_count += 1
        print('next page token', str(pageToken))
        return lst, pageToken

    def get_message_by_Id(self, messageId)->str:
        try:
            raw_msg = self.__service.users().messages().get(userId='me',
                                                            id=messageId,
                                                            format='raw').execute()
        except errors.HttpError as error:
            print(error)
            print('    at GmailQuerys::get_message_by_Id')
            exit()

        res = base64.urlsafe_b64decode(raw_msg.get('raw', '').encode('ASCII'))
        print('message %s got' % messageId)
        return res

"""
obj = GmailQuerys(service_mk())
handler = obj.init_a_query(['UNREAD', 'CATEGORY_SOCIAL'], 10)
res = True
with open('Test_Mail.js', 'w') as fd:
    while(res):
        res = obj.next(handler)
        if res: fd.write(res.decode('UTF-8'))
        fd.write('\n\n\n--------------------------\n\n\n')
"""
