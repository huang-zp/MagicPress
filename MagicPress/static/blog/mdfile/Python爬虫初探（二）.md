>** 相对于系列一做了一些简单的改进，主要是由于科四有图片和动图之分，并且有时候程序会暂停，但不报错，所以一直在想断点继续问题，当然效率依旧低。见谅**



# 同时爬取图片和动图问题
因为科目四有的题目包含动图，要爬取的网站是做成mov格式的短视频
例如：

	<div class="test-r f-r">
		                  <video src="http://www.jiazhao.com/images/tiku/201511231357033827.mov" controls="controls">您的浏览器不支持不放</video><!-- <a href="javascript:;" class="t-big">点击放大观看</a> -->   
		                  		   
## 增加获取视频链接

系列一获取图片的方法是在获取选项、答案的基础上再次传到BeautifulSoup对象，然后再次提取img标签，如果某题没有图片，提取的则是一个空值，此处提取img和video标签。如果某题没有图片或视频，提取的则是一个空值。只需改一句代码

	img = soup.find_all(['img','video'])

# 获取图片或动图后缀

系列一中为了方便直接在文件名后面加的字符串形式.png后缀，但是现在要解决后缀不一致（写代码尽可能还是不要偷懒...）
解决代码：

	if img:
		for im in img:
			src = im.get('src')
			suffix = src.split('.')[3] 
			filename = str(i) + '.' + suffix

如果此题有图片或动图，则把这个图的链接通过'.'进行分割。最后的元素则是后缀

# 争取实现断点继续

不知道为什么程序会暂停不动，模仿浏览器，捕获异常都试了，依然不行，所以我尽可能的实现断点继续。
每个图片对应一个链接，难免有一个链接卡住（我猜测的）
**  解决办法 : **
在我们得到链接，并生成文件名后，先不去打开这个这个链接，先根据文件名判断这个图片是否文件夹中已经包含，如果包含扔掉这个链接，去继续下一个链接

	if img:
		for im in img:
			src = im.get('src')
			suffix = src.split('.')[3] 
			filename = str(i) + '.' + suffix
			if os.path.exists('picture/'+filename):
				break
			saveImg(im.get('src'),filename)
			
![](/static/editor.md/photoupdate/2017-08-15--2222.png)

# 题目解析的爬取

**思路**
	1.将所以题目的解析链接爬取出去单独存放到一个文件。
	2.为了解决有些链接一次进不去必须中断程序再次开始，和存储图片思路一样，争取实现断点继续，
	3.但是写入文件和保存图片还是不一样，针对面临的情况，初步解决想法为每抽取一条链接的解析，就删掉这个链接，用列表存储从链接文件中读取的链接
	
	
	