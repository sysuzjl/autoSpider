# sqlModule.py
# coding=utf-8
# author=zhouj
import re
import sys

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

def safe_replace(content):
	#去掉\n和\r
	content = content.replace('\n', '')
	r = re.compile(r'\'')
	s = r.sub('\\\'',content)
	return s

def get_sql(title, time, preinfo, content, source, mode, preimage, label):
	sql = "INSERT INTO `article_pool`(title, create_time, preinfo, content, preimage, source, type, label) VALUES (\'"
	#添加 标题、时间、导语、内容、来源
	sql = sql + safe_replace(title) + '\',\'' \
	+ safe_replace(time) + ' 00:00:00' + '\',\'' \
	+ safe_replace(preinfo) + '\',\'' \
	+ safe_replace(content) + '\',\'' \
	+ safe_replace(preimage) + '\',\'' \
	+ safe_replace(source) + '\','
	#添加类型
	if mode == 0 or mode == 3 or mode == 4 or mode == 8 or mode == 14:
		sql = sql + '1' + ',\''
	elif mode == 1 or mode == 6 or mode == 12:
		sql = sql + '3' + ',\''
	elif mode == 2 or mode == 5 or mode == 9 or mode == 10 or mode == 11:
		sql = sql + '2' + ',\''
	elif mode == 7 or mode == 13:
		sql = sql + '4' + ',\''
	sql = sql + label + '\');'

	return sql
