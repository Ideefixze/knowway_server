import json
import hasher
#
# User class 
# contains data about single user and all nescessary functionalities
#
class User:
    def __init__(self, id, username, passwordHash, resourcePoints, totalPoints, authCode):
        self.__id=id
        self.__username=username
        self.__passwordHash=passwordHash
        self.__resourcePoints= resourcePoints
        self.__totalPoints=totalPoints
        self.__authCode=authCode
    
    @classmethod
    def loadFromJSON(cls, jsonSerial):
        data = json.loads(jsonSerial)
        id = data["_User__id"]
        username = data["_User__username"]
        passwordHash = data["_User__passwordHash"]
        resourcePoints= data["_User__resourcePoints"]
        totalPoints=data["_User__totalPoints"]
        authCode=data["_User__authCode"]
        return cls(id, username, passwordHash, resourcePoints, totalPoints, authCode)

    @classmethod 
    def registerNewUser(cls, uid, uusername, upasswordHash):
        id=uid
        username=uusername
        passwordHash=upasswordHash
        resourcePoints = dict()
        totalPoints = 0
        authCode = hasher.hash(str(id)+uusername+upasswordHash)
        return cls(id,username,passwordHash,resourcePoints,totalPoints,authCode)

    def setUsername(self, username):
        self.__username = username
    
    def getUsername(self):
        return self.__username

    def getPasswordHash(self):
        return self.__passwordHash

    def getId(self):
        return self.__id

    def getTotalPoints(self):
        return self.__totalPoints
    
    def getAuthCode(self):
        return self.__authCode

    def getResourcePointsDict(self):
        return self.__resourcePoints

    def getResourcePointsForResource(self, link):
        if(link in self.__resourcePoints.keys()):
            return self.__resourcePoints[link]
        else:
            return 0

    def printDebugInfo(self):
        print("["+str(self.__id)+"] Username: "+self.__username +", auth ("+self.__authCode+"), passwordHash = "+self.__passwordHash)
        print("Total points: "+str(self.__totalPoints) + ", in particular: ")
        print(self.__resourcePoints)

    def __str__(self):
        return "("+self.__username+") has got "+str(self.__totalPoints)+" points."

    def serialize(self):
        return json.dumps(self, default=lambda  o: o.__dict__, sort_keys=False, indent=4)

    def __eq__(self, other):
        return hash(self.serialize())==hash(other.serialize())

    def addPointsForResource(self, link, points, maxPoints):

        if(link in self.__resourcePoints):
            self.__resourcePoints[link][0] = points + self.__resourcePoints[link][0]
            self.__resourcePoints[link][1] = maxPoints
        else:
            self.__resourcePoints[link] = [points, maxPoints]

        #If maximum points for resource has been obtained, reduce overflow
        if(self.__resourcePoints[link][0]>self.__resourcePoints[link][1]):
            self.__resourcePoints[link][0]=self.__resourcePoints[link][1] 



if( __name__ == '__main__'):
    newuser1 = User.registerNewUser(10,"Jordan","123def")
    newuser2 = User.loadFromJSON(newuser1.serialize())
    print(newuser1.serialize())
    newuser2.setUsername("Niekowalski")
    print(newuser2.serialize())