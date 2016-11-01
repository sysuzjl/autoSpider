# formatter.py
# coding=utf-8
# author=zhouj
import re
import urllib
import datetime
import sys
from bs4 import BeautifulSoup

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

def isToDel(inData):
    if inData == '<p></p>' or inData == '<p> </p>' or inData == '<p>\n</p>' \
    or inData.find('src="http://img.moduovr.com/01.png"') != -1 \
    or inData.find('src="http://img.moduovr.com/160518_sarah_2_1.jpg"') != -1 \
    or inData.find('src="http://img.moduovr.com/151102_sarah_2_3.jpg"') != -1 \
    or inData.find('src="http://img.moduovr.com/01.png"') != -1 \
    or inData.find('魔多，最专业的 VR 媒体，有料更有趣') != -1 \
    or (inData.find('魔多') != -1 and inData.find('有料更有趣') != -1) \
    or inData.find('转载请注明作者') != -1 \
    or (inData.find('关于VR，所有') != -1 and inData.find('都在这里') != -1) \
    or inData.find('转载请注明') != -1 \
    or inData.find('http://www.vrrb.cn/"') != -1 \
    or inData.find('虚拟现实第一媒体') != -1 \
    or inData.find('百度VR') != -1 \
    or (inData.find('更多精彩VR') != -1 and inData.find('请戳进来') != -1) \
    or inData.find('via') != -1:
        return True
    return False

def arrage_art_content(article, mode):


#提取<div>....</div>
	if mode == 14:
		re_art = re.findall(r'<p[\s\S]+/p>', article)
	else:
		re_art = re.findall(r'<div[\s\S]*?>([\s\S]*)</div>', article)

#去掉\n和\r
	r = re.compile(r'[\f\n\r\t\v]')
	s = r.sub('',str(re_art[0]))

#将p中的属性替换
	reobj = re.compile(r'<p[\s\S]*?>')  
	s, number = reobj.subn('<p>', s)

#去掉div中属性
	reobj = re.compile(r'<div[\s\S]*?>')  
	s, number = reobj.subn('<div>', s)
	

#去掉span标签
	s = re.sub(r'<span[\s\S]*?>', '', s)
	s = re.sub(r'</span>', '', s)
	s = re.sub(r'<br/>', '', s)
	s = re.sub(r'<br>', '', s)
	s = re.sub(r'<script[\s\S]*?</script>', '', s)
	s = re.sub(r'<xml[\s\S]*?</xml>', '', s)
	s = re.sub(r'<!--[\s\S]*?-->', '', s)
	s = re.sub(r'<!--[\s\S]*?>', '', s)
	s = re.sub(r'<![\s\S]*?-->', '', s)
	s = re.sub(r'<![\s\S]*?>', '', s)

#去掉class, id
	s = re.sub(r'class="[\s\S]*?"', '', s)
	s = re.sub(r'id="[\s\S]*?"', '', s)


#去掉img，iframe，embed，a中属性
	reList = [r'<embed([\s\S]*?src="[\s\S]*?"[\s\S]*?)>',
	r'<iframe([\s\S]*?src="[\s\S]*?"[\s\S]*?)>',
	r'<a([\s\S]*?href="[\s\S]*?"[\s\S]*?)>',
	r'<img([\s\S]*?src="[\s\S]*?"[\s\S]*?)>']
	for i in range(0, reList.__len__()):
		deleteInfos = re.findall(reList[i], s)
		for deleteInfo in deleteInfos:
			if i == 2:
				temp = re.compile(r'href="[\s\S]*?"')
			else:
				temp = re.compile(r'src="[\s\S]*?"')
			if deleteInfo[-1:] == '/':
				endinfo = '/'
			else:
				endinfo = ''
			temp = re.findall(temp, deleteInfo)
			s = s.replace(deleteInfo, ' ' + temp[0] + endinfo)


 #将img上的center替换,及div替换
	reobj = re.compile('<center[\s\S]*?>')  
	s, number = reobj.subn('<p>', s)
	reobj = re.compile('</center>')  
	s, number = reobj.subn('</p>', s)
	reobj = re.compile('<div[\s\S]*?>')  
	s, number = reobj.subn('<p>', s)
	reobj = re.compile('</div>')  
	s, number = reobj.subn('</p>', s)


#去掉来源
	lines = re.findall(r'(<p[\s\S]*?</p>)', s)
	for i in range(0, lines.__len__()):
		if isToDel(lines[i]) == True:
			s = s.replace(lines[i], '')
#每个</p>后添加/n
	reobj = re.compile(r'</p>\s*')
	s = reobj.sub('</p>', s)


#添加导语
	r = re.compile(r'<p>([\s\S]*?)</p>')
	info = re.findall(r, s)
	addInfo = ''
	#找到首个p标签不含img
	for i in range(0, info.__len__()):
		if info[i].find('<img') != -1:
			continue
		else:
			addInfo = info[i]
			break

	pre_info = re.sub(r'<[\s\S]*?>', '', addInfo)
	if pre_info.find('摘要：') != -1 :
		s = s.replace(pre_info, '')
		s = s.replace('<p></p>','')
		pre_info = pre_info.replace('摘要：', '')

	return pre_info, s