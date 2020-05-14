import json
import user
import requests
import wikipedia
import urllib.parse
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
        self.recalculateMaxPoints()
        self._visits = 0

    def getLink(self):
        return self._link

    def getTitle(self):
        return None
    
    def getCategoryID(self):
        return self._categoryid

    def getMaxPoints(self):
        return self._maxPoints

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

    def __init__(self, link,catid=1):
        self._title = link.split('/',-1)[-1].replace("wiki?title=",'')
        self._title = self._title.replace('+',' ')
        self._title = urllib.parse.unquote(self._title)
       
        try:
            w = wikipedia.WikipediaPage(self._title)
        except:
            raise(AssertionError)
        else:
            #print("created new wiki art. : ", self._title)
            super().__init__(link, catid)

    def getTitle(self):
        return self._title

    def recalculateMaxPoints(self):
        wikiartContent = wikipedia.page(self.getTitle()).content
        length = len(wikiartContent)
        self._maxPoints = 100 + int(length/100)

class PolonaResource(Resource):

    def __init__(self, link,catid=2):
        #print(link.split('/',-1))
        if("polona.pl" not in link.split('/',-1)):
            raise(AssertionError)
        super().__init__(link, catid)

    def getPolonaID(self) -> str:
        return (self._link.split('/', -1)[4].split(',')[-1])

    def recalculateMaxPoints(self):
        URL='https://polona.pl/api/entities/'+self.getPolonaID()+'/'
        r = requests.get(URL, {})
        data = r.json()
        self._maxPoints = len(data['scans'])*10
    

#res1 = PolonaResource("https://polona.pl/item/pisma-adama-mickiewicza-t-5,NTE5MTk1/6/#info:metadata")
#print (res1.getPolonaID())
#print (res1.getMaxPoints())

res2 = WikipediaResource("http://127.0.0.1:5000/wiki?title=France")
res3 = Resource("test.pl",12)
print(res2.serialize())
print(res3.serialize())