import json
import os
import sys

import requests
from requests.exceptions import Timeout

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import openstack.url as url
address = url.address
tenet_id = url.tenet_id



def setServerError(Openstack_instanceID):
    admin_token=url.gettoken()
    openstack_setError_payload={
        "os-resetState": {
            "state": "error"
        }
    }
    print(admin_token)
    user_res = requests.post("http://" + address + "/compute/v2.1/servers/"+Openstack_instanceID+"/action",
                             headers={'X-Auth-Token': admin_token},
                             data=json.dumps(openstack_setError_payload))

    print("set instance error result is : " , user_res)

setServerError("b2ea89e0-bccf-4b01-bdd7-721cbcf341bc")