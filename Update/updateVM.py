import json
import requests
import time
from requests.exceptions import Timeout

address = "10.125.70.26"
tenet_id = "6654633a49f34e8bb31cf573e4f4d06e"

# 토큰 받아오기
class AccountView():
    def Request(self,apiURL, jsonData):
        auth_res = requests.post("http://"+address+apiURL,
            headers = {'content-type' : 'application/json'},
            data = json.dumps(jsonData))
        return auth_res

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



    #스택 ID 받아오기    
    def get_stack(self,stackName):
        admin_token= self.token()
        auth_res = requests.get("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName,
            headers = {'X-Auth-Token' : admin_token}).json()
        stack_ID=auth_res["stack"]["id"]    
        print("Stack ID is : ",stack_ID)    
        return stack_ID


    # 사용자 요구사항 변경에 따른 stack(가상환경) Update
    def update_stack(self,stackName,stackID):
        
        start = time.time()
        admin_token= self.token()
        system_num=int(input("변경을 원하는 시스템 입력: 1.Ubuntu 2.CentOS 3.Fedora\n"))


        if(system_num==1):
            with open('update.json','r') as f:
                json_data=json.load(f)
        elif(system_num==2):
            with open('centos.json','r') as f:
                json_data=json.load(f)
        elif(system_num==3):
            with open('fedora-0223.json','r') as f:
                json_data=json.load(f)
     
            #address heat-api v1 프로젝트 id stacks
        user_res = requests.put("http://"+address+"/heat-api/v1/"+tenet_id+"/stacks/"+stackName+"/"+stackID,
            headers = {'X-Auth-Token' : admin_token},
            data = json.dumps(json_data))
        print("stack 업데이트 ",user_res)

        end = time.time()
        print("종래 시스템의 오케스트레이션 가상환경 업데이트 시간 : ", end-start)
        

def main():
    f=AccountView()
    # f.create_stack()
    stackName="VE"
    stackID=f.get_stack(stackName)
    f.update_stack(stackName,stackID)

main()