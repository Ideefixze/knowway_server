import user as u
import socket, errno
import simple_db
import resource_factory as rf
from multiprocessing import Process
import resource as r
import multiprocessing
import os
import glob
import threading
import routes
import hasher
import urllib.parse

current_dir = os.path.dirname(__file__)

#Server - singleton.
class Server(object):
    __instance = None

    @staticmethod
    def getInstance():
        if Server.__instance == None:
            return None
        return Server.__instance

    def __new__(cls, *args, **kwargs):
        if Server.__instance == None:
            Server.__instance = object.__new__(cls)
            return Server.__instance
        else:
            Server.__instance.resetServer()
            return Server.__instance
            
    def __init__(self, ip, port):
        Server.__instance = self
        routes.SERVER = self

        self.ip = ip
        self.port = port
        self.servproc = threading.Thread(target=routes.app.run, args = [ip,port,False])
        self.udb = simple_db.Simple_DB_User()
        self.rdb = simple_db.Simple_DB_Resource()
        self.resfactory = rf.ResourceFactory()
        #self.servproc.setDaemon(True)

    def runServer(self):
        print("Starting up server...")
        self.servproc.start()

    def running(self):
        return self.servproc.is_alive()

    def totalUserCount(self):
        path, dirs, files = (os.walk(current_dir+"\\users\\")).__next__()
        file_count = len(files)
        return file_count

    def registerNewUser(self, username, passwordHash):
        
        foundUser = self.scanUsername(username)

        if(foundUser is not None): 
            return foundUser.getId()

        i = self.totalUserCount()
        newuser = u.User.registerNewUser(i, username, passwordHash)
        self.saveUser(newuser)
        return i

    #Wrapper methods that were here are now defined in Simple_DB class
    def saveUser(self, userdata):
        self.udb.saveUser(userdata)

    def scanUsername(self, username):
        return self.udb.scan(simple_db.eqUsername, username)

    def scanLogin(self, username, passwordhash):
        return self.udb.scan(simple_db.eqLogin, [username,passwordhash])

    def scanAuth(self, auth):
        return self.udb.scan(simple_db.eqAuth,auth)

    def getUser(self, id):
        return self.udb.getUser(id)

    def resetServer(self):
        self.udb.deleteUserData()
        self.rdb.deleteResourceData()

    #Given the direct link, find local resource in data base
    def getResource(self, link):
        link = link.split("&page=",1)[0] 
        title = link.split("?title=",1)[1]
        title = urllib.parse.unquote(title) 
        return self.rdb.getResource(self.resfactory.DetermineCategory(link), title)

    def addPointsForUser(self, uid, auth, link, time):
        #Open file with user data
        try:
            f = open(current_dir+"\\users\\"+str(uid)+".txt", 'r')
        except:
            return [0,0]
        else:
            #Recreate user in memory from JSON
            loadedUser = u.User.loadFromJSON(f.read())
            #If given auth is valid with loaded user of given id and time is not negative
            if(auth == loadedUser.getAuthCode() and time >=0.0):
                #Find resource locally, if not found, create one and save it locally
                localres = self.getResource(link)
                if(localres is None):
                    res = self.resfactory.ResourceFromLink(link)
                    res.addVisit()
                    self.rdb.saveResource(res)
                else:
                    res = localres
                    if(loadedUser.getResourcePointsForResource(link)[0]==0):
                        localres.addVisit()
                        self.rdb.saveResource(localres)

                if(res is not None):
                    loadedUser.addPointsForResource(link, time*15, res.getMaxPoints())
                else:
                    return [0,0]
            f.close()
            #Apply changes to our user and save it locally
            self.saveUser(loadedUser)
            return loadedUser.getResourcePointsForResource(link)

    def addComment(self, uid, content, link):

        localres = self.getResource(link)
        if(localres is None):
            localres = self.resfactory.ResourceFromLink(link)
            self.rdb.saveResource(localres)
        try:
            id = localres.getComments()[-1].getCommentTuple[0]+1
        except:
            id=0

        localres.addComment(id, uid, content)
        self.rdb.saveResource(localres)

    #given the comment list of [comment_id, user_id, content] create [username, content] for displaying
    def getResourceFinalCommentList(self, comments):
        finalcommentlist = []
        for c in comments:
            finalcomment = []
            try:
                finalcomment.append(self.getUser(c.getCommentTuple()[1]).getUsername())
            except:
                finalcomment.append("Anonymous")

            finalcomment.append(c.getCommentTuple()[2])
            finalcommentlist.append(finalcomment)

        return finalcommentlist



if __name__ == '__main__':
    s = Server("127.0.0.1", 5000)
    #s.resetServer()
    #for i in range(0,1000):
        #s.registerNewUser(str(str(i)+"user"), str(hash("password")))
    s.runServer()