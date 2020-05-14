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
        r.setVisits(data['_visits'])
        for c in data["_comments"]:
            r.addComment(c['_Comment__id'], c['_Comment__who'], c['_Comment__content'])
        return r