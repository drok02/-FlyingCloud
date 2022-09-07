import time

import account
import user
import guestOS
import zone
import template

import VM

#Account 만들기 -> create acoount
account=account.Account()
userid=account.createAccount("drok02@nvaer.com","lee","bonghun","0000","bonghun")

#반환된 UserID의 key 생성하기,반환받기 -> user.registerKey
user=user.user()
apikey,secretkey=user.registerUserKey(userid)

#해당 key로 template 만들기 -> template.registerTemplate
guestos=guestOS.OS()
ubuntu=guestos.getubuntuID()
zone=zone.zone()
zoneid=zone.getZoneID()
template=template.Template()
templatename="bong"
template.regiTemplate(templatename,"https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img",ubuntu,zoneid)
time.sleep(10)
templateid=template.getTemplateIDfromAccount(templatename)

while True :
    template_status=template.getTemplatestatus(templatename)
    if template_status== "Download Complete": break
    else :
        if template_status== "error" :
            print("image status is error. terminate process.")
            exit()
        else:
            print("wait until image status active. current status is", template_status)
            time.sleep(1)


#템플릿으로 중지상태의 VM생성 -> VM.deployVM
vm=VM.VM()
vm.deployVM(templateid,templatename)








