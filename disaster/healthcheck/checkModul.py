import json
import re
from urllib import request


ip = ["google.com"]

p = re.compile('[=]\s(\d+)[m][s]')

address = "192.168.0.118"

# while True: 

# cmd = 'ping ' + ip[0]
# x=subprocess.run(cmd, shell=True, timeout=30)
# p1=p.findall(str(x))
# print(x)

# while True:
#     cmd = 'ping' + ip[0]
#     try: 
#         for x in subprocess.check_output(cmd).splitlines():
#             p1=p.findall(str(x))
#         print(ip[0], 'Ping Ok','최소 응답시간: '+p1[0],'최대 응답시간: '+p1[1],'평균 응답시간: '+p1[2])
#     except subprocess.CalledProcessError:
#         print(ip, 'Ping Check')


# ---------------try2-----------------use os system

# hostname = "google.com"
# response = os.system("ping -n 1 " + hostname)
# print("Response is ",response)
# if response == 0:
#     Netstatus = "Network Active"
# else:
#     Netstatus = "Network Error"

# print(Netstatus)


#---------------try3--------------use ping3
# while True:
#     site = "google.com"
#     result= verbose_ping(site, timeout=5)
#     # os.system("ping -n 1 "+ site)
#     # print(result)
#     if result == None:
#         print(site + '\t' + 'ping Check Fail')
#         # 재해이벤트 발생
#         break
#     else:
#         print(site + '\t'+ 'Ping Check OK')
#     time.sleep(5)


#---------------try4------------use openstack api
def token():
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

        # Openstack keystone token 발급
        auth_res = request.post("http://"+address+"/identity/v3/auth/tokens",
            headers = {'content-type' : 'application/json'},
            data = json.dumps(token_payload))

        #발급받은 token 출력
        admin_token = auth_res.headers["X-Subject-Token"]
        print("token",admin_token)
        return admin_token