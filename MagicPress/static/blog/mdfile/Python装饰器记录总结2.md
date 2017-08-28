>**装饰器是一个函数,一个用来包装函数的函数，装饰器在函数申明（不需要调用）完成的时候被调用，调用之后返回一个修改之后的函数对象，将其重新赋值原来的标识符，并永久丧失对原始函数对象的访问。对某个方法应用了装饰方法后， 其实就改变了被装饰函数名称所引用的函数代码块入口点，使其重新指向了由装饰方法所返回的函数入口点。**





# 无参数装饰器-包装无参数函数
这是一个打印log的decorator，此时输出了函数名、返回值、运行时间。

	import time
	from functools import wraps
	def log(func):
	    @wraps(func)
	    def wrapper():
			print("function runing")
			ts = time.time()
			result = func()
			te = time.time()
			print("function      = {0}".format(func.__name__))
			print("  return      = {0}".format(result))
			print("    time      = %.6f sec" % (te - ts))
	    return wrapper

	@log
	def sum():
	    x = 1
	    y = 2
	    return x + y

	sum()
	
运行结果:

	function runing
	function      = sum
	  return      = 3
	    time      = 0.000001 sec
    
代码中在sum函数上一行添加@log相当于执行了语句:

	sum = log(sum)
	
由于log()是一个decorator，返回一个函数，所以，原来的sum()函数仍然存在，只是现在同名的sum变量指向了新的函数，于是调用sum()将执行新函数，即在log()函数中返回的wrapper()函数

# 无参数装饰器-包装有参数函数

	import time
	from functools import wraps
	def log(func):
	    @wraps(func)
	    def wrapper(*args, **kwargs): # 接受传入的参数
			print("function runing")
			ts = time.time()
			result = func(*args, *kwargs) # 函数使用传入的参数
			te = time.time()
			print(" function      = {0}".format(func.__name__))
			print("arguments      = {0} {1}".format(args, kwargs))
			print("   return      = {0}".format(result))
			print("     time      = %.6f sec" % (te - ts))
	    return wrapper

	@log
	def sum(x,y):
	    return x + y

	sum(1,2)
	
运行结果：

	function runing
	 function      = sum
	arguments      = (1, 2) 
	   return      = 3
	     time      = 0.000004 sec
	     
# 带参数装饰器 – 包装无参数函数

	import time
	from functools import wraps
	def log(name):
	    def decora(func):
			@wraps(func)
			def wrapper():
				print("name : {0}".format(name))
				print("function runing")
				ts = time.time()
				result = func()
				te = time.time()
				print(" function      = {0}".format(func.__name__))
				print("   return      = {0}".format(result))
				print("     time      = %.6f sec" % (te - ts))
			return wrapper
	    return decora

	@log('MagicRoc')
	def sum():
	    x = 1
	    y = 2
	    return x + y

	sum()
	
运行结果:

	name : MagicRoc
	function runing
	 function      = sum
	   return      = 3
	     time      = 0.000002 sec
	
此时代码中在sum函数上一行添加@log('MagicRoc')相当于执行了语句:

	sum = log('MagicRoc')(sum)
	
首先执行log('MagicRoc')，返回的是decorator函数，再调用返回的函数，参数是sum函数，返回值最终是wrapper函数。

**不同在于：比上一层多了一层封装，先传递参数，再传递函数名**

# 带参数装饰器 – 包装有参数函数

	import time
	from functools import wraps
	def log(name):
	    def decora(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				print("name : {0}".format(name))
				print("function runing")
				ts = time.time()
				result = func(*args, **kwargs)
				te = time.time()
				print(" function      = {0}".format(func.__name__))
				print("arguments      = {0} {1}".format(args, kwargs))
				print("   return      = {0}".format(result))
				print("     time      = %.6f sec" % (te - ts))
			return wrapper
	    return decora

	@log('MagicRoc')
	def sum(x,y):
	    return x + y

	sum(1,2)
	
运行结果：

	name : MagicRoc
	function runing
	 function      = sum
	arguments      = (1, 2) {}
	   return      = 3
	     time      = 0.000002 sec
	     
# 多个Decrorator

	from functools import wraps
	def div(cla):
	    def decara(func):
			@wraps(func)
			def wrapper(*args,**kwargs):
				return "<div class = %s > %s  </div>" % (cla, func())
			return wrapper
	    return decara

	def h1(cla):
	    def decara(func):
			@wraps(func)
			def wrapper(*args,**kwargs):
				return "<h1 class = %s > %s </h1>" % (cla,func())
			return wrapper
	    return decara
	    
	@div('divclass')
	@h1('h1class')
	def hello():
	    return 'hello world'
	    
	print( hello())
	
装饰器的顺序很重要:

	@A
	@B
	@C
	def f ():
等价于:

	f = A(B(C(f)))
	
代码运行过程中中hello先指向了h1中的wrapper，又指向了div中的wrapper。
h1中的func指向的是要修饰的函数本身，而div中的func指向的是h1中的wrapper函数。

# 装饰器类

	from functools import wraps
	import time
	class log(object):
	    def __init__(self,name):
			self.name = name

	    def __call__(self,func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				print("name : {0}".format(self.name))
				print("function runing")
				ts = time.time()
				result = func(*args, **kwargs)
				te = time.time()
				print(" function      = {0}".format(func.__name__))
				print("arguments      = {0} {1}".format(args, kwargs))
				print("   return      = {0}".format(result))
				print("     time      = %.6f sec" % (te - ts))
			return wrapper

	@log('MagicRoc')
	def sum():
	    x = 1
	    y = 2
	    return x + y
	    
	sum()


# 将装饰器定义为类的一部分

用类方法作为装饰器函数和普通函数作为装饰器函数极其相似
	
	from functools import wraps

	class A:
	    def decorator(self, func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)
			return wrapper

使用的时候：
	
	a = A()
	@a.decorator
	def fun():
	    pass


Flask 通过URL的路由来调用相关注册的函数就是将装饰器定义为类的一部分

# 理解Flask 路由注册回调函数

	class MyApp():
	    def __init__(self):
		self.func_map = {}
	 
	    def register(self, name):
			def func_wrapper(func):
				self.func_map[name] = func
				return func
			return func_wrapper
	 
	    def call_method(self, name=None):
			func = self.func_map.get(name, None)
			if func is None:
				raise Exception("No function registered against - " + str(name))
			return func()
	 
	app = MyApp()
	 
	@app.register('/')
	def main_page_func():
	    return "This is the main page."
	 
	@app.register('/next_page')
	def next_page_func():
	    return "This is the next page."
	 
	print app.call_method('/')
	print app.call_method('/next_page')
	
因为这里是带参数的装饰器，所以比之前的要多一层嵌套，最外层的接受参数，其次层的接受函数参数。这里知识把url和对应的回调函数记录在url_map中，所以原样返回原函数就好。就不用定义第三个需要返回的函数了


# 关于整篇文章的wraps装饰器

被decorator的函数其实已经是另外一个函数了，在打印log的例子中，sum函数指向的已经是wrapper函数了，所以输出sum.\_\_name\_\_的值不是sum而是wrapper。不需要编写wrapper.\_\_name\_\_ = func.\_\_name\_\_这样的代码。直接使用wraps装饰器就可以消除这个问题


> 参考链接：
* http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014318435599930270c0381a3b44db991cd6d858064ac0000
* http://coolshell.cn/articles/11265.html
* http://www.wklken.me/posts/2012/10/27/python-base-decorator.html