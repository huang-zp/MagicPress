> **hexo真心很好用，但是如果更换系统或者更换电脑后应该怎么继续维护这个博客呢，我使用了github pages，可以利用github的分支功能解决这个问题，一个分支用来存放Hexo生成的网站原始的文件，另一个分支用来存放生成的静态网页。**


# 前提
	现在已经在一台电脑上搭建好hexo，并且已经部署到github pages，可以成功的发布博客

# 新建分支提交原始文件
## 初始化
在本地博客根目录输入**git init**，为整个hexo目录初始化git环境
## 添加远程库
将本地与github上的仓库建立关联
	
	git remote add origin git@github.com:MagicRoc/MagicRoc.github.io.git
	
## 建立新分支并切换到新分支
新建分支hexo并切换到hexo分支

	git checkout -b hexo
	
## 将hexo生成网站原始的文件提交到hexo分支

	git add -A
	git commit -m "原始文件"
	
## 将hexo分支推送到远程库
	
	git push origin hexo
	
** 现在已经成功备份到hexo分支**

# 换系统或者换电脑之后的hexo数据恢复

## 配置环境
首先在新环境下安装**Node 、Git**
### Node安装
升级系统，安装依赖包
	
	sudo apt-get update
	sudo apt-get install python gcc make g++
	
获取源代码，解压
	
	wget http://nodejs.org/dist/v0.12.9/node-v0.12.9.tar.gz
	tar zxvf node-v0.12.9.tar.gz
	
编译、安装

	cd node-v0.12.4/
	./configure
	sudo make install
	
### Git安装
	
	sudo apt-get install git
	
将本地SSH key添加到github，终端输入：
	
	ssh-keygen -t rsa -C "fengyujiancheng@aliyun.com"

然后将用户主目录中的.ssh目录下的id_rsa.pub文件内容复制，登陆GitHub，打开“Account settings”，“SSH Keys”页面：
然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容。

	最后不要忘记这两行命令
	
	git config --global user.name "MagicROC"
	git config --global user.email "fengyujiancheng@aliyun.com"

## 数据恢复

克隆仓库

	git clone https://github.com/MagicRoc/MagicRoc.github.io.git

切换到hexo分支

	git checkout hexo
	
安装hexo
	
	npm install -g hexo-cli
	
安装依赖包
	
	npm install

安装git部署插件
	
	npm install hexo-deployer-git

** 不需要hexo init这条指令**

测试
	
	hexo g
	hexo s

## 发布博客
在hexo分支下写好新博客后执行以下操作

	git add .
	git commit -m "..."
	git push origin hexo
	
**发布网站到master分支上**
	
	hexo g -d