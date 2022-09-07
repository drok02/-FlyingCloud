import json
import requests
from requests.exceptions import Timeout
import time
import cloustack.urls as cloudstackkey
import openstack.DR.backupimgSend as openstackimagesend
import openstack.url as openstackkey
import asyncio
import threading


import threading
import time

off = 0
# class baseCloudBackup(threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.flag = threading.Event()
#
#     def run(self):
#         while not self.flag.is_set():
#             print("baseCloudBackup said : Backup processing %s is alive\n"%self.ident)
#             time.sleep()
#         print("baseCloudBackup said : Thread %s die\n"%self.ident)
#
# class stopBackup(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.flag = threading.Event()
#
#     def run(self):
#         global off
#         for i in range(0,5):
#             print("stopBackup said : %d left\n"%(5-i))
#             time.sleep(1)
#         off = 1
#         print("stopBackup said : Thread %s die\n"%self.ident)
def baseCloudBackup(backupCycle=1):
    global off
    while off == 0:
        print("backupStatus is",off)
        time.sleep(backupCycle)

def stopBackup():
    global off
    off = 1
    print("stop backup and status is ",off)

def main():
    # try:
    #     basecloudbackup = baseCloudBackup()
    #     stopbackup = stopBackup()
    #
    #     basecloudbackup.start()
    #     stopbackup.start()
    #
    #     stopbackup.join()
    #     if off == 1:
    #         basecloudbackup.flag.set()
    #         basecloudbackup.join()
    # except Exception as e:
    #     print(e)
    t1=threading.Thread(target=baseCloudBackup, args=(1,))
    t2=threading.Thread(target=stopBackup )

    t1.start()
    time.sleep(3)
    t2.start()
    t2.join()
    t1.join()
if __name__ == '__main__':
    main()

#
# class disasterRecovery():
#     # cloudstackUrl= cloudstackkey.baseurl
#     # cloudstackApikey= cloudstackkey.apiKey
#     # cloudstackSecretkey=cloudstackkey.secretKey
#     # openstackUrl = openstackkey.address
#     # openstack_tenantId=openstackkey.tenet_id
#     # token=openstackkey.gettoken()
#     global backupstatus
#     backupstatus = 0
#
#     def setbacupstatus(self,int):
#         self.backupstatus=int
#     def getbackupstatus(self):
#         return self.backupstatus
#
#
#     async def baseCloudBackup(self,cycletime=1):
#         self.setbacupstatus(1)
#
#         while(self.backupstatus==1):
#             print("backup status is ",self.getbackupstatus())
#             await asyncio.sleep(cycletime)
#
#
#         print("hello")
#
#
#
#     def stopbackup(self):
#         self.setbacupstatus(0)
#         print("stop",self.backupstatus)





#
# async def main():
#     f = disasterRecovery()
#     # await asyncio.gather(f.baseCloudBackup(), f.stopbackup())
#     await f.baseCloudBackup(1)
#     # await f.ttt()
#     f.stopbackup()


