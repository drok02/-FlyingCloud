import signature
import urls as key

class Account():
    baseurl=key.baseurl
    apiKey=key.apiKey
    secretkey=key.secretKey
    def listAccount(self):
        baseurl=self.baseurl

        request={
            "apiKey": self.apiKey,
            "response" : "json",
            "command" : "listAccounts"
        }
        secretkey=self.secretkey
        request['apiKey']=self.apiKey

        response = signature.requestsig(baseurl,secretkey,request)

        return response

    def createAccount(self, email, firstname, lastname, password, username):
        request= {"apiKey": self.apiKey, "response": "json", "command": "createAccount", "accounttype":"0",
                  "email": email,"firstname":firstname, "lastname":lastname, "password":password, "username":username}

        response= signature.requestsig(self.baseurl,self.secretkey,request)
        print(response)

f=Account()
f.listAccount()