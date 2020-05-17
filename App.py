import IQuerys
import IFilter

import eMailUtils

class App:
    def __init__(self, 
                 querys: IQuerys, 
                 _filter: IFilter,
                 labelIds: list, 
                 maxPrePage: int,
                 maxPages: int
                 ):
        self.__querys = querys
        self.__filter = _filter
        self.__labelIds = labelIds
        self.__maxPrePage = maxPrePage
        self.__maxPages = maxPages
        self.__res = {}
    
    @property
    def res(self):
        return self.__res

    def process_html(self, html) -> dict:
        pass

    def process(self):
        handler = self.__querys.init_a_query(self.__labelIds, self.__maxPrePage
                                             ,maxPages=self.__maxPages)
        r = True 
        while r: 
            r = self.__querys.next(handler)
            if r: mailobj = eMailUtils.get_email_object(r)
            if self.__filter.filter(mailobj):
                htmls = eMailUtils.get_html_payloads(mailobj)
                for i in htmls:
                    dt = self.process_html(i)
                    if dt:
                        self.__res = {**self.__res, **dt} # override old res if same key

        self.__querys.end(handler)           
