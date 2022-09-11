import base64
import hashlib
import hmac
import os
import sys
import urllib

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import urllib.parse
import urllib.request


def requestsig( baseurl, secretkey, request):
    request_str = '&'.join(['='.join([k, urllib.parse.quote_plus(request[k])]) for k in request.keys()])
    sig_str = '&'.join(
        ['='.join([k.lower(), urllib.parse.quote_plus(request[k].lower().replace('+', '%20'))]) for k in
         sorted(request)])
    sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1)
    sig = hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()
    sig = base64.encodebytes(hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest())
    sig = base64.encodebytes(
        hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip()
    sig = urllib.parse.quote_plus(base64.encodebytes(
        hmac.new(secretkey.encode('utf-8'), sig_str.encode('utf-8'), hashlib.sha1).digest()).strip())
    req = baseurl + request_str + '&signature=' + sig
    # print(req)
    res=urllib.request.urlopen(req)
    response=res.read()

    # print(response)
    return response