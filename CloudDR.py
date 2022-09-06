import json
import requests
from requests.exceptions import Timeout

import cloustack.urls as cloudstackkey
import openstack.DR.backupimgSend as openstackimagesend
import openstack.url as openstackkey

class disasterRecovery():
    cloudstackUrl= cloudstackkey.baseurl
    cloudstackApikey= cloudstackkey.apiKey
    cloudstackSecretkey=cloudstackkey.secretKey
    openstackUrl = openstackkey.address
    openstack_tenantId=openstackkey.tenet_id




