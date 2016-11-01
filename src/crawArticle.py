# crawArticle.py
# coding=utf-8
# author=zhouj
import re
import urllib
import datetime
import time
from bs4 import BeautifulSoup
from agent import *
from match import *
from formatter import *

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

#获取文章title
def get_title(soup, mode):
	#需报错误信息
	if mode == 0 or mode == 1:
		title = soup.select('.arc-tit')
	elif mode == 2 or mode == 3:
		title = soup.select('.left521')
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		title = soup.find('h1')
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		title = soup.select('h1[class="title"]')
	elif mode == 14:
		title = soup.select('h1[class="article-title"]')
	elif mode == 15:
		title = soup.select('.title')
	if type(title) == list :
		for i in range(0, title.__len__()):
			title[i] = str(title[i])
		title = "".join(title)
	r = r'>([\s\S]*?)<'
	re_title = re.compile(r)
	titles = re.findall(re_title, str(title))
	return titles[0].strip()

#获取文章内容
def get_content(soup, mode):
	if mode == 0 or mode == 1:
		content = soup.select('.arc-body')
	elif mode == 2 or mode == 3:
		content = soup.select('.left523')
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		content = soup.select('.note-editing-area')
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		content = soup.select('.post-content')
	elif mode == 14:
		content = soup.select('.article-content')
	elif mode == 15:
		content = soup.select('.visible-sm')
	for i in range(0, content.__len__()):
	    content[i] = str(content[i])
	return "".join(content)

#对于vrzinc网站的时间特殊处理
def vrzinc_get_time(create_time):
	r = r'</i>([\s\S]*?)</span>'
	re_time = re.compile(r)
	create_time = re.findall(re_time, create_time)

	#对于vrzinc网站 特殊处理
	mytime = re.findall(r'\((.*?)\)', create_time[0])
	if mytime.__len__() > 0:
		return time.strftime("%Y-") + mytime[0]
	else:
		if create_time[0].find('天') != -1 :
			re_time = re.compile(r'[0-9]+')
			create_time  = re.findall(re_time, create_time[0])
			cur_time = datetime.datetime.now()
			d = int(create_time[0])
			return (cur_time - datetime.timedelta(days=d)).strftime("%Y-%m-%d")
		return time.strftime("%Y-%m-%d")

#获取文章时间
def get_time(soup, mode):
	if mode == 0 or mode == 1:
		create_time = soup.select('.time')
	elif mode == 2 or mode == 3:
		create_time = soup.select('.left522')
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		create_time = soup.select('.data-item')
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		create_time = soup.select('.postclock')
	elif mode == 14:
		create_time = soup.select('time[class="muted"]')
	elif mode == 15:
		create_time = soup.select('.data-item')
	for i in range(0, create_time.__len__()):
	    create_time[i] = str(create_time[i])
	create_time = "".join(create_time)
	#提取时间
	if mode == 0 or mode == 1:
		r = r'>(.+)<'
	elif mode == 2 or mode == 3:
		r = r'发布时间：(.+?)\s'
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		r = r'[0-9]*-[0-9]*?-[0-9]*'
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		return vrzinc_get_time(create_time)
	elif mode == 14 or mode == 15:
		r = r'[0-9]*-[0-9]*?-[0-9]*'
	re_time = re.compile(r)
	create_time = re.findall(re_time, create_time)
	
	return create_time[0]

#获取文章图片
def get_img(content, mode):
	reg = r'src="(.+?)"'
	imgre = re.compile(reg)
	imglist = re.findall(imgre,content)
	imgDir = '/Users/zhoujl/Desktop/vr/auto/images/'
	imgDir1 ='./'
	if mode == 0 or mode == 1:
		imgDir = imgDir + 'c/'
	elif mode == 2 or mode == 3:
		imgDir = imgDir + 'd/'
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		imgDir = imgDir + 'a/'
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		imgDir = imgDir + 'b/'
	elif mode == 14:
		imgDir = imgDir + 'e/'
	flag = 0
	preimage = './images/common.jpg'

	for imgurl in imglist:
		r=r'.+/(.+)'
		imgName=re.compile(r)
		imgName=re.findall(imgName,imgurl)
		imgPath=imgDir+imgName[0]
		imgPath=imgPath.replace('-moduo', '')
		try:
			#下载图片
			urllib.urlretrieve(imgurl, imgPath)
		except IOError:
			print "Error: 没有找到图片" + imgurl
		#文本中图片路径替换
		imgPath = imgPath.replace('/Users/zhoujl/Desktop/vr/auto', '.')
		content = content.replace(imgurl, imgPath)
		#添加预览图
		if flag == 0:
			preimage = imgPath
			flag = 1

	return content, preimage

def get_source(mode):
	if mode == 0 or mode == 1:
		return '百度VR'
	elif mode == 2 or mode == 3:
		return 'VR日报'
	elif mode == 4 or mode == 5 or mode == 6 or mode == 7:
		return 'moduo魔多'
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		return 'vrzinc'
	elif mode == 14:
		return 'VR科技网'

def get_label(title, content):
	flag = 0
	if title.find('Oculus') != -1 or content.find('Oculus') != -1:
		label = 'Oculus'
		flag = 1
	if title.find('HTC') != -1 or content.find('HTC') != -1:
		if flag == 1:
			label = label + '|' + 'HTC'
		else:
			label = 'HTC'
			flag = 1
	if title.find('PSVR') != -1 or content.find('PSVR') != -1 or title.find('索尼') != -1 or content.find('索尼') != -1:
		if flag == 1:
			label = label + '|' + '索尼'
		else:
			label = '索尼'
			flag = 1
	if flag == 1:
		return label
	return ''

#爬取文章,并写成sql语句
def get_article(url, mode):
	#获取文章html
	html = url_user_agent(url, mode)
	soup = BeautifulSoup(html, "html.parser")
	#获取时间、标题
	title = get_title(soup,mode).decode('utf-8')
	time = get_time(soup, mode)
	#是否提取该文章
	if title_match(title, mode) == False:
		return False,'','','','','','',''
	if time_match(time, mode) == False:
		return False,'','','','','','',''
	if (title.__len__() == 0):
		return False,'','','','','','',''
	#提取内容
	content = get_content(soup, mode)
	#输出 正确格式
	preinfo, content = arrage_art_content(content, mode)
	#获取标签
	label = get_label(title, content)
	#获取文章图片
	content, preimage = get_img(content,mode)
	source = get_source(mode)
	return True, title, time, preinfo, content, source, preimage, label