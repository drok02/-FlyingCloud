import urllib
import urllib.parse
import urllib.request
import hashlib
import hmac
import base64
import json
import sys, os

import signature

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key

defaultZone = "zone1"


class zone():

    def listzone(self, zonename=defaultZone):
        baseurl = key.baseurl
        apiKey = key.apiKey
        secretkey = key.secretKey

        request = {"apiKey": apiKey, "response": "json", "command": "listZones", "name": zonename}
        response = signature.requestsig(baseurl, secretkey, request)
        jsonData = json.loads(response)
        # print(jsonData)
        return jsonData

    def getZoneID(self, zonename=defaultZone):
        zone = self.listzone(zonename)
        id = zone["listzonesresponse"]["zone"][0]["id"]
        print(zonename + " id is " + id)
        return id

# f=zone()
# # p=f.listzone()
# # print(p)
# f.getZoneID()
