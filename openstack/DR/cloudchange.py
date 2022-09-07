import json
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import openstack.url as url
address = url.address
tenet_id = url.tenet_id
import webbrowser

def viewCloudstackconsole(Ftoken,instanceid,instanceName):

    request='http://'+address+':6080/vnc_lite.html?path=%3Ftoken%'+Ftoken+'&title='+instanceName+'('+instanceid+')'
    webbrowser.open(request)

Ftoken=url.gettoken()
viewCloudstackconsole(Ftoken,'ubuntu','a911fa62-9446-4063-9851-3f9aa576f6e0')