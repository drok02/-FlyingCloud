import json
import os
import sys

import requests
from requests.exceptions import Timeout

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import openstack.url as url
address = url.address
tenet_id = url.tenet_id

token=url.gettoken()

# 1. 오픈스택 이미지 생성
def create_image( name="test", visibility="public"):
    admin_token = token
    # 특정 (shared) 네트워크 참조
    create_image_payload = {
        "name":name,
        "visibility":visibility
    }
    image_create = requests.post("http://" + address + "/image/v2/images",
                                headers={'X-Auth-Token': admin_token},
                                 data=create_image_payload)
    print()
    print("image create response is : " + image_create)
    print()

    # 특정 img id 참조
    # img_uuid = requests.get("http://" + address + "/image/v2/images?name=ubuntu",
    #                         headers={'X-Auth-Token': admin_token}
    #                         ).json()["images"][0]["id"]
    #
    # # flavor_reference= input("flavor ref id 입력: ")
    # openstack_instance_payload = {
    #     "server": {
    #         "name": instacne_name,
    #         "imageRef": img_uuid,
    #         "flavorRef": flavor_id,
    #         "networks": [{
    #             "uuid": network_uuid
    #         }]
    #     }
    # }
    # # 인스턴스 생성 요청
    # user_res = requests.post("http://" + address + "/compute/v2.1/servers",
    #                          headers={'X-Auth-Token': admin_token},
    #                          data=json.dumps(openstack_instance_payload))
    # print(user_res.json())


# 2. 오픈스택 이미지에서 import 사용하여 web상의 이미지 데이터 import하기


create_image()