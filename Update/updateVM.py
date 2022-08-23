import json
import requests
import time
from requests.exceptions import Timeout
import sys,os
sys.path.append("/Users/ibonghun/Developer/FlyingCloud/DR")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("__file__"))) + "/DR/")
from time import sleep
import backupimgSend

address = "10.125.70.26"
tenet_id = "1e65301da67c4015be06b7213129bef3"

# 토큰 받아오기
class AccountView1(): 
    
    
    
    # Get Token
    def token(self):
        # data2 = json.loads(request.body)
        # Admin으로 Token 발급 Body
        token_payload = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": "admin",
                            "domain": {
                                "name": "Default"
                            },
                            "password": "0000"
                        }
                    }
                }
            }
        }  

        try:
                # Openstack keystone token 발급
            auth_res = requests.post("http://"+address+"/identity/v3/auth/tokens",
                headers = {'content-type' : 'application/json'},
                data = json.dumps(token_payload),timeout=5)
            admin_token = auth_res.headers["X-Subject-Token"]
            print("token : \n",admin_token)
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
        #발급받은 token 출력

    #-----------------------Image---------------------------------------

    # Create image from current Instacne
    def create_image(self,serverName,imageName):
        f=backupimgSend.AccountView()
        res=f.create_img_from_server(serverName,imageName)
        print(res) 
        # admin_token= self.token()
        # auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
        #     headers = {'X-Auth-Token' : admin_token}).json()
        # server_ID=auth_res["stack"]["id"]    
        # print("Stack ID is : ",server_ID)    
        # return server_ID
    
    
    # Get image ID
    def get_image_id(self,imageName):
        admin_token= self.token()
        auth_res = requests.get("http://"+address+"/image/v2/images?name="+imageName,
            headers = {'X-Auth-Token' : admin_token}).json()["images"][0]["id"]
        image_uuid=auth_res  
        print("Image ID is : ",image_uuid)    
        return image_uuid


    #------------------------Heat---------------------------------------------------------
    #스택 ID 받아오기    
    def get_stack_uuid(self,stackName):
        admin_token= self.token()
        auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
            headers = {'X-Auth-Token' : admin_token}).json()
        stack_ID=auth_res["stack"]["id"]    
        print("Stack ID is : ",stack_ID)    
        return stack_ID

    # 스택으로 생성한 인스턴스의 이름 받아오기
    def get_instance_name(self,stackName):
        admin_token= self.token()
        stack_uuid=self.get_stack_uuid(stackName)
        auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName+"/"+stack_uuid+"/template",
            headers = {'X-Auth-Token' : admin_token}).json()["resources"]["mybox"]["properties"]["name"]
        print("Stack ",stackName,"'s Instance Name is : ",auth_res)    
        return auth_res

    # 사용자 요구사항 변경에 따른 stack(가상환경) Update
    def update_stack(self,stackName):
        stackID=self.get_stack_uuid(stackName)
        imageName="imageForUpdate"


        # 1. 스택 이름으로 기존 인스턴스 정보(이름) 받아오기
        serverName=self.get_instance_name(stackName)
        # 2. 인스턴스 이름으로 스냅샷 이미지 생성
        f=backupimgSend.AccountView()
        f.create_img_from_server(serverName,imageName)

        # Wait until image status active
        image_uuid= self.get_image_id(imageName)
        while True :
            image_status=requests.get("http://"+address+"/image/v2/images/"+image_uuid,
                headers = {'Content-Type': 'application/json','X-Auth-Token' : admin_token}).json()['status']
            if image_status=="active": break
            else : 
                if image_status=="error" :
                    print("image status is error. terminate process.")
                    return 0
                else: 
                    sleep(0.5)


        # 3. 생성된 스냅샷 이미지를 Template에 추가
        admin_token= self.token()
        flavor_num=int(input("변경을 원하는 VCPU 개수 입력(변경을 원하지 않을시 0 입력): \n"))
        ram_num=int(input("변경을 원하는 RAM(MB) 입력(변경을 원하지 않을시 0 입력): \n"))
        disk_num=int(input("변경을 원하는 Disk(GB) 입력(변경을 원하지 않을시 0 입력): \n"))
        network_num= int(input("네트워크 입력 : 1. public 2. private 3. shared\n"))
        package_num=int(input("변경을 원하는 Package들을 입력(복수입력 가능, 변경을 원하지 않을시 0 입력): 1. apache2 2. pwgen 3. libguestfs-tools 4. pastebinit 5. gedit  \n"))
        
        # flavor=[""]
        # selected_flavor={"flavor": flavor[]}
        # json_data["parameters"].update(flavor)


        if(flavor_num==1):
            with open('update.json','r') as f:
                json_data=json.load(f)
        elif(flavor_num==2):
            with open('Update/update_patch.json','r') as f:
                json_data=json.load(f)
        elif(flavor_num==3):
            with open('fedora-0223.json','r') as f2:
                json_data=json.load(f)



        # 4. Template의 내용을 바탕으로 가상환경 업데이트 수행
        user_res = requests.patch("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName+"/"+stackID,
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(json_data))
        print("stack 업데이트 ",user_res.json())


        
def main():
    f=AccountView1()
    admin_token = f.token()
    # f.create_image("VM_of_Orchestration_test","updateimage2")
    # f.get_instance_name("VE")





    # f.create_stack()
    # stackName="VE"
    # stackID=f.get_stack(stackName)
    # f.update_stack(stackName,stackID)

main()