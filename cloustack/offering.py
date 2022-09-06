import urllib.parse, urllib.request
import hashlib
import hmac
import base64
import json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
import signature
class Offering():

    def listServiceOfferings(self):
        baseurl=key.baseurl
        apiKey=key.apiKey
        secretkey=key.secretKey

        # baseurl='http://10.125.70.28:8080/client/api?'
        request= {"apiKey": apiKey, "response": "json", "command": "listServiceOfferings"}
        # secretKey="2yLo8pQRIpwBW4jOwgPd6WVKBmi3q3gosi2llVa5h3JOVZKBHvbbLdc_mbaYEtKIGP5N_mmfnJeNW1maP4AKew"
        # request_str='&'.join(['='.join([k,urllib.parse.quote_plus(request[k])]) for k in request.keys()])
        # sig_str='&'.join(['='.join([k.lower(),urllib.parse.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request)])
        # sig=hmac.new(secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1)
        # sig=hmac.new(secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()
        # sig=base64.encodebytes(hmac.new(secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest())
        # sig=base64.encodebytes(hmac.new(secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()).strip()
        # sig=urllib.parse.quote_plus(base64.encodebytes(hmac.new(secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()).strip())
        # req=baseurl+request_str+'&signature='+sig
        # print("request URL is \n1",json.dumps(req,indent="\t"))
        # print()
        # res=urllib.request.urlopen(req)
        response=signature.requestsig(baseurl,secretkey,request)
        print(type(response))
        # print(response)
        # print(json.dumps(res,indent=2))
        # print(req)
        jsonData=json.loads(response)
        print(jsonData["listserviceofferingsresponse"]["serviceoffering"][0]["id"])
        return jsonData["listserviceofferingsresponse"]["serviceoffering"][0]["id"]
#
# f=Offering()
# f.listServiceOfferings()
