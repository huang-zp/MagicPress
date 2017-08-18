
> **在实验楼偶然发现一篇使用python实现图片转字符画的文章，觉得很有创意，图片的处理使用PIL。于是尝试了一下，本篇博客主要是参考原文，百度谷歌后解决在实践中遇到的问题，和一些已经解答的疑惑。在此记录所得**


# 分析
一张彩色的照片有很多颜色，每种颜色都有对应的RGB值。我们可以这样处理一张图片，将照片深色的部分使用繁琐的字符填充，而浅色的部分使用简单的字符填充，例如" $ " 和 " . "两种字符填充可以组成强烈的对比。判断深色部分或者浅色部分使用灰度值
> 灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，黑色为0，故黑白图片也称灰度图像

使用灰度值公式将像素的 RGB 值映射到灰度值:

	gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
这样就可以判断出照片中深色浅色的部位了，因为我们能使用的字符有限，没有办法一个灰度值使用一个字符替代，所以使用一种字符替换三个相近灰度值的部分，我们可以使用"$"字符替代灰度值为0、1、2黑色的部分，用"."字符替代灰度值为251、252、253的部分，而254、255这样白色的使用空字符 " "

# 安装pillow(PIL)库:
	$ sudo apt-get update
	$ sudo apt-get install python-dev
	$ sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
	$ sudo pip install pillow
	
# 编写代码

## 导入的库
	from PIL import Image
	import argparse

	parser = argparse.ArgumentParser()

	parser.add_argument('file')     #输入文件
	parser.add_argument('-o', '--output')   #输出文件
	parser.add_argument('--width', type = int, default = 80) #输出字符画宽
	parser.add_argument('--height', type = int, default = 80) #输出字符画高

图片的处理使用PIL库中的image
argpase 是解析命令行参数和选择的模块，如需了解，百度谷歌

## 用于替换图片的字符列表：

	ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
	
## RGB值转换字符的函数

	def get_char(r,g,b,alpha = 256):
	    if alpha == 0:
		return ' '
	    length = len(ascii_char)
	    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

	    unit = (256.0 + 1)/length
	    return ascii_char[int(gray/unit)]

注意几个灰度值共用一个字符

## 使用Image处理图片

	im = Image.open(IMG)
	im = im.resize((WIDTH,HEIGHT), Image.NEAREST)
	
image.open(),打开相应的照片，并返回一对象
resize()函数处理图片的缩放，WIDTH，HEIGHT则是缩放后的宽高，NEAREST则是缩放的质量，此处是最低质量
**（ PIL.Image.NEAREST：最低质量， PIL.Image.BILINEAR：双线性，
PIL.Image.BICUBIC：三次样条插值，Image.ANTIALIAS：最高质量）**

## 生成表示字符画的字符串

	for i in range(HEIGHT):
		for j in range(WIDTH):
		    txt += get_char(*im.getpixel((j,i)))
		txt += '\n'
	
**im.getpixel(xy) 返回给定位置的像素值。返回一个含有r,g,b三个值的元组
注意元组前面加*号传入Python函数时，元组中的元素被解开作为独立的参数依次传给python函数**

# 完整参考代码

	 from PIL import Image
	import argparse


	parser = argparse.ArgumentParser() #命令行输入参数处理

	parser.add_argument('file')     #输入文件
	parser.add_argument('-o', '--output')   #输出文件
	parser.add_argument('--width', type = int, default = 80) #输出字符画宽
	parser.add_argument('--height', type = int, default = 80) #输出字符画高


	args = parser.parse_args() #获取参数

	IMG = args.file
	WIDTH = args.width
	HEIGHT = args.height
	OUTPUT = args.output

	ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


	def get_char(r,g,b,alpha = 256): # 将256灰度映射到70个字符上
	    if alpha == 0:
		return ' '
	    length = len(ascii_char)
	    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

	    unit = (256.0 + 1)/length
	    return ascii_char[int(gray/unit)]

	if __name__ == '__main__':

	    im = Image.open(IMG)
	    im = im.resize((WIDTH,HEIGHT), Image.NEAREST)

	    txt = ""

	    for i in range(HEIGHT):
		for j in range(WIDTH):
		    txt += get_char(*im.getpixel((j,i)))
		txt += '\n'

	    print txt


	    if OUTPUT:     #字符画输出到文件
		with open(OUTPUT,'w') as f:
		    f.write(txt)
	    else:
		with open("output.txt",'w') as f:
		    f.write(txt)
		    
# 运行程序
默认输出文件名output.txt，图片默认高宽80

	python image_ascii.py image.jpg


也可以这样制定输出文件名和高宽

	python image_ascii.py image.jpg -o put.txt --width 40 --height 40


# 效果图
	自己的照片对应的字符画
![](/static/editor.md/photoupdate/2017-08-15--12.png)
	网上找的卡通照片原图以及对应的字符画
![](/static/editor.md/photoupdate/2017-08-15--0.jpg) 
![](/static/editor.md/photoupdate/2017-08-15--21.png)