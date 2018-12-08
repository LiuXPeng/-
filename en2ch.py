#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'english text translate to chinese'

__author__ = 'lxp'


import time
import sys
import http.client
import hashlib
import json
import urllib
import random




#============================================================
#--------------------调用百度翻译api翻译----------------------
#这里用的别人代码
'''''
    @Author: LCY
    @Contact: lchuanyong@126.com
    @blog: http://http://blog.csdn.net/lcyong_
    @Date: 2018-01-15
    @Time: 19:19
    说明： appid和secretKey为百度翻译文档中自带的，需要切换为自己的
           python2和python3部分库名称更改对应如下：
           httplib      ---->    http.client
           md5          ---->    hashlib.md5
           urllib.quote ---->    urllib.parse.quote
    官方链接：
           http://api.fanyi.baidu.com/api/trans/product/index

'''
def baidu_translate(content):
    appid = '20151113000005349'
    secretKey = 'osubCEzlGjzvw8qdQc41'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    q = content
    fromLang = 'en'  # 源语言
    toLang = 'zh'  # 翻译后的语言
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
        js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
        dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
        #print(dst) # 打印结果 
        if httpClient:
            httpClient.close()
        return dst
    except Exception as e:
        if httpClient:
            httpClient.close()
            return e



#===================打开文件，按行依次翻译=====================
#--------------------每行翻译字符数有限制----------------------
def trans(shuruwenjian):
	#输出文件构建
	shuchuwenjian = shuruwenjian.split('.')[0] + '_chinese' + '.txt'
	f = open(shuruwenjian, 'r', encoding='utf-8')
	line = f.readline()
	g = open(shuchuwenjian, 'w+')
	g.truncate()#清空文件，防止测试时候不停加入
	g.close()
	g = open(shuchuwenjian, 'a', encoding='utf-8')

	while line:
		t = baidu_translate(line)
		print(str(t))
		g.write(str(t))
		g.write('\n')
		line = f.readline()
		#由于api限制，每秒只能翻译一条
		time.sleep(1)

	g.close()
	f.close()

	return


def main():
	if len(sys.argv) != 2:
		print("输入错误")
		return
	filename = sys.argv[1]
	trans(filename)

	return

if __name__ == '__main__':
	main()

