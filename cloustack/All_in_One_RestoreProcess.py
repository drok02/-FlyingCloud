import json

import VM
import template
import guestOS
import volume
import time
# Restore 환경을 위해 먼저 VM 생성
# vm=VM.VM()
# res=vm.deployVM("989c3cde-0557-48ee-8197-58a1d3b90d08","restore-test-2","true")
# res=json.loads(res)
# vmid=res["deployvirtualmachineresponse"]["id"]
# print(res)
# print("vmid is ",vmid)



vmid="ed063e0a-1d74-4b3d-968d-7d19de66b28d"
vm=VM.VM()
os=guestOS.OS()
template=template.Template()
# 1. 실행중인 VM을 중지
vm.stopVM(vmid)

# 1-2. VM 중지까지 대기
while True :
    VM_status=vm.getvmstatus(vmid)
    if VM_status== "Stopped": break
    else :
        print("wait until VM status Stopped. current status is", VM_status)
        time.sleep(1)

# 2. VM으로부터 템플릿 생성
volumid=volume.getVol_ID_of_VM(vmid)
ostypeid=os.getostypeofVMid(vmid)
template_name="restore-template-test"

template_id=template.createTemplate(template_name,ostypeid,volumid)

while True :
    template_status=template.getTemplatestatus(template_name)
    if template_status== "Download Complete": break
    else :
        if template_status== "error" :
            print("image status is error. terminate process.")
            exit()
        else:
            print("wait until image status active. current status is", template_status)
            time.sleep(1)

# 3. 템플릿을 extractable 상태로 업데이트

template.updateextractable(template_id)


# 4. 템플릿 extrat api 실행

extract_job_id=template.extractTemplate(template_id)
while True :
    job_status=template.queryjobresult(extract_job_id)
    job_status=json.loads(job_status)
    job_status=job_status["queryasyncjobresultresponse"]["jobstatus"]
    if job_status == 1 : break
    else :
        print("wait until job status active. current status is", job_status)
        time.sleep(0.5)

# for i in range(3):
#     template.queryjobresult(extract_job_id)
#     time.sleep(0.5)
# 5. 해당 extract job을 참조하여 download url 받아오기

template.getTemplateDownURL(extract_job_id)

