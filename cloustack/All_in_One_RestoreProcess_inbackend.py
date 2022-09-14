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



vmid="db0c3a4e-62ab-4e63-ae26-98ba4d091d7f"
vm=VM.VM()
os=guestOS.OS()
template=template.Template()
# # 1. 실행중인 VM을 중지
vm.stopVM(vmid)

# 1-2. VM 중지까지 대기
while True :
    VM_status=vm.getvmstatus(vmid)
    if VM_status== "Stopped": break
    else :
        print("wait until VM status Stopped. current status is", VM_status)
        time.sleep(1)

# # 2. VM으로부터 템플릿 생성
volumid=volume.getVol_ID_of_VM(vmid)
ostypeid=os.getostypeofVMid(vmid)
template_name="restore-template-test"
#
template_id=template.createTemplate(template_name,ostypeid,volumid)
time.sleep(10)
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

import os
import json
from re import S
import time
import paramiko
from sqlite3 import OperationalError
import requests
import webbrowser
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.files import File
from openstack.models import OpenstackBackupImage, OpenstackInstance
from openstack.serializers import OpenstackBackupImageSerializer
from openstack.openstack_modules import RequestChecker


def getTemplatestatus(admin_apiKey, admin_secretKey, template_name):
    import cloudstack_controller as csc

    request_body = {"apiKey": admin_apiKey, "response": "json", "command": "listTemplates",
                    "templatefilter": "selfexecutable", "name": template_name}
    template_status_get_req = csc.requestThroughSig(admin_secretKey, request_body)
    template_status_get_res = json.loads(template_status_get_req)
    if len(template_status_get_res["listtemplatesresponse"]) == 0:
        template_download_status = "Download Not Completed"
    else:
        template_download_status = template_status_get_res["listtemplatesresponse"]["template"][0]["status"]

    print("Template status is ", template_download_status)

    return template_download_status


def templateIDgetter(admin_apiKey, admin_secretKey, template_name):
    import cloudstack_controller as csc

    request_body = {"apiKey": admin_apiKey, "response": "json", "command": "listTemplates",
                    "templatefilter": "selfexecutable", "name": template_name}
    template_id_get_req = csc.requestThroughSig(admin_secretKey, request_body)
    template_id_get_res = json.loads(template_id_get_req)
    templateID = template_id_get_res["listtemplatesresponse"]["template"][0]["id"]
    print("Template id is ", templateID)

    return templateID


def registerCloudstackTemplate(zoneID, template_name, backup_img_file_name, os_type_id):
    import cloudstack_controller as csc
    admin_apiKey = csc.admin_apiKey
    admin_secretKey = csc.admin_secretKey

    request_body = {"apiKey": admin_apiKey, "response": "json", "command": "registerTemplate",
                    "displaytext": template_name, "format": "qcow2", "hypervisor": "kvm",
                    "name": template_name, "url": "http://119.198.160.6:8000/media/img-files/" + backup_img_file_name,
                    "ostypeid": os_type_id, "zoneid": zoneID}
    template_register_req = csc.requestThroughSigForTemplateRegist(admin_secretKey, request_body)
    webbrowser.open(template_register_req)  # url 오픈으로 해결 안돼서 webbrowser로 open함

    while True:
        template_status = getTemplatestatus(admin_apiKey, admin_secretKey, template_name)
        if template_status == "Download Complete":
            break
        else:
            if template_status == "error":
                print("이미지 등록이 정상적으로 실행되지 않았습니다.")
                break
            else:
                print("wait until image status active. Current status is ", template_status)
            time.sleep(5)

    backup_template_id = templateIDgetter(admin_apiKey, admin_secretKey, template_name)
    print("Registered template " + backup_img_file_name + " to cloudstack")

    return backup_template_id


def deployCloudstackInstance(user_id, user_apiKey, user_secretKey, instance_name, cloudstack_user_network_id,
                             backup_img_file_name, os_type):
    import cloudstack_controller as csc
    zoneID = csc.zoneID
    domainID = csc.domainID
    hostID = csc.hostID
    small_offeringID = csc.small_offeringID
    medium_offeringID = csc.medium_offeringID

    template_name = instance_name + "Template"
    if os_type == "F":  # Fedora(openstack default)
        os_type_id = "8682cef8-a3f3-47a0-886d-87b9398469b3"
    elif os_type == "c":  # centos
        os_type_id = "abc"
    else:  # ubuntu(18.04 LTS)
        os_type_id = "12bc219b-fdcb-11ec-a9c1-08002765d220"

    backup_template_id = registerCloudstackTemplate(zoneID, template_name, backup_img_file_name, os_type_id)

    request_body = {"apiKey": user_apiKey, "response": "json", "command": "deployVirtualMachine",
                    "networkids": cloudstack_user_network_id, "serviceofferingId": medium_offeringID,
                    'templateId': backup_template_id, "zoneId": zoneID,
                    "displayname": instance_name, "name": instance_name, "domainid": domainID,
                    "account": user_id, "hostid": hostID, "startvm": "false"
                    }
    try:
        instance_deploy_req = csc.requestThroughSig(user_secretKey, request_body)
    except Exception as e:
        print("에러 내용: ", e)

    print("Created Instance " + backup_img_file_name + " to cloudstack")

    return backup_template_id, instance_deploy_req


def deleteCloudstackInstanceAndTemplate():
    pass


def backup(cycle):
    import openstack_controller as oc  # import는 여기 고정 -> 컴파일 시간에 circular import 때문에 걸려서
    from account.models import AccountInfo
    openstack_hostIP = oc.hostIP

    print("this function runs every", cycle, "seconds")
    req_checker = RequestChecker()

    try:
        instance_count = OpenstackInstance.objects.filter(backup_time=cycle).count()
        if instance_count == 0:
            return "백업 주기 ", cycle, "시간짜리 instance 없음"

        admin_token = oc.admin_token()
        if admin_token == None:
            return "오픈스택서버 고장"

        backup_instance_list = OpenstackInstance.objects.filter(backup_time=cycle)
        print(cycle, "시간짜리 리스트: ", backup_instance_list)

        for instance in backup_instance_list:
            print("인스턴스 오브젝트: ", instance)
            backup_instance_id = instance.instance_id
            backup_instace_name = instance.instance_name
            backup_instance_os_type = instance.image_name[0]
            user_id = instance.user_id.user_id
            cloudstack_user_network_id = instance.user_id.cloudstack_network_id
            cloudstack_user_apiKey = instance.user_id.cloudstack_apiKey
            cloudstack_user_secretKey = instance.user_id.cloudstack_secretKey
            print("클라우드 스택의 유저 네트워크 id:: ", cloudstack_user_network_id)
            print("인스턴스 id: ", backup_instance_id)
            backup_payload = {
                "createBackup": {
                    "name": "Backup " + backup_instance_id,
                    "backup_type": "daily",
                    "rotation": 1
                }
            }
            backup_req = req_checker.reqCheckerWithData("post",
                                                        "http://" + openstack_hostIP + "/compute/v2.1/servers/" +
                                                        backup_instance_id + "/action", admin_token,
                                                        json.dumps(backup_payload))
            if backup_req == None:
                raise requests.exceptions.Timeout

            instance_image_URL = backup_req.headers["Location"]
            print("image_URL : " + instance_image_URL)
            instance_image_ID = instance_image_URL.split("/")[6]
            print("image_ID : " + instance_image_ID)

            while (True):
                image_status_req = req_checker.reqChecker("get",
                                                          "http://" + openstack_hostIP + "/image/v2/images/" + instance_image_ID,
                                                          admin_token)
                if image_status_req == None:
                    raise requests.exceptions.Timeout
                print("이미지 상태 조회 status: ", image_status_req)
                print("이미지 상태 조회 리스폰스: ", image_status_req.json())

                image_status = image_status_req.json()["status"]
                if image_status == "active":
                    break
                time.sleep(5)
            image_download_req = req_checker.reqChecker("get",
                                                        "http://" + openstack_hostIP + "/image/v2/images/" + instance_image_ID + "/file",
                                                        admin_token)
            if image_download_req == None:
                raise requests.exceptions.Timeout
            print("오픈스택에서의 이미지 다운로드에 대한 리스폰스: ", image_download_req)
            backup_img_file = open(backup_instance_id + ".qcow2", "wb")
            backup_img_file.write(image_download_req.content)
            backup_img_file.close()

            backup_img_file_name = backup_instance_id + ".qcow2"
            backup_img_file_to_db = open(backup_instance_id + ".qcow2", "rb")
            backup_image_data = {
                "instance_id": backup_instance_id,
                "image_id": instance_image_ID,
                "image_url": instance_image_URL,
                "instance_img_file": File(backup_img_file_to_db)
            }
            print(backup_image_data)

            if OpenstackBackupImage.objects.filter(instance_id=backup_instance_id).exists():
                OpenstackBackupImage.objects.filter(instance_id=backup_instance_id).delete()
                serializer = OpenstackBackupImageSerializer(data=backup_image_data)
                if serializer.is_valid():
                    serializer.save()
                    print("updated image info")
                    print(serializer.data)
                    backup_img_file_to_db.close()
                    os.remove(backup_instance_id + ".qcow2")
                    backup_template_id, instance_deploy_req = deployCloudstackInstance(user_id, cloudstack_user_apiKey,
                                                                                       cloudstack_user_secretKey,
                                                                                       backup_instace_name,
                                                                                       cloudstack_user_network_id,
                                                                                       backup_img_file_name,
                                                                                       backup_instance_os_type)
                    # deleteCloudstackInstanceAndTemplate()
                else:
                    print("not updated")
                    print(serializer.errors)
                    backup_img_file_to_db.close()
                    os.remove(backup_instance_id + ".qcow2")
                    print("not updated")
                    pass

                backup_img_file_to_db.close()
                print("updated")

            else:
                serializer = OpenstackBackupImageSerializer(data=backup_image_data)
                if serializer.is_valid():
                    serializer.save()
                    print("saved image info")
                    print(serializer.data)
                    backup_img_file_to_db.close()
                    os.remove(backup_instance_id + ".qcow2")

                    # ------cloudstack template register & instance deploy------#
                    backup_template_id, instance_deploy_req = deployCloudstackInstance(user_id, cloudstack_user_apiKey,
                                                                                       cloudstack_user_secretKey,
                                                                                       backup_instace_name,
                                                                                       cloudstack_user_network_id,
                                                                                       backup_img_file_name,
                                                                                       backup_instance_os_type)
                    # deleteCloudstackInstanceAndTemplate()
                else:
                    print("not saved")
                    print(serializer.errors)
                    backup_img_file_to_db.close()
                    os.remove(backup_instance_id + ".qcow2")
                    print("not saved")  # return "not saved"
                    pass

            print("Backup for " + backup_instance_id + " is completed")

        return "All backup has completed."

    except OperationalError:
        return "인스턴스가 없습니다."
    except requests.exceptions.Timeout:
        return "오픈스택서버 고장"
    except requests.exceptions.ConnectionError:
        return "요청이 거부되었습니다."


def backup6():
    backup_res = backup(6)
    print(backup_res)


def backup12():
    backup_res = backup(12)
    print(backup_res)


def deleter():
    OpenstackBackupImage.objects.all().delete()
    print("all-deleted")


def start():
    scheduler = BackgroundScheduler()  # ({'apscheduler.job_defaults.max_instances': 2}) # max_instance = 한 번에 실행할 수 있는 같은 job의 개수
    # scheduler.add_job(deleter, 'interval', seconds=5)
    # scheduler.add_job(backup6, 'interval', seconds=30)
    # scheduler.add_job(backup12, 'interval', seconds=120)
    # scheduler.add_job(freezerBackup6, 'interval', seconds=60)
    scheduler.add_job(backup6, 'interval', seconds=30)

    scheduler.start()
