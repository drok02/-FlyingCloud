import subprocess
import re

ip = ["192.168.0.1"]

p = re.compile('[=]\s(\d+)[m][s]')


cmd = 'ping ' + ip[0]
subprocess.run(cmd, shell=True)

# while True:
#     cmd = 'ping' + ip[0]
#     try: 
#         for x in subprocess.check_output(cmd).splitlines():
#             p1=p.findall(str(x))
#         print(ip[0], 'Ping Ok','최소 응답시간: '+p1[0],'최대 응답시간: '+p1[1],'평균 응답시간: '+p1[2])
#     except subprocess.CalledProcessError:
#         print(ip, 'Ping Check')