import base64
import hashlib
import hmac
import os
import sys
import urllib
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urllib.parse
import urllib.request
import sys,os
import signature

baseurl='http://211.197.83.186:8080/client/api?'
apiKey="YWYjj6hm1w3SE802vm21xfWl4gFq-K0WuQNkCFx7b7hUtfkqmgXzFLZ_G9k8xDST4gU6U-Fyh_gN9Ft17Xcdww"
secretKey="NcPKi1iYFdOT6G15aZwFLBcpwMdswBpbzVCyQoNWKXnBNXIuXR029271FMMEdIzz29eHA2CfOuoWnS9EVg46cg"

def getuserkey(userid):

    # baseurl='http://10.125.70.28:8080/client/api?'
    request= {"apikey": apiKey, "response": "json", "command": "getUserKeys", "id": userid}

    signature.requestsig(baseurl,secretKey,request)

getuserkey('d618c5e3-c9df-4088-834b-6b77889a0360')