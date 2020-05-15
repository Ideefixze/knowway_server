import resource
import json

class ResourceFactory(object):

    def ResourceFromLink(self, link):
        if("wiki?title=" in link):
            return resource.WikipediaResource(link)
        elif("polona?title=" in link):
            return resource.PolonaResource(link)
        else:
            return None

    def DetermineCategory(self, link):
        if("wiki?title=" in link):
            return 1
        elif("polona?title=" in link):
            return 2
        else:
            return 0

    #Loads a Resource from JSON
    #WARNING: it returs a base class rather than a WikipediaResource/PolonaResource
    #use only for load/save purposes
    #it is much faster solution than creating a new XResource from link in json
    #because when you make a new specific Resource it recalculates maxPoints and that take a lot of time
    def LoadResourceFromJSON(self, jsondata):
        data = json.loads(jsondata)
        r = resource.Resource.loadFromJSON(data)
        return r