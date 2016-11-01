# spider.py
# coding=utf-8
# author=zhoujl
#！/usr/bin/python 
import re
import time
import datetime
import os
import sys
from agent import *
from crawPage import * 
from crawArticle import * 
from sqlModule import *

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

#获取今天爬取的文章链接
def get_art_urls():
	cur_time = datetime.datetime.now()
	file_name = cur_time.strftime("%Y%m%d")
	file_path = '/Users/zhoujl/Desktop/vr/auto/'+file_name+'.txt'
	yesterday = cur_time - datetime.timedelta(days=2)
	global file_object
	#判断今天的urltxt是否创建，并删除昨天的txt
	if os.path.exists(file_path):
		#file_name = yesterday.strftime("%Y%m%d")
		file_path = '/Users/zhoujl/Desktop/vr/auto/'+file_name+'.txt'
		file_object = open(file_path, 'r+')
		urls=file_object.readlines()
		file_object.close()
		return urls
	else:
		file_object = open(file_path, 'a+')
		file_name = yesterday.strftime("%Y%m%d")
		file_path = '/Users/zhoujl/Desktop/vr/auto/'+file_name+'.txt'
		file_object.close()
		#if os.path.exists(file_path):
			#os.remove(file_path)
		return list()

def get_mainurls(url, mode) :
	total_pages=list()
	total_pages.append(url)
	if mode == 0:
		for i in range(2, 8):
			curpage = url + '/%d.html' %i
			total_pages.append(curpage)
	elif mode == 1:
		for i in range(2, 4):
			curpage = url + '/%d.html' %i
			total_pages.append(curpage)
	elif mode == 2:
		for i in range(2, 4):
			curpage = url + '/index_%d.html' %i
			total_pages.append(curpage)
	elif mode == 3:
		for i in range(2, 13):
			curpage = url + '/index_%d.html' %i
			total_pages.append(curpage)
	elif mode == 14:
		curpage = 'http://www.vrsat.com/category/news/page/2'
		total_pages.append(curpage)

	return total_pages

def main():
	urls=['http://ivr.baidu.com/it','http://ivr.baidu.com/gamenews',
	'http://www.vrrb.cn/guandian','http://www.vrrb.cn/kuaixun',
	'http://www.moduovr.com/category/40.html', 'http://www.moduovr.com/category/42.html',
	'http://www.moduovr.com/front/article/article_list?kws=&type=new&page=1&limit=10&cate_id=all&tag_id=151&order_by=new',
	'http://www.moduovr.com/front/article/article_list?kws=&type=new&page=1&limit=10&cate_id=all&tag_id=150&order_by=new',
	'http://www.vrzinc.com/news', 'http://www.vrzinc.com/opinion', 'http://www.vrzinc.com/report', 'http://www.vrzinc.com/startup',
	'http://www.vrzinc.com/game', 'http://www.vrzinc.com/movie', 'http://www.vrsat.com/category/news']
	#获取今天爬取的文章链接
	got_art_urls = get_art_urls()
	file_object1=open('/Users/zhoujl/Desktop/vr/auto/insert.sql','a+')
	sqlList = list()
	for i in range(0, urls.__len__()):
		#获取该网站主页的拓展页面，以获取更多文章url
		mainUrls = get_mainurls(urls[i], i)
		print mainUrls
		#爬取主页上的链接，判断是否重复爬取，是则放入列表
		for mainUrl in mainUrls: 
			urlList = craw_page(mainUrl, got_art_urls, i)
			for url in urlList:
				flag, title, time, preinfo, content, source, preimage, label = get_article(url, i)
				if flag == False:
					continue
				#返回sql语句
				sql = get_sql(title, time, preinfo, content, source, i, preimage, label) + '\n'
				sqlList.append(sql)
				file_path = time.replace('-', '') +'.txt'
				file_object = open(file_path, 'a+')
				file_object.write(url + '\n')
				file_object.close()
	file_object1.writelines(sqlList)



if __name__ == '__main__':
	global file_object
	main()
