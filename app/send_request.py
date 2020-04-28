import requests,json
# from copy import deepcopy


class SendRequest():

    def __init__(self,data):
        self.data = data
        no_use = ['protocol','error']
        for i in no_use:
            if i in self.data:
                del self.data[i]
        self.response = ''
        self.report = []

    def request(self,data={}):
        if not data:
            data = self.data

        return requests.request(**data)




        


                    
                

