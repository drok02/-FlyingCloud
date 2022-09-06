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


f = OS()
f.listostype()