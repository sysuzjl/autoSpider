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
from crawKuaixun import * 
from sqlModule import *
from mysql_connect import *

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
		file_object = open(file_path, 'a+')
		return urls
	else:
		file_object = open(file_path, 'a+')
		file_name = yesterday.strftime("%Y%m%d")
		file_path = '/Users/zhoujl/Desktop/vr/auto/'+file_name+'.txt'
		#if os.path.exists(file_path):
			#os.remove(file_path)
		return list()


def main():
	urls=['http://ivr.baidu.com/it/','http://ivr.baidu.com/gamenews/',
	'http://www.vrrb.cn/guandian/','http://www.vrrb.cn/kuaixun/',
	'http://www.moduovr.com/category/40.html', 'http://www.moduovr.com/category/42.html',
	'http://www.moduovr.com/front/article/article_list?kws=&type=new&page=1&limit=10&cate_id=all&tag_id=151&order_by=new',
	'http://www.moduovr.com/front/article/article_list?kws=&type=new&page=1&limit=10&cate_id=all&tag_id=150&order_by=new',
	'http://www.vrzinc.com/news', 'http://www.vrzinc.com/opinion', 'http://www.vrzinc.com/report', 'http://www.vrzinc.com/startup',
	'http://www.vrzinc.com/game', 'http://www.vrzinc.com/movie', 'http://www.vrsat.com/category/news', 'http://www.moduovr.com/front/news']
	#获取今天爬取的文章链接
	got_art_urls = get_art_urls()
	file_object1=open('/Users/zhoujl/Desktop/vr/auto/insert.sql','a+')
	sqlList = list()
	for i in range(0, urls.__len__()):
		print i
		if i == 15:
			sqlList = sqlList + get_kuaixun(urls[i], file_object, got_art_urls)
		else:
			print urls[i]
			#爬取主页上的链接，判断是否重复爬取，是则放入列表
			urlList = craw_page(urls[i], got_art_urls, i)
			for url in urlList:
				flag, title, time, preinfo, content, source, preimage, label = get_article(url, i)
				if flag == False:
					continue
			#返回sql语句
				sql = get_sql(title, time, preinfo, content, source, i, preimage, label) + '\n'
				sqlList.append(sql)
				file_object.write(url + '\n')
	file_object1.writelines(sqlList)
	#mysql_connect(sqlList)


if __name__ == '__main__':
	global file_object
	main()
