import user as u
import resource as r
import resource_factory as rf
import os
import shutil
import glob
import json

def eqAuth(loadedUser, check):
    return check == loadedUser.getAuthCode()

def eqUsername(loadedUser, check):
    return check == loadedUser.getUsername()

def eqLogin(loadedUser, check):
    return (check[0] == loadedUser.getUsername() and check[1] == loadedUser.getPasswordHash())

class Simple_DB_User(object):

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

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

#Simple DB class for managing resource comments
class Simple_DB_Resource(object):

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.res_factory = rf.ResourceFactory()

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
        shutil.rmtree(self.current_dir+"\\resources")

    def saveResource(self, res):
        try:
            savefile = open(self.current_dir+"\\resources\\"+str(res.getCategoryID())+"\\"+str(res.getTitle())+".txt", "w+")
        except:
            print("Unable to find: "+str(res.getCategoryID())+"\\"+str(res.getTitle())+".txt!")
            raise AssertionError
        else:
            savefile.write(res.serialize())
            savefile.close()