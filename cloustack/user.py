import signature
import urls as key

class user():
    baseurl=key.baseurl
    apiKey=key.apiKey
    secretkey=key.secretKey


    def listusers(self):
        baseurl=self.baseurl
        request={
            "apiKey": "W52i_LjFrXiTApR6FseHUkkGH24fIHnKvZ7Oq8rZQVZ8ow1TIl4JTmYIkbjmF-9_7t7zplyR-YkcWIHQIOYU9Q",
            "response" : "json",
            "command" : "listUsers"
        }
        secretkey=self.secretkey
        request['apiKey']=self.apiKey

        response = signature.requestsig(baseurl,secretkey,request)

        return response

    def deleteuser(self):

        request= {"apiKey": self.apiKey, "response": "json", "command": "deleteUser",
                  "id": "5de8e0ef-7f5c-46fa-8c26-26a6c9cc99d8"}
        # request_str='&'.join(['='.join([k,urllib.parse.quote_plus(request[k])]) for k in request.keys()])
        # sig_str='&'.join(['='.join([k.lower(),urllib.parse.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request)])
        # sig=hmac.new(self.secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1)
        # sig=hmac.new(self.secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()
        # sig=base64.encodebytes(hmac.new(self.secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest())
        # sig=base64.encodebytes(hmac.new(self.secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()).strip()
        # sig=urllib.parse.quote_plus(base64.encodebytes(hmac.new(self.secretkey.encode('utf-8'),sig_str.encode('utf-8'),hashlib.sha1).digest()).strip())
        # req=self.baseurl+request_str+'&signature='+sig
        # req
        # res=urllib.request.urlopen(req)
        # response=res.read()
        response= signature.requestsig(self.baseurl,self.secretkey,request)
        print(response)


    def getuserkey(self,userid):
        baseurl=self.baseurl
        request={
            "apiKey": self.apiKey,
            "response" : "json",
            "command" : "registerUserKeys",
            "id": userid
        }
        secretkey=self.secretkey
        response = signature.requestsig(baseurl,secretkey,request)
        userapikey=response["registeruserkeysresponse"]["userkeys"]["apikey"]
        usersecretkey=
        return response

f=user()
f.getuserkey('59e7ea0e-e109-44d0-aaef-1ef725664e68')