import urllib.parse, urllib.request
import hashlib
import hmac
import base64
import json
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
import signature

def console(vmid):
    baseurl=key.baseurl
    baseurl='http://211.197.83.186:8080/client/console?'            #다른 메소드들과 달리 마지막 api? 가 아닌 console?이다.
    apiKey=key.apiKey
    secretkey=key.secretKey

    # baseurl='http://10.125.70.28:8080/client/api?'
    request= {"vm":vmid,"apiKey": apiKey, "response": "json", "cmd": "access"}

    response=signature.requestsig(baseurl,secretkey,request)
    print(response)
    # print(json.dumps(res,indent=2))
    # print(req)
    # jsonData=json.loads(response)
    # print(jsonData["listserviceofferingsresponse"]["serviceoffering"][0]["id"])
    # return jsonData["listserviceofferingsresponse"]["serviceoffering"][0]["id"]
#vm=29603248-6d8a-4582-aa9a-4d1bfb4d7714&apikey=3NRrdrhDTwggQ_oQny11dD39-XRWJxCd0dh2xqtMNShrz_jb4ZdhHtmRh7NYiOfRzLNwPcBVAfT9FHh9v96vzg&response=json&signature=u4c7QZNQNcN+2s3fhRNSHTyl7+Q=
#http://211.197.83.186:8080/client/api?apiKey=YWYjj6hm1w3SE802vm21xfWl4gFq-K0WuQNkCFx7b7hUtfkqmgXzFLZ_G9k8xDST4gU6U-Fyh_gN9Ft17Xcdww&response=json&cmd=access&vm=c80d6745-7714-4bf7-81ad-c37ff0d71fed&signature=crRjFnecqtHWPfcZnfUTsc4RUks%3D
# console("c80d6745-7714-4bf7-81ad-c37ff0d71fed")