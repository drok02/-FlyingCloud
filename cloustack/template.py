import base64
import hmac
import os
import sys

from requests.auth import HTTPBasicAuth

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urls as key
import json
import signature
import urllib.parse, urllib.request
import hashlib
import webbrowser
import urllib.parse
import urllib.request
import requests

class Template():
    baseurl = key.baseurl
    apikey = key.apiKey
    secretkey = key.secretKey


    #인터넷상의 이미지 파일로 템플릿 생성
    def regiTemplate(self, name, url, osTypeid, zoneid):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey

        request = {"apiKey": apikey, "response": "json", "command": "registerTemplate",
                   "displaytext": name, "format": "qcow2", "hypervisor": "kvm",
                   "name": name, "url": url, "ostypeid": osTypeid, "zoneid": zoneid}
        request_str = '&'.join(['='.join([k, urllib.parse.quote_plus(request[k])]) for k in request.keys()])
        sig_str = '&'.join(
            ['='.join([k.lower(), urllib.parse.quote_plus(request[k].lower().replace('+', '%20'))]) for k in
             sorted(request)])
        sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1)
        sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()
        sig = base64.encodebytes(hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest())
        sig = base64.encodebytes(
            hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip()
        sig = urllib.parse.quote_plus(base64.encodebytes(
            hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip())
        req = baseurl + request_str + '&signature=' + sig
        print(req)
        # reque=urllib.request.Request(req)
        # data=urllib.request.urlopen(reque).read()
        # print(data)

        # res = urllib.request.urlopen(req)
        # print(res)

        # req=signature.requestsig(baseurl, secretkey, request)
        # print(res.read())

        webbrowser.open(req)
        # get=requests.get(req)
        # print(get)

    def listTemplate(self):
        baseurl = key.baseurl
        apiKey = key.admin_apkKey
        secretKey = key.admin_secretKey
        request = {}
        request['command'] = 'listTemplates'
        request['templatefilter'] = 'selfexecutable'
        request['response'] = 'json'
        request['apikey'] = apiKey
        secretkey = secretKey
        response = signature.requestsig(baseurl,secretkey,request)
        jsonData = json.loads(response)
        print(response)
        return jsonData

    def copyTemplate(self):
        baseurl = key.baseurl
        secretkey = key.secretKey
        request = {}
        request['command'] = 'copyTemplate'
        request['id'] = '585e06bb-fbb5-11ec-8775-08002702dd0b'
        request['destzoneid'] = '8c7c81c5-4379-4fd2-9153-64f17243aa9c'
        request['response'] = 'json'
        request['apikey'] = key.apiKey

        req=signature.requestsig(baseurl,secretkey,request)
        # print(response)
        print(req)

    def getCentosID(self):
        id = self.listTemplate()["listtemplatesresponse"]["template"][0]["id"]
        print(id)
        return id

    def getTemplateIDfromAccount(self,name):
        baseurl = key.baseurl
        apiKey = key.admin_apkKey
        secretKey = key.admin_secretKey
        # baseurl='http://10.125.70.28:8080/client/api?'
        request = {}
        request['command'] = 'listTemplates'
        request['templatefilter'] = 'selfexecutable'
        request['name'] = name
        request['response'] = 'json'
        request['apikey'] = apiKey
        secretkey = secretKey
        response = signature.requestsig(baseurl, secretkey, request)
        jsonData = json.loads(response)
        templateID=jsonData["listtemplatesresponse"]["template"][0]["id"]
        print("Template id is ",templateID)
        return templateID

    def deleteTemplate(self,id):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey

        request = {"apiKey": apikey, "response": "json", "command": "deleteTemplate",
                   "id": id}

        signature.requestsig(baseurl, secretkey, request)

    #현재 템플릿의 상태 반환
    def getTemplatestatus(self,name):
        baseurl = key.baseurl
        apiKey = key.admin_apkKey
        secretKey = key.admin_secretKey

        # baseurl='http://10.125.70.28:8080/client/api?'
        request = {}
        request['command'] = 'listTemplates'
        request['templatefilter'] = 'selfexecutable'
        request['name'] = name
        request['response'] = 'json'
        request['apikey'] = apiKey
        secretkey = secretKey
        response = signature.requestsig(baseurl, secretkey, request)
        jsonData = json.loads(response)
        status=jsonData["listtemplatesresponse"]["template"][0]["status"]
        print("Template status is ",status)
        return status
    #"virtualmachineid": vmid, "domainid":"24efff21-2bab-11ed-94e7-08002767856c","volumeid":volid

    #VM으로부터 템플릿 생성
    def createTemplate(self, templatename, osTypeid, volid):
        baseurl = key.baseurl
        apiKey = key.apiKey
        secretKey = key.secretKey
        request = {"apiKey": apiKey, "response": "json", "command": "createTemplate","displaytext":templatename,
                   "name": templatename, "ostypeid": osTypeid,
                   "volumeid": volid
                   }
        response = signature.requestsig(baseurl, secretKey, request)
        response_json=json.loads(response)
        templateid=response_json["createtemplateresponse"]["id"]
        print("Template Create is complete. id is ",templateid)
        return templateid


    #템플릿을 추출가능하도록 속성 업데이트
    def updateextractable(self,templateID):
        # updateTemplatePermissions
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "updateTemplatePermissions",
                   "id": templateID ,"isextractable":"true"}
        res=signature.requestsig(baseurl, secretkey, request)
        print(res)

    # 템플릿 추출
    def extractTemplate(self, templateID):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "extractTemplate",
                   "id": templateID, "mode": "download", "zoneid": "e4ebd8fa-f0af-46b0-ac20-0acc3863b3d1"}
        # signature.requestsig(baseurl, secretkey, request)
        request_str = '&'.join(['='.join([k, urllib.parse.quote_plus(request[k])]) for k in request.keys()])
        sig_str = '&'.join(
            ['='.join([k.lower(), urllib.parse.quote_plus(request[k].lower().replace('+', '%20'))]) for k in
             sorted(request)])
        sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1)
        sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()
        sig = base64.encodebytes(hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest())
        sig = base64.encodebytes(
            hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip()
        sig = urllib.parse.quote_plus(base64.encodebytes(
            hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip())
        req = baseurl + request_str + '&signature=' + sig
        # request["signature"]=sig
        authParams = HTTPBasicAuth('admin', 'password')
        print(req)
        res = requests.get(req)
        res = res.json()
        jobid = res["extracttemplateresponse"]["jobid"]
        # print(req)
        print("job id is ", jobid)
        # res = urllib.request.urlopen(req)
        # response = res.read()
        # header=res.getheader('content-type')
        # print("response is :", response)
        # print("header is : \n",header)
        return jobid

    # job 상태 반환
    def queryjobresult(self, TemplateJobID):
        #         queryAsyncJobResult
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "queryAsyncJobResult", "jobid": TemplateJobID}

        res = signature.requestsig(baseurl, secretkey, request)
        print(res)
        return res

    # 추출한 Template을 다운로드하기 위한 url 반환
    def getTemplateDownURL(self, TemplateJobID):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "queryAsyncJobResult", "jobid": TemplateJobID}
        response = signature.requestsig(baseurl, secretkey, request)
        resJson = json.loads(response)
        url = resJson['queryasyncjobresultresponse']['jobresult']['template']['url']
        print("DownloadURL is : \n", url)
        return url

    def listCertificates(self):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listTemplatePermissions",
                   "id": "8d3d8fb5-4b02-4557-abd2-dcafc474b3a6"}
        signature.requestsig(baseurl, secretkey, request)

    def privisionCertificate(self,hostid):
        #
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "provisionCertificate",
                   "hostid": hostid}
        signature.requestsig(baseurl, secretkey, request)

    def listCert(self):

        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listCaCertificate"}
        signature.requestsig(baseurl, secretkey, request)

    def listCAProvider(self):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listCAProviders"}
        signature.requestsig(baseurl, secretkey, request)

    def listTags(self):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listTags","account":"admin"}

        signature.requestsig(baseurl, secretkey, request)

    def listApis(self):
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listApis","name":"extractTemplate"}

        signature.requestsig(baseurl, secretkey, request)


    def listAsyncJob(self):
        #listAsyncJobs
        baseurl = key.baseurl
        apikey = key.apiKey
        secretkey = key.secretKey
        request = {"apiKey": apikey, "response": "json", "command": "listApis", "name": "listAsyncJobs"}

        signature.requestsig(baseurl, secretkey, request)



# f=Template()
# f.regiTemplate(templatename,"https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img",ubuntu,zoneid)

# f.getTemplateDownURL("1f522d2d-4ed3-4b11-86a7-54bc2d63d4ff")

# f.createTemplate("restore_snapshot_ubuntu","8eef80ca-2bab-11ed-94e7-08002767856c","0478cea7-619c-490c-8fd8-2183bca8e106")
#centos 5.5 ostype id is 2544d7e0-2bab-11ed-94e7-08002767856c
#ubuntu 3 template id is 8d3d8fb5-4b02-4557-abd2-dcafc474b3a6
# f.updateextractable()
# f.getTemplatestatus("bong")


# f.extractTemplate("0a241840-25ac-43be-9d99-9adc54b14381")
# f.queryjobresult()
# f.listCertificates()
# # f.regiTemplate("op
# f.privisionCertificate("c5637606-7d9a-4fdf-aa18-3815616e3ecd")
# enstack_image","http://3.39.193.17:8000/media/img-files/backup
# f.listApis()
# 0903.qcow2","a20b6938-286a-11ed-bfb3-0800277c0f4b")


# # f.listTemplate()
# z=zone.getZone1ID()
# f.listAsyncJob()

# f.regiTemplate("imagebackupapitest2","http://3.39.193.17:8000/media/img-files/backup0903.qcow2","8eef80ca-2bab-11ed-94e7-08002767856c",z)