# match.py
# coding=utf-8
# author=zhoujl
import re
import sys
import datetime
#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

def title_match(title, mode):
	if mode == 2:
		#去除 标题标有VR每周红黑榜及VR日报字段的
		reList=[u'《VR每周红黑榜》', u'VR日报[：:]']
		for r in reList:
			re_title=re.compile(r)
			titleList = re.findall(re_title, title)
			if (titleList.__len__() > 0):
				return False

		#标题带有？做为观察一类
		re_title=re.compile(u'[\s\S]+[\?？]')
		titleList = re.findall(re_title, title)

		if (titleList.__len__() > 0):
			return True
		return False
	else:
		return True
def time_match(time, mode):
	cur_time = datetime.datetime.now()
	yesterday = cur_time - datetime.timedelta(days=2)
	cur_time = cur_time.strftime("%Y-%m-%d")
	yesterday = yesterday.strftime("%Y-%m-%d")
	if cur_time == time:
		return True
	return False
	