import json
import re
from requests.exceptions import Timeout
import requests
from backupimgSend import AccountView



ip = ["google.com"]

p = re.compile('[=]\s(\d+)[m][s]')

address = "10.125.70.26"

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
def check_module(serverID):
    f=AccountView()
    admin_token=f.token()
    if admin_token == None:
        print("Server Error")
    try: 
    #인스턴스 생성 요청
        user_res = requests.get("http://"+address+"/compute/v2.1/servers/"+serverID,
            headers = {'X-Auth-Token' : admin_token}, timeout=5)
        vm_status= user_res.json()["server"]["status"]
        print(vm_status)
        if vm_status == "ERROR":
            print("VM Error")
            return None
        else:
            return vm_status
    except Timeout:
            print("Server Connection Failed")
            return None

    except ConnectionError:
        print("HTTPConnectionErr")
        return None
    except requests.exceptions.ConnectionError:
        status_code = "Server Error"
        print(status_code)

def main():
    serverID="642574eb-f9bf-4b65-84aa-48fd404c8d4b"
    check_module(serverID)

main()