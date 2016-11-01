# crawPage.py
# coding=utf-8
# author=zhouj
import re
import datetime
import sys
from bs4 import BeautifulSoup
from agent import *

#默认utf-8 编码
reload(sys)
sys.setdefaultencoding('utf-8')

#获取主页每篇文章模块
def get_main_content(url, mode):
	html = url_user_agent(url, mode)
	soup = BeautifulSoup(html, "html.parser")

	#需要_message 报错误信息
	#适应不同主页对其文章模块的摘取
	if mode == 0 or mode == 1:
		content = soup.select('.pic-item-6')
	elif mode == 2 or mode == 3:
		content = soup.select('.xwt1')
	elif mode == 4 or mode == 5:
		content = soup.select('.layout-row')
	elif mode == 8 or mode == 9 or mode == 10 or mode == 11 or mode == 12 or mode == 13:
		content = soup.find_all('h2')
	elif mode == 14:
		content = soup.select('.excerpt')
	elif mode == 6 or mode == 7:
		r = re.compile(r'<li[\s\S]*?/li>')
		html = html.replace('\\', '')
		content = re.findall(r, html)
	return content

#爬取主页上的链接，判断是否重复爬取，是则放入列表
def craw_page(mainUrl, gotUrls, mode):
	artModule = get_main_content(mainUrl, mode)
	seen = set()
	#获取文章链接
	for art in artModule:
		art = str(art)
		r=r'href="([\s\S]*?)"'
		re_html = re.compile(r)
		htmlList = re.findall(re_html, str(art))
		if (mode == 2 or mode == 3):
			htmlList[0] = 'http://www.vrrb.cn'+htmlList[0]
		if mode == 6 or mode == 7:
			re_html = re.compile(r'id=([0-9]*)')
			htmlList = re.findall(re_html, htmlList[0])
			htmlList[0] = 'http://www.moduovr.com/article/'+htmlList[0]+'.html'
		if htmlList[0]+'\n' not in gotUrls:
			seen.add(htmlList[0])

	return list(seen)
