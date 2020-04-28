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

        # if data['method'] == 'POST':
        #     self.response = requests.post(url=data['url'], headers=data['headers'], data=data['data'])
        # elif data['method'] == 'GET':
        #     self.response = requests.post(url=data['url'], headers=data['headers'])
        
        # else:
        #     raise Exception('不能处理POST与GET以外的请求')
        return self.response

    def assert_response(self,substr,data={}):
        if not data:
            data = self.data
        res = self.response.text
        if isinstance(substr,str):
            if substr in res:
                return True
            else:
                self.report.append((data,res))
                return False

        else:
            for i in substr:
                if i in res:
                    return True
            else:
                self.report.append((data,res))
                return False

        


    def mass_request(self,var):
        # var形如{
        #     'data':[
        #         {
        #             'role':teacher,
        #             'id':1,
        #         },
        #         {
        #             'role':teacher,
        #             'id':2,
        #         },
        #     ]
        # }
        var_key = var.keys[0]
        #处理正文
        if var_key == 'data':
            try:
                data_type = self.data['headers']['Content-Type']
            except ValueError:
                print('找不到正文格式声明')
                raise Exception
            if 'json' in data_type:
                body = json.loads(self.data['data'])
                for cell in var[var_key]:
                    for key in cell:
                        body[key] = cell[key]
                    m_data = copy.deepcopy(self.data)
                    m_data['data'] = json.dumps(body)
                    self.request(m_data)
                    self.assert_response(self,substr,m_data)
        if var_key == 'headers':
            headers = self.data['headers']
            for cell in var[var_key]:
                for key in cell:
                   headers[key]= cell[key]
                m_data = copy.deepcopy(self.data)
                m_data['headers'] = headers
                self.request(m_data)
                self.assert_response(self,substr,m_data)

        


                    
                

