# agent.py
# coding=utf-8
# author=zhoujl
import urllib2
import sys
import requests
import re
import socket
from urllib2 import URLError, HTTPError  
#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

def url_user_agent(url, mode):
    if mode != 6 or mode != 7:
        #设置使用代理
        enable_proxy = False
        proxy = {'http':'127.0.0.1:9743'}
        proxy_handler = urllib2.ProxyHandler(proxy)
        null_proxy_handler = urllib2.ProxyHandler({})
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handler)
        else:
            opener = urllib2.build_opener(null_proxy_handler)
        # opener = urllib2.build_opener(proxy_support,urllib2.HTTPHandler(debuglevel=1))
        #opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        #添加头信息，模仿浏览器抓取网页，对付返回403禁止访问的问题
        # i_headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        i_headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'}
        req = urllib2.Request(url,headers=i_headers)
        try: 
            html = urllib2.urlopen(req)
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'  
            print 'Error code: ', e.code
            return ''
        except URLError, e:  
            print 'We failed to reach a server.'  
            print 'Reason: ', e.reason
            return ''
        except socket.error, e:
            print 'Reason: ', e
            return ''
        if url == html.geturl():
            doc = html.read()
            return doc
        return ''
    else:
        doc = requests.get(url).content
        return doc


#url = 'http://www.dianping.com/search/category/2/10/g311'
#doc = url_user_agent(url)
#print doc