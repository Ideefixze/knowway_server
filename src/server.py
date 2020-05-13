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

    def addPointsForUser(self, uid, auth, link, time):
        try:
            f = open(current_dir+"\\users\\"+str(uid)+".txt", 'r')
        except:
            return [0,0]
        else:
            loadedUser = u.User.loadFromJSON(f.read())
            if(auth == loadedUser.getAuthCode()):
                if(time>=0.0):
                    res = self.resfactory.ResourceFromLink(link)
                    localres = self.rdb.getResource(res.getCategoryID(), res.getTitle())
                    if(localres is None):
                        self.rdb.saveResource(res)
                    #print(res)
                    if(res is not None):
                        loadedUser.addPointsForResource(link, time*15, res.getMaxPoints())
                    else:
                        return [0,0]
            f.close()
            self.saveUser(loadedUser)
            return loadedUser.getResourcePointsForResource(link)

    def addComment(self, uid, content, link):
        res = self.resfactory.ResourceFromLink(link)
        localres = self.rdb.getResource(res.getCategoryID(), res.getTitle())
        localres.addComment(len(localres.getComments()), uid, content)
        self.rdb.saveResource(localres)




if __name__ == '__main__':
    #print(hasher.hash("zimny"))
    #app.run("127.0.0.1",5000,debug=True)
    
    s = Server("127.0.0.1", 5000)
    #s.resetServer()
    #for i in range(0,1000):
        #s.registerNewUser(str(str(i)+"user"), str(hash("password")))
    s.runServer()
    #print(s.totalUserCount())
    #s.registerNewUser("chuj", "abcd")
    #i = s.registerNewUser("chujdwa","chuju")
    #s.registerNewUser("aaaa","chuju")
    #print(i)
    #print(s.getUser(i).getAuthCode())
    #print(s.addPointsForUser(i, s.getUser(i).getAuthCode(),"https://polona.pl/item/pisma-adama-mickiewicza-t-5,NTE5MTk1/", 10.0))
    #s = Server("127.0.0.1", 5000)