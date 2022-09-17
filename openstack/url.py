import requests
import json
from requests.exceptions import Timeout

address = "192.168.0.17"
tenet_id = "6d3c418129734350b114b3fcee7acc44"

def gettoken(user="admin", password="0000", domain="Default"):
    token_payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": user,
                        "domain": {
                            "name": domain
                        },
                        "password": password
                    }
                }
            }
        }
    }

    try:
        # Openstack keystone token 발급
        auth_res = requests.post("http://" + address + "/identity/v3/auth/tokens",
                                 headers={'content-type': 'application/json'},
                                 data=json.dumps(token_payload), timeout=5)
        admin_token = auth_res.headers["X-Subject-Token"]
        # print("token : \n",admin_token)
        return admin_token
    except Timeout:
        print("Server Connection Failed")
        return None

    except ConnectionError:
        print("HTTPConnectionErr")
        return None
    except requests.exceptions.ConnectionError:
        status_code = "Connection refused"
        print(status_code)
        return None
    # 발급받은 token 출력