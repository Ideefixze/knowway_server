""" 
User class contains data about single user and all nescessary functionalities
Made by: Dominik Zimny for a Software Engineering project.
"""
import json
import hasher

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
        """From jsonSerial string of json format loads a new User and returns them."""
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
        """Creates a new user from the given data."""
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
        """Returns a tuple from the resourcePoints dict [points,maxpoints]. If it doesn't exist yet return [0,0]."""
        if(link in self.__resourcePoints.keys()):
            return self.__resourcePoints[link]
        else:
            return [0,0]

    def __str__(self):
        return "("+self.__username+") has got "+str(self.__totalPoints)+" points."

    def serialize(self):
        """Serializes User as a JSON string."""
        return json.dumps(self, default=lambda  o: o.__dict__, sort_keys=False, indent=4)

    def __eq__(self, other):
        return hash(self.serialize())==hash(other.serialize())

    def addPointsForResource(self, link, points, maxPoints):
        """Adds points for a user for a resource with a given link. Makes sure that points will not be greater than maxPoints."""
        if(link in self.__resourcePoints):
            self.__resourcePoints[link][0] += points
            self.__resourcePoints[link][1] = maxPoints
        else:
            self.__resourcePoints[link] = [points, maxPoints]
            
        self.__totalPoints += points

        #If maximum points for the resource has been obtained, remove overflow
        if(self.__resourcePoints[link][0]>self.__resourcePoints[link][1]):
            self.__totalPoints -= self.__resourcePoints[link][0]-self.__resourcePoints[link][1] 
            self.__resourcePoints[link][0]=self.__resourcePoints[link][1] 
            



if( __name__ == '__main__'):
    newuser1 = User.registerNewUser(10,"Jordan","123def")
    newuser2 = User.loadFromJSON(newuser1.serialize())
    print(newuser1.serialize())
    newuser2.setUsername("Niekowalski")
    print(newuser2.serialize())