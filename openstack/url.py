import requests
import json
from requests.exceptions import Timeout

address = "1.255.161.166"
tenet_id = "3cc86c969f24442b866bfb965d2a8e4b"

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