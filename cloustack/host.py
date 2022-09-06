import json
import os
import sys

import signature

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
defaulthost="localhost.cloud.priv"

class host():

    def listhosts(self,hostname=defaulthost):
        baseurl=key.baseurl
        apiKey=key.apiKey
        secretkey=key.secretKey

        request= {"apiKey": apiKey, "response": "json", "command": "listHosts", "name": hostname}
        response=signature.requestsig(baseurl,secretkey,request)
        return response
        # jsonData=json.loads(response)
        # print(jsonData)
        # return jsonData
    def gethostid(self,hostname=defaulthost):
        res=self.listhosts(hostname)
        jsonData = json.loads(res)
        id=jsonData["listhostsresponse"]["host"][0]["id"]
        print("host"+hostname+"'s id is "+id)
        return id
f=host()
f.gethostid()