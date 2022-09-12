import json
import sys, os

import signature

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key

baseurl = key.baseurl
apiKey = key.admin_apkKey
secretkey = key.admin_secretKey

def listdomains():
    request = {"apiKey": apiKey, "response": "json", "command": "listDomains"}
    response = signature.requestsig(baseurl, secretkey, request)
    jsonData = json.loads(response)
    # print(jsonData)
    return jsonData

def getdefaultDomainID():
    res=listdomains()
    id=res["listdomainsresponse"]["domain"][0]["id"]
    print("Domain ID is : ",id)
    return id

getdefaultDomainID()