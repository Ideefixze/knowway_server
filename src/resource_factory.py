""" 
Simple implementation of Factory design pattern for determining which resource to make from link of form: <domain>/<type>?<data>
Made by: Dominik Zimny for a Software Engineering project.
"""

import resource
import json

class ResourceFactory(object):
    """
    Serves basic functionality for creating new Resources.
    """
    def ResourceFromLink(self, link):
        """
        Creates a new resource from link (<domain>/<type>?title=) and recalculates automatically point limit.
        """
        if("wiki?title=" in link):
            return resource.WikipediaResource(link)
        elif("polona?title=" in link):
            return resource.PolonaResource(link)
        else:
            return None

    def DetermineCategory(self, link):
        """
        Returns a category from link. 
        A shortcut function to skip making a new resource and then getting a category.
        """
        if("wiki?title=" in link):
            return 1
        elif("polona?title=" in link):
            return 2
        else:
            return 0

    
    def LoadResourceFromJSON(self, jsondata:str):
        """
        Loads a Resource from JSON and returns a corresponding type it doesnt recalculate points (to save a lot of time).
        jsondata is a string of jsonfile read by Simple_DBs
        """
        data = json.loads(jsondata)
        c = data['_categoryid']
        if(c==1):
            r = resource.WikipediaResource.loadFromJSON(data)
        elif(c==2):
            r = resource.PolonaResource.loadFromJSON(data)
        else:
            r = resource.Resource.loadFromJSON(data)
        return r
