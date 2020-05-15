import json
import user
import requests
import wikipedia
import urllib.parse
import polona as PolonaAPI
from collections import namedtuple
#
#
class Comment:

    def __init__(self, comment_id:int, user_id:int, content:str):
        self.__id = comment_id
        self.__who = user_id
        self.__content = content

    def getCommentTuple(self):
        return [self.__id, self.__who, self.__content]

    def __eq__(self, other):
        return self.getCommentTuple()==other.getCommentTuple()


class Resource:

    def __init__(self, link, categoryid):
        self._link = link
        self._categoryid = categoryid
        self._maxPoints = 0
        self._comments = list()
        
        self._visits = 0
    
    @classmethod
    def loadFromJSON(cls, data):
        t = data['_title']
        l = data['_link']
        c = data['_categoryid']
        m = data['_maxPoints']
        v = data['_visits']
        res = cls(l,c)
        res.setVisits(v)
        commentlist = list()
        for c in data["_comments"]:
            commentlist.append(Comment(c['_Comment__id'], c['_Comment__who'], c['_Comment__content']))
        res.setComments(commentlist)
        res.setMaxPoints(m)
        res.setTitle(t)
        return res

    def getLink(self):
        return self._link

    def getTitle(self):
        return self._title

    def setTitle(self, t):
        self._title = t
    
    def getCategoryID(self):
        return self._categoryid

    def getMaxPoints(self):
        return self._maxPoints

    def setMaxPoints(self, maxp):
        self._maxPoints = maxp

    def getComments(self):
        return self._comments

    def setComments(self, c):
        self._comments=c

    def getVisits(self):
        return self._visits

    def addVisit(self):
        self._visits+=1

    def setVisits(self, v):
        self._visits=v

    def addComment(self, cid:int, user_id:int, content:str):
        for i in self._comments:
            if(i.getCommentTuple()[2]==content):
                return
        #print(Comment(cid, user_id, content).getCommentTuple())
        self._comments.append(Comment(cid, user_id, content))

    def removeComment(self, cid):
        for c in self._comments:
            if(c.getCommentTuple()[0]==cid):
                self._comments.remove(c)

    def recalculateMaxPoints(self):
        self._maxPoints=100

    def getComments(self):
        return self._comments

    def serialize(self):
        return json.dumps(self, default=lambda  o: o.__dict__, sort_keys=False, indent=4)


class WikipediaResource(Resource):

    def __init__(self, link,catid=1,recalc=True):
        
        super().__init__(link, catid)
        self._title = link.split('/',-1)[-1].replace("wiki?title=",'')
        self._title = urllib.parse.unquote(self._title)
        try:
            w = wikipedia.WikipediaPage(self._title.replace('+',' '))
        except:
            raise(AssertionError)
        if(recalc):
            self.recalculateMaxPoints()

    def recalculateMaxPoints(self):
        wikiartContent = wikipedia.page(self.getTitle()).content
        length = len(wikiartContent)
        self._maxPoints = 100 + int(length/100)

class PolonaResource(Resource):

    def __init__(self, link,catid=2,recalc=True):
        link = link.split("&page=",1)[0]
        
        super().__init__(link, catid)
        self._title = link.split('/',-1)[-1].replace("polona?title=",'')

        if(recalc):
            self.recalculateMaxPoints()

    def recalculateMaxPoints(self):
        self._maxPoints = len(PolonaAPI.PolonaScan(self._title))*10
    