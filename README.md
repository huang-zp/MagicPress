# 部署网址：http://huangzp.com/

>**What is MagicPress ?。这是一款基于Flask的个人博客。页面简洁，但是功能齐全。集成了Editor.md，所以可以使用MakeDown语法编写文章。创新点在于Editor.md与Flask-admin的完美结合、Editor.md与七牛云API的结合、多主题功能、还有各种提升体验的小创新**

**这个网站就是MagicPress部署后的效果，前台如你所见**

## 登陆后部分后台效果图

**后台主页：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-FyiO9-admin.png)

**文章管理：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-dNwDk-adminarticle.png)

**配图管理：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-aHaWa-adminpicture.png)

**评论管理：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-PUYVz-comment.png)

**主题更换：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-Evd8V-theme.png)

**编写文章：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-JjPJa-write.png)

**修改文章：**
![](http://oumkbl9du.bkt.clouddn.com/2017-08-27-tEXMN-savewrite.png)


## 技术点：
* flask-admin与Editor.md的结合
解决办法：继承Flask-admin默认页面， 并修改之（list, create, edit等页面...），使用自己的表单，并对Textarea使用Editor.md
* 图片的处理
解决办法：Editor.md自身的图片上传介绍很容易看懂，写个接口返回指定个数json数据就OK，但是一些注意的点
1.Flask最好使用5000默认端口，类似8080端口editor图片上传一直发起get请求（找了整整一天...）、
2.使用七牛云图床：现在写文章很多都会选择把图片放在图床上， 使用七牛云图床SDK结合自己写的Editor.md上传图片接口吗，直接返回此图片在七牛云的外链（感觉非常良好...比七牛云上传插件，命令行上传什么的简单多了）
3.使用tinify压缩优化图片，容量缩小很多，图片效果几乎没变化（很厉害）
* 修改文章的默认数据
解决办法：看了一点wtforms的文档就解决了..。可能是之前没有想过这个问题, 还有标签和类别两个选择框，还是看官方文档
* 主题的处理
解决办法，其实这个不难，只需要一个开关就好，最初我设置在了app的config中，后来感觉动态更改app配置有些不妥，于是写在文件中，对读取文件的函数进行缓存操作，只要不更换主题就不用重新读取，最后发现还是太年轻...总之最后还是直接写在了文件，没有用缓存。
* 配图的处理
解决办法：为了方便的管理，修改了flask-admin的默认显示，通过column_formatters属性写了处理函数， 覆盖了图片表默认显示
* 评论的处理
解决办法：DFA算法敏感词过滤，taobao开放ip查询接口
* 权限处理
解决办法：Flask-security， 简单快捷
* 数据库设计
使用flask-sqlalchemy, 其他就是一对多，多对多，分页使用flask-sqlalchemy的paginate()。
* 数据库迁移
使用flask-migrate
* 缓存
flask-cache，写了缓存的自定义装饰器，(redis正在写)

还有一些其他的小知识点，应该没必要列出来了。。。以上某些我感觉需要总结的有时间再单开一篇文章去写。

MagicPress写到现在感觉对Flask的项目结构化有了更清晰的理解，对Flask-admin的使用更加顺手，可以更快的定位问题与设计解决办法，增加功能块的时候会先画流程再编码





