# standard of mail

import sys

class QuerySession:
    def __init__(self,
                 labelIds : list,
                 maxEntriesPrePage : int,
                 maxPages = None
                 ):
        self.__nextPageToken = None
        self.labelIds = labelIds
        self.currentMessageIdsListIndex = 0
        self.currentMessageIdsList = None
        self.maxEntriesPrePage = maxEntriesPrePage

        self.pages_count = 0
        self.max_pages = maxPages

    @property
    def nextPageToken(self):
        return self.__nextPageToken
    @nextPageToken.setter
    def nextPageToken(self, _nextPageToken):
        self.__nextPageToken = _nextPageToken

class IQuerys:
    # int : QuerySession
    __session_map = {}

    # idx manager:
    __lastidx = 0xfffe
    def give_an_idx(self):
        if self.__lastidx < sys.maxsize - 1:
            self.__lastidx += 1
        else:
            raise RuntimeError('how this exhausted?')
        return self.__lastidx


    def init_a_query(self, labelIds: list, maxEntriesQuantity: int, maxPages=None) -> int:
        idx = self.give_an_idx()
        self.__session_map[idx] = QuerySession(labelIds, maxEntriesQuantity, maxPages)
        return idx

    def get_messageIds_list_and_pageToken(self,
                                        labelIds,
                                        maxPrePage,
                                        pageToken=None
                                        ) -> (list, object):
        """
        read a page from wherever and report it as a list and next page token
        the parameters of labelsIds, maxPrePage are not severely stricted,
        they are from gmail api, and direct us to a intuitive way to get mail ids via pages,

        read Stick assertion code below, it's input can be any objects

        Conditions:
         if not beginning, the input parameter pageToken are None
         this means session object's page list is None, and nextPageToken is also None
         if has next page to get:
             return:
                first parameter #type(list) as new page, which "indexed" by pageToken input parameter,
                seconds parameter #type(object) as next page token
         if no page left:
             return:
                first parameter #type(list) as last page list
                seconds parameter #type(object) as None
        """
        pass

    def get_message_by_Id(self, messageId) -> str:
        """
        messageId can arbirarily be anything what maps to a mail
        return a string, which are python email module can parse
        """
        pass

    def __get_new_page(self, sessionId: int):
        sessionObj = self.__session_map[sessionId]
        if isinstance(sessionObj.max_pages, int):
            if not sessionObj.pages_count < sessionObj.max_pages:
                sessionObj.nextPageToken = None
                return
        new_messageIdsList, nextPageToken = \
        self.get_messageIds_list_and_pageToken(
            sessionObj.labelIds,
            sessionObj.maxEntriesPrePage,
            sessionObj.nextPageToken,
            ) # Message Id only list

        sessionObj.currentMessageIdsList = new_messageIdsList
        sessionObj.nextPageToken = nextPageToken
        sessionObj.currentMessageIdsListIndex = 0

    def __get_next(self, sessionId: int):
        sessionobj = self.__session_map[sessionId]


        idx = sessionobj.currentMessageIdsListIndex
        if idx >= len(sessionobj.currentMessageIdsList):
            if sessionobj.currentMessageIdsList and not sessionobj.nextPageToken:
                return None
            self.__get_new_page(sessionId)

        messageId = sessionobj.currentMessageIdsList[sessionobj.currentMessageIdsListIndex]
        sessionobj.currentMessageIdsListIndex += 1

        return self.get_message_by_Id(messageId)

    # @param: session id
    # return message, can be loaded by email.python
    def next(self, sessionId: int) -> str:


        if sessionId not in self.__session_map.keys():
            raise RuntimeError('not initialized id handle')

        sessionobj = self.__session_map[sessionId]

        # first time
        if sessionobj.currentMessageIdsList == None and sessionobj.nextPageToken == None:
            self.__get_new_page(sessionId)

        return self.__get_next(sessionId)

    def end(self, sessionId):
        if sessionId not in self.__session_map.keys():
            raise RuntimeError('not initialized id handle')
        del self.__session_map[sessionId]


stick_pages =  [  [1, 2, 9, 4, 5],
                   [1, 3, 4, 5, 6],
                   [3,4, 5, 6, 7],
                   [2, 4, 5, 6, 6],
                   [0, 1, 2, 4, 5, 6, 1, 4, 2, 3]
                   ]
stick_content = []
for i in range(0, 10):
    stick_content.append(str(i))


class Stick(IQuerys):
    #def __init__(self, service):
    #    super(Stick, self).__init__()
    #    self.__service = service

    def get_message_by_Id(self, messageId)->str:
        return stick_content[messageId]

    def get_messageIds_list_and_pageToken(self,
                                          labelIds,
                                          maxPrePage,
                                          pageToken=None,
                                          ) -> (list, object):
        if pageToken == None:
            pageToken = 0

        if pageToken >= len(stick_pages): # PageToken out of stick_pages' range
            # out of pages
            pageToken = len(stick_pages)-1
            return stick_pages[pageToken], None

        return stick_pages[pageToken], pageToken + 1


obj = Stick()
handle = obj.init_a_query([], 10, 2)
tmp = []
for i in stick_pages:
        tmp.extend(i)
ii = 0
while ii < len(tmp):
    content = obj.next(handle)
    assert(str(tmp[ii]) == content)
    if content == None:
        break
    ii += 1

del ii
del tmp
del handle
del obj
del stick_content
del stick_pages
