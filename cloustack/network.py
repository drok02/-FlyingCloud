import json
import os
import sys

import signature

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
defaultNet="net_test"

class net():

    def listnetworks(self):
        baseurl=key.baseurl
        apiKey=key.apiKey
        secretkey=key.secretKey

        request= {"apiKey": apiKey, "response": "json", "command": "listNetworks"}
        response=signature.requestsig(baseurl,secretkey,request)
        return response
        # jsonData=json.loads(response)
        # print(jsonData)
        # return jsonData
    def getnetid(self):
        res=self.listnetworks()
        jsonData = json.loads(res)
        id=jsonData["listnetworksresponse"]["network"][0]["id"]
        print("network id is "+id)
        return id
# f=net()
# f.getlistid()
