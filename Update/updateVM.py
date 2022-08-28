import json
import requests
import time
from requests.exceptions import Timeout
import sys,os
sys.path.append("/Users/ibonghun/Developer/FlyingCloud/DR")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("__file__"))) + "/DR/")
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname("__file__"))) + "/Create/")
from time import sleep
import backupimgSend
# import create

address = "192.168.0.12"
tenet_id = "38aa5f9f33aa4d73bce5442f8a306e11"

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

    #-------------------------Cinder---------------------------------------------
    #스택의 볼륨이름 get
    def get_Stacks_volName(self,stackName):
        template=self.get_stack_template(stackName)
        volName=template["resources"]["myvolume"]["properties"]["name"]
        print("VolName is : ", volName)
        return volName
    # 해당 볼륨의 ID get
    def get_vol_id(self,VolName):
        admin_token=self.token()
        auth_res = requests.get("http://"+address+"/volume/v3/"+tenet_id+"/volumes?name="+VolName,
            headers = {'X-Auth-Token' : admin_token}).json()["volumes"][0]["id"]
        print("VolName ",VolName,"'s Volume set result is : ",auth_res)    
        return auth_res

    #볼륨의 status 변경
    def set_vol_avail(self,volID):
        admin_token=self.token()
        payload={
            "os-reset_status": {
                "status": "available",
                "attach_status": "detached",
                "migration_status": "migrating"
            }
        }

        auth_res = requests.post("http://"+address+"/volume/v3/"+tenet_id+"/volumes/"+volID+"/action",
            headers = {'Content-Type': 'application/json','X-Auth-Token' : admin_token},
            data=json.dumps(payload))
        print("Volume ",volID,"'s status is : ",auth_res)    
        return auth_res


    #------------------------Heat---------------------------------------------------------
    #스택의 ID 받아오기    
    def get_stack_uuid(self,stackName):
        admin_token= self.token()
        auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
            headers = {'X-Auth-Token' : admin_token}).json()
        stack_ID=auth_res["stack"]["id"]    
        print("Stack ID is : ",stack_ID)    
        return stack_ID
    
    
    def get_stack_template(self,stackName):
        admin_token=self.token()
        stack_uuid=self.get_stack_uuid(stackName)
        auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName+"/"+stack_uuid+"/template",
            headers = {'X-Auth-Token' : admin_token}).json()
        print("Stack ",stackName,"'s Template detail is : ",auth_res)    
        return auth_res




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
        admin_token= self.token()

        # # 1. 스택 이름으로 기존 인스턴스 정보(이름) 받아오기
        # serverName=self.get_instance_name(stackName)

        # 1_1 Volume의 상태 available 상태로 변경시키기 
        VolName=self.get_Stacks_volName(stackName)
        Volid=self.get_vol_id(VolName)
        self.set_vol_avail(Volid)



        # # 2. 인스턴스 이름으로 스냅샷 이미지 생성
        # f=backupimgSend.AccountView()
        # f.create_img_from_server(serverName,imageName)
        
        # # Wait until image status active
        # image_uuid= self.get_image_id(imageName)

        # while True :
        #     image_status=requests.get("http://"+address+"/image/v2/images/"+image_uuid,
        #         headers = {'Content-Type': 'application/json','X-Auth-Token' : admin_token}).json()['status']
        #     if image_status=="active": break
        #     else : 
        #         if image_status=="error" :
        #             print("image status is error. terminate process.")
        #             return 0
        #         else: 
        #             print("wait until image status active. current status is",image_status)
        #             sleep(0.5)


        # 3. 생성된 스냅샷 이미지를 Template에 추가
        flavor_num=int(input("업데이트 파일 선택 : 1. update.json 2. update_patch.json  \n"))
        # flavor_num=int(input("변경을 원하는 VCPU 개수 입력(변경을 원하지 않을시 0 입력): \n"))
        # ram_num=int(input("변경을 원하는 RAM(MB) 입력(변경을 원하지 않을시 0 입력): \n"))
        # disk_num=int(input("변경을 원하는 Disk(GB) 입력(변경을 원하지 않을시 0 입력): \n"))
        # network_num= int(input("네트워크 입력 : 1. public 2. private 3. shared\n"))
        # package_num=int(input("변경을 원하는 Package들을 입력(복수입력 가능, 변경을 원하지 않을시 0 입력): 1. apache2 2. pwgen 3. libguestfs-tools 4. pastebinit 5. gedit  \n"))
        
        # flavor=[""]
        # selected_flavor={"flavor": flavor[]}
        # json_data["parameters"].update(flavor)
        

        if(flavor_num==1):
            with open('update.json','r') as f:
                json_data=json.load(f)
        elif(flavor_num==2):
            with open('update_patch.json','r') as f:
                json_data=json.load(f)
        elif(flavor_num==3):
            with open('fedora-0223.json','r') as f:
                json_data=json.load(f)

        # json_data["parameters"]["images"]=imageName


        # 4. Template의 내용을 바탕으로 가상환경 업데이트 수행
        user_res = requests.patch("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName+"/"+stackID,
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(json_data))
        print("stack 업데이트 ",user_res)

        
        # while True :
        #     stack_status= requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
        #     headers = {'X-Auth-Token' : admin_token}).json()["stack"]["stack_status"]
        #     # print(stack_status)
        #     if stack_status=="UPDATE_COMPLETE": 
        #         print("UPDATE_COMPLETE")
        #         break
        #     else : 
        #         if stack_status=="error" :
        #             print("image status is error. terminate process.")
        #             return 0
        #         else: 
        #             print("wait until stack status complete. current status is",stack_status)
        #             sleep(1)


        # f2=backupimgSend.AccountView()
        # f2.delete_image(imageName)



    def test(self,serverName,imageName):
        f=backupimgSend.AccountView()
        f.create_img_from_server(serverName,imageName)

    def test2(self,imageName):
        f=backupimgSend.AccountView()
        f.delete_image(imageName)
    def test3(self):
        stackName="VE"
        f=AccountView1()
        admin_token=f.token()
        stack_status= requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
            headers = {'X-Auth-Token' : admin_token}).json()["stack"]["stack_status"]
        print(json.dumps(stack_status,indent="\t"))
    
    def test4(self):
        f=create.AccountView()
        f.create_stack()

def main():
    f=AccountView1()
    admin_token = f.token()
    # f.create_image("VM_of_Orchestration_test","updateimage2")
    # f.get_instance_name("VE")
    # f.set_vol_avail("c1a09d0a-a565-4378-a7a7-b8c15921e002")
    stackName="VE"
    f.update_stack(stackName)
    # f.test("VM_of_Orchestration_test","Update")
    # f.test2("Update")

# f=AccountView1()
# f.test3()
main()


