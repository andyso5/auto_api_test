1.解析xlsx文件需要安装pywin32，注意文件比较大，采用国内镜像可以大大加快速度，如下输入：
pip intall -i https://pypi.tuna.tsinghua.edu.cn/simple pywin32

  详情参见：https://blog.csdn.net/fatfatmomo/article/details/81184119

2.把..\AppData\Local\Programs\Python\Python37\lib\site-packages\win32
  这个路径加到系统变量，详情：https://blog.csdn.net/Andy_221313/article/details/105701918
  
 3.文件路径用绝对路径
 
 4.使用案例见https://github.com/andyso5/auto_api_test/blob/master/send_http.py
 
 5.http文件中变量定义的形式为${variable}
 
 6.send_http.py中parse_http_test函数返回的是一个迭代HttpTest对象，
   如果存在可以正常解析的参数文件，每次迭代返回的对象包含的参数顺序与参数文件的行数一致
   
   如果保持parse_http_test中的变量data_path为默认值（空字符），脚本会默认寻找http文件同级目录下参数文件（只支持csv文件）
   
   如果向parse_http_test中的变量data_path传入非空的参数文件路径，会优先以这个参数文件为准(支持csv,xlsx,json三种格式)
   
  7.可以自定义断言函数，通过parse_http_test中的assert_fn传入
    断言函数的要求是：
    1.只能接受requests.models.Response对象这一个参数
    2.返回bool值
