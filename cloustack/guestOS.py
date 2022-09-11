import urllib.parse, urllib.request
import hashlib
import hmac
import base64
import json
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
import signature


class OS():

    def listostype(self):
        baseurl = key.baseurl
        secretkey = key.secretKey
        request = {"response": "json", "command": "listOsTypes", "keyword": "ubuntu", 'apikey': key.apiKey}
        response = signature.requestsig(baseurl, secretkey, request)
        return response

    def getubuntuID(self):
        response=self.listostype()
        response = json.loads(response)
        ubuntu1804LTSID = response["listostypesresponse"]["ostype"][16]["id"]
        print("18.04lts ID is ", ubuntu1804LTSID)
        return ubuntu1804LTSID
f = OS()
f.listostype()