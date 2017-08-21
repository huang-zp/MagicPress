> **前段时间自学了Flask框架，看得狗书入门，最近做一个新闻发布网站准备拿Flask来做，尝试一下Flask快速开发，并且练练手，于是接触到了Flask-admin。
总结一下Flask-admin**


# 首先需要导入的包
	from flask_admin import Admin,BaseView,expose,AdminIndexView
	from flask_admin.contrib.sqla import ModelView
	
## 效果图
![](/static/editor.md/photoupdate/2017-08-18--1.png)


# 模型视图
* 管理新闻、管理公告、管理文件、管理展示栏是四个与数据库表同步的模型视图，如果你想要在后台管理程序中数据库中的表在初始化admin后仅需一句代码

		admin = Admin(app)
		admin.add_view(ModelView(User, db.session))'

* 但是有时候flask-admin的默认设置并不能满足你的条件，如果我们在后台只打算让表中固定的几列数据显示,这时候我们就不能直接像上面那样直接ModelView，我们需自定义一个类并继承ModelView，并重写一些代码，把想要显示出来的列名写在column_list中

		class MyV1(ModelView):
	    		column_list = ('id', 'title','timestamp','count','content')
	    		def __init__(self, session, **kwargs):
				super(MyV1, self).__init__(News, session, **kwargs)

然后在程序中再加入代码如下，然后就OK了

		admin.add_view(MyV1(db.session,name = u'管理新闻'))

* 如果我们使用flask做网站是给自己使用，后台和数据库中同步的列名是英文显示没有多大影响，自己写的数据库难道还不知道什么意思，但是当我们是写给非技术人员使用时，他们可能不能理解每个列名是什么意思，所以现在我们就需要将列名中文化，也是需要重写column_labels
	
		class MyV1(ModelView):
		    column_labels = {
			'id':u'序号',
			'title' : u'新闻标题',
			'timestamp':u'发布时间',
			'count':u'浏览次数',
			'content':u'新闻内容'
		    }
		    column_list = ('id', 'title','timestamp','count','content')
		    def __init__(self, session, **kwargs):
			super(MyV1, self).__init__(News, session, **kwargs)


* 有时候当同步数据库表成功后，扩展会有一个默认新建数据插入数据库表中的功能，但是我们有时候发表博客、新闻这些需要排版的文章但是默认的新建数据不支持这个功能怎么办，我们可以把默认创建功能先关掉。


		class MyV1(ModelView):
		    can_create = False

		    column_labels = {
			'id':u'序号',
			'title' : u'新闻标题',
			'timestamp':u'发布时间',
			'count':u'浏览次数',
			'content':u'新闻内容'
		    }
		    column_list = ('id', 'title','timestamp','count','content')
		    def __init__(self, session, **kwargs):
			super(MyV1, self).__init__(News, session, **kwargs)
	
# 创建视图

* 上面我们说到讲默认创建功能关掉，但是我们怎么新建数据呢，我们可以自己写一个视图，关联自己的模板，再在模板中集成富文本。

		class MyNews(BaseView):
		  	@expose('/', methods=['GET', 'POST'])
		    	def index(self):
				form = NameForm()
				return self.render('donews.html', form=form)

　　然后再程序中加入代码

		admin.add_view(MyNews(name=u'发表新闻'))

# 对主页面的修改

* Flask-admin默认主页面标题是Home，而且界面一片空白，由于各种需要，我们需要对这些进行更改，参考以下代码
复制代码

		admin = Admin(
		    app,
		    index_view=AdminIndexView(
			name='导航栏',
			template='welcome.html',
			url='/admin'
		    )
		)


将标题修改为导航栏，并将主页设置为welcome.html，进入后台对应的url也可以修改

# 权限设置

* 一般后台并不是对所有用户开放的，所有牵扯到了管理员权限，这一块我是依靠flask-login这个扩展实现的，关于flask-login会再写一遍进行总结，新加代码如下

		class MyNews(BaseView):
		    def is_accessible(self):
			if current_user.is_authenticated and current_user.username == "admin":
			    return True
			return False
		    @expose('/', methods=['GET', 'POST'])
		    def index(self):
			form = NameForm()
			return self.render('donews.html', form=form)

通过判断当前用户登录状态和当前登录的用户名进行权限设置