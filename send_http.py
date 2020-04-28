from app import HttpParse, EasyExcel, ParseCSV, SendRequest
import json
import os
import unittest
#默认断言依据
def _assert(response):
    json_data = response.json()
    if json_data['code'] == 1:
        return True
    else:
        return False

class HttpTest():
    def __init__(self,httpTemplate,data,assert_fn):
        self.httpTemplate = httpTemplate
        self.data = data
        self.assert_fn = assert_fn
        self.request = HttpParse(http_str=httpTemplate).parse(data)


    def run(self):
        self.response = SendRequest(self.request).request()
        self.is_pass = self.assertTrue()
        
    
    def assertTrue(self):
        
        return self.assert_fn(self.response)



def _check_http_file(http_path):
    file = os.path.split(http_path)[-1]
    if '.' in file:
        if file[-5:]=='.http':
            return http_path
        else:
            raise Exception("输入的文件%s不是http文件" % http_path)
    else:
        return http_path + '.http'

def _check_attached_file(http_path,data_path):
    if data_path:
        return data_path
    file = http_path[:-4] + 'csv'
    if os.path.exists(file):
        return file
    else:
        return ''

def _parse_attached_file(data_path):

    if not data_path:
        return {
            'data':[]
        }

    split_file = data_path.split('.')
    if len(split_file)<2:
        raise Exception("无法识别附加文件%s" % data_path)

    file_class = split_file[-1]
    if file_class == 'csv':
        return ParseCSV(data_path).parse()

    elif file_class == 'xlsx':
        return EasyExcel(data_path).parse()

    elif file_class == 'json':
        with open(data_path) as file:
            data = json.loads(file.read())
        return data
    else:
        raise Exception('不支持%s文件格式' % file_class)

def parse_http_test(http_path,data_path='',encoding='utf-8',assert_fn=_assert):

    http_path = _check_http_file(http_path)
    data_path = _check_attached_file(http_path,data_path)

    httpTemplate = open(http_path,encoding=encoding).read()
    data = _parse_attached_file(data_path)

    if data['data']:
        for i in data['data']:
            yield HttpTest(httpTemplate,i,assert_fn)
    else:
        yield HttpTest(httpTemplate,{},assert_fn)





if __name__ == '__main__':
    import os
    from pprint import pprint
    #同目录下存在同名的csv文件
    dir_path = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(dir_path,r'app\test.http')
    # p = r'E:\auto_generate_Jmx\http\app\test.http'
    for httptest in parse_http_test(p):
        httptest.run()
        if httptest.is_pass:
            print('变量参数为：')
            pprint(httptest.request)
            print('返回结果为：')
            pprint(httptest.response.json())




    
