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
    print(token)
    create_image_payload = {
        "name":name,
        "visibility":visibility,
        "disk_format":"qcow2",
        "container_format":"bare"

    }
    image_create = requests.post("http://" + address + "/image/v2/images",
                                headers={'X-Auth-Token': admin_token},
                                 data=json.dumps(create_image_payload))
    print()
    print("image create response is : " , image_create)
    print()


# 2. 오픈스택 이미지에서 import 사용하여 web상의 이미지 데이터 import하기
def import_image_file(imageid, url="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/0eb018a8-5e3b-41e4-8b4d-eca04b768b52/03f5b7e7-01c2-402d-b835-97737ca21b4d.qcow2?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20220912%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20220912T175534Z&X-Amz-Expires=86400&X-Amz-Signature=23af3eca50d91243fc1e691b00db162b24a6db324a37e6d1e91f32187fded639&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%20%3D%2203f5b7e7-01c2-402d-b835-97737ca21b4d.qcow2%22&x-id=GetObject"):
    admin_token = token
    # 특정 (shared) 네트워크 참조
    print(token)
    import_image_payload = {
        "method": {
            "name": "web-download",
            "uri": url
        },
        "all_stores": True,
        "all_stores_must_succeed": True
    }

        #
    import_image_data = requests.post("http://" + address + "/image/v2/images/"+imageid+"/import",
                                headers={'X-Auth-Token': admin_token},
                                 data=json.dumps(import_image_payload))
    print()
    print("image create response is : " , import_image_data)
    print()

# import_image_file("5cda54b6-d6c1-4b99-925c-b8ef2073572d","https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img")
# create_image()
import_image_file("e6184ba2-7c38-4761-a345-c9bb8411ca6d","https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img")