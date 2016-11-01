# crawKuaixun.py
# coding=utf-8
# author=zhouj
import re
import urllib
import datetime
import time
from bs4 import BeautifulSoup
from agent import *
from match import *
from crawArticle import *

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

#获取快讯文章
def get_kuaixun(url, file_object, got_art_urls):
	#获取文章html
	html = url_user_agent(url, 15)
	soup = BeautifulSoup(html, "html.parser")
	articles = soup.select('.layout-news')
	sqlList = list()
	flag = 0
	for article in articles:
		soup1 = BeautifulSoup(str(article), "html.parser")
		#标题、前言、时间、链接
		title = get_title(soup1, 15)
		create_time = get_time(soup1, 15)
		preinfo = get_content(soup1, 15)
		re_link = re.findall(r'href="([\s\S]*?)"',preinfo)
		link = re_link[0]
		print link
		#判断链接是否之前存在
		if link+'1\n' in got_art_urls:
			continue
		if time_match(create_time,15) == False:
			continue
		#修改前言
		got_art_urls.append(link+'1\n')
		file_object.write(link+'1\n')
		re_info = re.findall(r'>([\s\S]*?)<a', preinfo)
		preinfo = re_info[0]
		#sql生成
		sql = "INSERT INTO `kuaixun`(title, create_time, preinfo, link) VALUES (\'"
		sql = sql + title + '\',\'' + create_time + ' 00:00:00' + '\',\'' \
		+ preinfo.strip() + '\',\'' + link + '\');' +'\n'
		sqlList.append(sql)
	return sqlList




