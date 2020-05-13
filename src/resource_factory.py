import resource
import json

class ResourceFactory(object):

    def ResourceFromLink(self, link):
        if("wiki?title=" in link):
            return resource.WikipediaResource(link)
        else:
            return None

    def LoadResourceFromJSON(self, jsondata):
        data = json.loads(jsondata)
        r = self.ResourceFromLink(data["_link"])
        r.setComments(data["_comments"])
        return r