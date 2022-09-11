import json
import urllib
import urllib.parse
import urllib.request
import hashlib
import hmac
import base64
import sys
# sys.path.append('./ServiceOffering')
import signature
import urls as key
# from .ServiceOffering import listServiceOfferings as service


import offering as listOffer
# import Zone.listZone
import zone
import network
import host
class VM():

    def deployVM(self,templateID,vmname="test"):
        baseurl=key.baseurl
        apiKey=key.apiKey
        secretkey=key.secretKey
        z=zone.zone()
        n=network.net()
        h=host.host()
        # serviceofferingId = "6906780f-3625-46ea-86f0-5ed272dc2f73"
        offering=listOffer.Offering()
        serviceofferingId = offering.listServiceOfferings()
        # baseurl='http://10.125.70.28:8080/client/api?'

        #"hostid": h.gethostid(),"startvm": "false",
        request= {"apiKey": apiKey, "response": "json", "command": "deployVirtualMachine",
                  "networkids": n.getnetid(), 'serviceofferingId': serviceofferingId,
                  'templateId': templateID, 'zoneId': z.getZoneID(),
                  "displayname":vmname,"name":vmname,"domainid":"24efff21-2bab-11ed-94e7-08002767856c",
                  "account":"admin", "hostid":"c5637606-7d9a-4fdf-aa18-3815616e3ecd"
                  }

        response= signature.requestsig(baseurl,secretkey,request)
        # print(response)
        return response

    def getVMid(self,vmname):
        request = {"apiKey": key.apiKey, "response": "json", "command": "listVirtualMachines",
                   "name": vmname}
        response = signature.requestsig(key.baseurl, key.secretKey, request)
        response= json.loads(response)
        vmid=response["listvirtualmachinesresponse"]["virtualmachine"][0]["id"]
        print("VM ID is ",vmid)
        return vmid

    def startVM(self,vmid):
        request = {"apiKey": key.apiKey, "response": "json", "command": "startVirtualMachine",
                   "id": vmid}
        response = signature.requestsig(key.baseurl, key.secretKey, request)
        return response


    def stopVM(self,vmid):
        request = {"apiKey": key.apiKey, "response": "json", "command": "stopVirtualMachine",
                   "id": vmid}
        response = signature.requestsig(key.baseurl, key.secretKey, request)
        return response

    def deleteVM(self,vmid):

        request = {"apiKey": key.apiKey, "response": "json", "command": "destroyVirtualMachine",
                   "id": vmid, "expunge": "true"}
        response = signature.requestsig(key.baseurl, key.secretKey, request)
        return response

    def createSnapshot(self,vmid):
        request = {"apiKey": key.apiKey, "response": "json", "command": "createVMSnapshot",
                   "virtualmachineid": vmid}
        response = signature.requestsig(key.baseurl, key.secretKey, request)
        return response
f=VM()
# f.deployVM("989c3cde-0557-48ee-8197-58a1d3b90d08","test0909")
f.deployVM("2b8ea85e-8695-4b8e-81f0-57b9463f7336","test-create-Template-VM")
