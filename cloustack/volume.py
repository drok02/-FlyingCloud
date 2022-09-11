import urls as key
import signature
import json

def listvolofvm(vmid):
    baseurl = key.baseurl
    apikey = key.apiKey
    secretkey = key.secretKey
    request = {"apiKey": apikey, "response": "json", "command": "listVolumes", "virtualmachineid": vmid}

    res=signature.requestsig(baseurl, secretkey, request)
    # print("volume list  : ",res)
    return res


def getVol_ID_of_VM(vmid):
    res=listvolofvm(vmid)
    res_json=json.loads(res)
    vmid=res_json['listvolumesresponse']['volume'][0]['id']
    print("volume is ",vmid)
    return vmid

# getVol_ID_of_VM("ed063e0a-1d74-4b3d-968d-7d19de66b28d")