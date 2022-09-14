import urllib.parse, urllib.request
import hashlib
import hmac
import base64
import json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
import signature
from bs4 import BeautifulSoup

def console(vmid):
    baseurl=key.baseurl
    baseurl='http://211.197.83.186:8080/client/console?'            #다른 메소드들과 달리 마지막 api? 가 아닌 console?이다.
    apiKey=key.apiKey
    secretkey=key.secretKey

    # baseurl='http://10.125.70.28:8080/client/api?'
    request= {"vm":vmid,"apiKey": apiKey, "response": "json", "cmd": "access"}

    response=signature.requestsig(baseurl,secretkey,request)

    htmlData = BeautifulSoup(response,features="html.parser")
    console_url_body=htmlData.html.frameset.frame['src']
    console_url="http:"+console_url_body
    print("Console URL is : \n",console_url)
    return console_url

console("219313e8-3588-4b5e-a299-37ce35463035")