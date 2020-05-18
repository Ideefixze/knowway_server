import user as u
import resource as r
import resource_factory as rf
import os
import shutil
import glob
import json
import threading

#Seconds between ranking updates
UPDATE_TIME = 30.0

def eqAuth(loadedUser, check):
    return check == loadedUser.getAuthCode()

def eqUsername(loadedUser, check):
    return check == loadedUser.getUsername()

def eqLogin(loadedUser, check):
    return (check[0] == loadedUser.getUsername() and check[1] == loadedUser.getPasswordHash())

class Simple_DB_User(object):

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.createRanking()

    def getUser(self, id):
        try:
            datafile = open(self.current_dir+"\\users\\"+str(id)+".txt", "r")
        except:
            #print("Wrong id!")
            return None
        else:
            user = u.User.loadFromJSON(datafile.read())
            datafile.close()
            return user

    def deleteUserData(self):
        files = glob.glob(self.current_dir+"\\users\\*")
        for f in files:
            os.remove(f)

    def scan(self, fun, check):
        for filename in os.listdir(self.current_dir+"\\users\\"):
            with open(os.path.join(self.current_dir+"\\users\\", filename), 'r') as f:
                loadedUser = u.User.loadFromJSON(f.read())
                if(fun(loadedUser, check)):
                    return loadedUser
        return None

    def saveUser(self, userdata):
        saveFile = open(self.current_dir+"\\users\\"+str(userdata.getId())+".txt", "w+")
        saveFile.write(userdata.serialize())
        saveFile.close()

    def createRanking(self,repeat=True):
        if(repeat):
            threading.Timer(UPDATE_TIME, self.createRanking).start()

        users = list()
        for filename in os.listdir(self.current_dir+"\\users\\"):
            with open(os.path.join(self.current_dir+"\\users\\", filename), 'r') as f:
                loadedUser = u.User.loadFromJSON(f.read())
                users.append([loadedUser.getUsername(), loadedUser.getTotalPoints()])
        
        users.sort(key=lambda x: x[1],reverse=True)
        saveFile = open(self.current_dir+"\\stats\\ranking.txt", "w+")
        saveFile.write(json.dumps(users))
        saveFile.close()


#Simple DB class for managing resource comments
class Simple_DB_Resource(object):

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.res_factory = rf.ResourceFactory()

        self.createRanking(1)
        self.createRanking(2)

    def getResource(self, cat, title):
        try:
            datafile = open(self.current_dir+"\\resources\\"+str(cat)+"\\"+str(title)+".txt", "r")
        except:
            #print("Unable to find: "+str(cat)+"\\"+str(title)+".txt!")
            return None
        else:
            res = self.res_factory.LoadResourceFromJSON(datafile.read())
            datafile.close()
            return res

    def deleteResourceData(self):
        try:
            shutil.rmtree(self.current_dir+"\\resources")
        except:
            return

    def saveResource(self, res):
        filename = self.current_dir+"\\resources\\"+str(res.getCategoryID())+"\\"+str(res.getTitle())+".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        try:
            savefile = open(filename, "w+")
        except:
            print("Unable to open: "+str(res.getCategoryID())+"\\"+str(res.getTitle())+".txt!")
            raise AssertionError
        else:
            savefile.write(res.serialize())
            savefile.close()

    def createRanking(self, catid, repeat=True):
        
        catid = str(catid)

        if(repeat):
            threading.Timer(UPDATE_TIME, self.createRanking, args=[catid]).start()

        res = list()
        try:
            for filename in os.listdir(self.current_dir+"\\resources\\"+catid+"\\"):
                with open(os.path.join(self.current_dir+"\\resources\\"+catid+"\\", filename), 'r') as f:
                    loadedRes = self.res_factory.LoadResourceFromJSON(f.read())
                    res.append([loadedRes.getLink(), loadedRes.getTitle(), loadedRes.getVisits()])
        except:
            return

        res.sort(key=lambda x: x[2],reverse=True)
        saveFile = open(self.current_dir+"\\stats\\res_ranking"+catid+".txt", "w+")
        saveFile.write(json.dumps(res))
        saveFile.close()

    def recommendFromCat(self, n, cat):
        """Returns an n'th item from ranking list of resources."""
        try:
            file = open(self.current_dir+"\\stats\\res_ranking"+str(cat)+".txt", "r")
        except:
            return ["","",0]
        else:
            data = json.loads(file.read())
            file.close()
            try:
                return data[n]
            except:
                return ["","",0]

