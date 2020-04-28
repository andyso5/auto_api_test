import re,json
class ParseHttp():

    def __init__(self,http_path,host=''):
        "添加host表示将指向本地的（带localhost）的链接转化为面向全网的链接"
        self.http_path = http_path
        self.http_file = open(http_path,encoding='UTF-8')
        self.res = {
            'method': '',
            'url': '',
            'headers': {},
            'data': '',
            'error':False,
        }

        if host and host[-1]!='/':
            self.host = host + '/'
        else:
            self.host = host
        
        self.is_empty = False

    def _modify_url(self,url):
        "如果输入host则会将本地链接修改"
        if self.host:
            return re.sub(r'localhost.*?/',self.host,url)
        else:
            return url


    def parse_request_line(self):
        request_line = self.http_file.readline().split()
        if request_line:
            self.res['method'] = request_line[0]
            self.res['url'] = self._modify_url(request_line[1])
        else:
            self.is_empty=True




    def parse_request_header(self):
        while True:
            request_header = self.http_file.readline().split()
            if request_header:
                self._parse_one_request_header(request_header)
            else:
                break

    def _parse_one_request_header(self,request_header):
        skip = False
        for i in range(len(request_header)):
            if skip:
                skip = False
                continue
            else:
                key = request_header[i]
                if key[-1]==':':
                    try:
                       self.res['headers'][key[:-1]] = request_header[i+1]
                    except IndexError:
                        print('接口请求头格式出现错误：\n%s' %self.http_path)
                        res['error']  = True
                    skip = True

    def parse_body(self):
        txt = ''
        body_lines = self.http_file.readlines()
        for i in body_lines:
            txt += i
        # self.res['data'] = json.loads(txt)
        self.res['data'] = re.sub(r'\n','',txt)

    def parse(self):
        self.parse_request_line()
        if self.is_empty:
            print('文件为空:\n%s' % self.http_path)
            self.http_file.close()
            return self.res

        else:
            self.parse_request_header()
            self.parse_body()
            self.http_file.close()
            return self.res
        
if __name__ == '__main__':
    
    from pprint import pprint
    #不带body的http文件
    p_1 = r'C:\Users\Administrator\Desktop\python\project\ytxy-api-gateway.git\test\child\getFreeCourseList.http'
    #空文件
    p_2 = r'test.http'

    p_3 = r'C:\Users\Administrator\Desktop\python\project\ytxy-api-gateway.git\test'
    # import os
    # error = []
    # for i in os.listdir(p_3):
    #     sub_p = os.path.join(p_3,i)
    #     if os.path.isdir(sub_p):
    #         for j in os.listdir(sub_p):
    #             p = os.path.join(sub_p,j)
    #             if os.path.isfile(p) and p[-4:]=='http':
    #                 try:
    #                     pprint(ParseHttp(p).parse())
    #                 except Exception as e:
    #                     print('\n\n出现异常：\n%s' % p)
    #                     print('异常为：%s\n\n' % e)
    #                     error.append((p,e))
    # pprint(error)
#     结果：
#     {'data': {},
#  'error': False,
#  'headers': {'Authorization': 'Bearer',
#              'Content-Type': 'application/json;charset=utf-8',
#              'X-YT-AppKey': '3977813fe4fe438fa1bde476854e6782'},
#  'method': 'POST',
#  'url': 'http://api.test.yitong.com/ytxy/gw/user/loginJiguang'}










