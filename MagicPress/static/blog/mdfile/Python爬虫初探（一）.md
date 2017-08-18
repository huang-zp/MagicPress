> ** 最近参与了的一个项目，因为项目需要驾照考试科一和科四的完整题库，网上找了好久找不到完整版题库，所以才有了这篇博客的由来，因为技术不太好，之前学习的又是Python web相关的知识，所以关于程序的代码可能有些繁琐、低效。见谅**




# 分析得到标题、选项和答案
首先看一下要爬取的网页源码内容，科目一共有四章，第一章有30页，每页二十道题，这是第一章第一页的第一题

	<a href="/tiba/9294/" target="_blank">
		          <div class="ui-test clearfix titem">
		               <p class="title">1、&nbsp;如图所示，A车在此处停车是可以的。</p>
		                                         <!--判断-->
		                   <div class="test-bd f-l">
		                       <ul>
		                            <li>A、正确</li>
		                            <li>B、错误</li>
		                            <li class="answer"><strong class="right">答案：</strong> <strong>对</strong><span style="margin-left:100px;display:inline-block;">查看分析</span></li>
		                       </ul>
		                    </div>
		                                        <div class="test-r f-r">
		                  <img src="http://www.jiazhao.com/images/tiku/1436112505.png" ><!-- <a href="javascript:;" class="t-big">查看大图</a> -->                        </div>
		          </div>
		          </a>
## 获取标题
**思考**
+ 利用urllib.request.urlopen获取网页HTML内容
+ 将HTML内容传到BeautifulSoup对象
+ 从对象里提取class为'title'的p标签

	from urllib.request import urlopen
	from bs4 import BeautifulSoup
	for n in range(1,31):
		url = 'www.××××××.com' + str(n)
		html = urlopen(url)
		soup = BeautifulSoup(html,'lxml')
		titlelist = soup.findAll("p",{"class":"title"})

现在得到了第一章的所有题目标题的列表。
## 获取选项和答案
选项和答案同样思路
+ 从对象中查找class 为"test-bd f-l"的div标签

	chooselist = bs0bj.findAll("div",{"class":"test-bd f-l"})

## 使用for循环同时遍历两个列表

	for title,choose,jiexi in zip(titlelist,chooselist):
		print(title.get_text())
		print(choose.get_text()) 
	
此时将会输出第一章所有的标题、选项和答案

**  zip:因为要同时遍历两个列表，接受一系列可迭代对象作为参数，将对象中对应的元素打包成一个个tuple（元组），然后返回由这些tuples组成的list（列表）。若传入参数的长度不等，则返回list的长度和参数中长度最短的对象相同。
get_text():把正在处理的HTML文档中的所有标签都清楚，然后返回一个只包含文字的字符串**

# 将得到数据写入文件，并做简单处理
## 将标题、选项、答案写入文件
	with open('tiku1.txt','w') as file:
		***
		***
		***
		for title,choose,jiexi in zip(titlelist,chooselist):
			file.write(title.get_text())
			file.write(choose.get_text()) 
	
文件中包含第一章所有试题，不足之处是多了四个字"查看解析"
	![](/static/editor.md/photoupdate/2017-08-15--1.png)
## 使用空值替换多余字符
解决办法：
	将文件中的数据全部读取出来赋值到字符串a
	使用字符串替换，使用空值替换掉“查看解析”
	将替换好的字符串写到另一个新文件

	# -*- coding:utf-8 -*-
  	with open('tiku1.txt','r') as f1:
  		a = f1.read()
  	b = a.replace('查看分析','')
  	with open('newtiku1.txt','w') as f2:
  		f2.write(b)
  
  		
# 题目对应图片的爬取
  
## 解决图片对应题号问题
  ** 思考，并不是每道题都附带图片，但是图片的命名必须要和题号对应起来，所以，在获取选项、答案的基础上再次传到BeautifulSoup对象，然后再次提取img标签，如果某题没有图片，提取的则是一个空值

	from urllib.request import urlopen
	from savepic import saveImg
	from bs4 import BeautifulSoup
	i = 1
	for n in range(1,30):
		url = "www.××××××.com"+ str(n)
		html = urlopen(url)
		bs0bj = BeautifulSoup(html,'lxml')
		chooselist = bs0bj.findAll("div",{"class":"ui-test clearfix titem"})
		for choose in chooselist:
			soup = BeautifulSoup(str(choose),"lxml")
			img = soup.find_all(['img'])
			if img:
				for im in img:
					filename = str(i)+'.png'
					saveImg(im.get('src'),filename)
					print("保存第{0}题的图片".format(i))
			else:
				print('第{0}题没有图片'.format(i))

## 图片保存

	from urllib.request import urlopen
	def saveImg(imageURL,fileName):
		u = urlopen(imageURL)
		data = u.read()
		with open('picture/'+fileName, 'wb') as f:
			f.write(data)
			
和写入字符串到文件类似，不过这里是以二进制方式写入图片流
	![](/static/editor.md/photoupdate/2017-08-15--2.png)