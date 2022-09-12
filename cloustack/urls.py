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
admin_apkKey     =      "YWYjj6hm1w3SE802vm21xfWl4gFq-K0WuQNkCFx7b7hUtfkqmgXzFLZ_G9k8xDST4gU6U-Fyh_gN9Ft17Xcdww"
admin_secretKey    =    "NcPKi1iYFdOT6G15aZwFLBcpwMdswBpbzVCyQoNWKXnBNXIuXR029271FMMEdIzz29eHA2CfOuoWnS9EVg46cg"
user_apiKey        =    "O5hI1EVpdHRADdqJX97kIBVYcgGsANjVQ1RptPB1SbJcdbVFxjdvnzr1W6GQLDXO7lWErTpSvGVOvE2yZMXkGg"
user_secretKey     =    "tJ6hQoC0f3d5XWP7qa7xfrBAJ0hp5-GtZNPEiZWi1_5ffPdH_lM7HSkQ5q2-fIjocMCVVtbQAXpZ7Vk0op--Bw"
baseurl='http://211.197.83.186:8080/client/api?'


apiKey= admin_apkKey
secretKey= admin_secretKey
roleID="860a51d5-2bab-11ed-94e7-08002767856c"
def getuserkey(userid):

    # baseurl='http://10.125.70.28:8080/client/api?'
    request= {"apikey": apiKey, "response": "json", "command": "getUserKeys", "id": userid}

    signature.requestsig(baseurl,secretKey,request)

# getuserkey('d618c5e3-c9df-4088-834b-6b77889a0360')


