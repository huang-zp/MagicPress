>** 很简单的一个python写的程序，每天早晨六点自动发送邮件到指定邮箱，邮件内容包括当地天气、笑话、英语单词。天气和笑话通过调用API，英语单词通过文件读取**



# 首先实现邮件发送

通过email 和 smtplib实现,需要导入的库

	from email import encoders
	from email.header import Header
	from email.mime.text import MIMEText
	from email.utils import parseaddr, formatadd
	import smtplib
	

设置邮箱表标题，发件人，收件人，以及邮箱内容

	msg = MIMEText(location+temp+weather+weatime+jokeall+jokeword, 'plain','utf-8')
    msg['From'] = _format_addr('Everymail <%s>' % from_addr)
    msg['To'] = _format_addr('管理员 <%s>' % to_addr)
    msg['Subject'] = Header('The New day', 'utf-8').encode()
    
    
生成实例，登录发送
    	
	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
	
接下的只要任务是获取MIMEText中的那些参数
**location ：当地位置
temp：当地温度
weather：当地天气
weatime：天气更新时间
jokeword：十个单词
jokeall：一个笑话**

# 天气的获取
    	
程序调用的是心知天气的API

	def fetchWeather():

	    location = getLocation()
	    result = requests.get(API, params={
		'key': KEY,
		'location': location,
		'language': LANGUAGE,
		'unit': UNIT
	    }, timeout=100)
	    values = json.loads(result.text)
	    results = values["results"][0]
	    wea = results["now"]
	    time = re.sub(r'([\d|-]+)T([\d|:]+).+', r'\1 \2', results["last_update"])
	    return wea,time
	    
通过json.loads将返回的json数据解析，然后一层一层的取出，天气，温度，和时间。因为返回的时间格式一点不适合查看，故用正则将其转化为常见的时间格式

# 笑话的获取

程序调用的是来福岛的笑话接口

	def fetchjoke():
	    showapi_appid = id  #替换此值
	    showapi_sign = key  #替换此值
	    url="http://route.showapi.com/341-1"
	    send_data = parse.urlencode([
	    ('showapi_appid', showapi_appid)
	    ,('showapi_sign', showapi_sign)
		            ,('time', "")
		            ,('page', "")
		            ,('maxResult', "")
	     
	  ])
	    req = request.Request(url)
	    with request.urlopen(req, data=send_data.encode('utf-8')) as f:
		str_res= f.read().decode('utf-8')
		json_res=json.loads(str_res)
		a = 1
		joketitle = []
		jokecontext = []
		jokeall = ""
		for i in json_res['showapi_res_body'].get("contentlist"):
		    joketitle.append(i["title"])
		    jokecontext.append(i["text"])
		    jokeall = jokeall + '标题 : ' + i["title"] + '\n'
		    jokeall = jokeall + '内容 : \n' + i["text"] + '\n\n'
		    a+=1
		    break
		return(jokeall)

也是通过json.loads解析返回的json数据，然后取出所需要的数据，作为函数返回数据

# 单词的获取

单词是从一个txt文件按顺序读取的，之前把四级单词全部复制进去。但是有时候程序可能crash，重新启动程序的时候可能又要从第一个单词开始读取了，所以又多了一个文件用来记录每次读取的位置

	def fetchword():
	    theword = ""
	    with open('value.txt',"r") as f1,open('recoad.txt',"r") as f2:
		flag = f2.read()
		count = 1
		for i in f1:
		    count+=1
		    if (count >= int(flag)):
		        theword = theword + str(i) + "\n";
		        if(count == int(flag)+10):
		            break
	    with open("recoad.txt","w") as f:
		f.write(str(int(flag)+10))
	    return theword
	    
# 定时发送

	import threading
	import time
	from sendmail import send
	def outosend():
	    send()
	    global t    #Notice: use global variable!
	    t = threading.Timer(86400.0, outosend)    # 定时器
	    t.start()
	t = threading.Timer(5.0, outosend)
	while 1:
	    if time.localtime()[3] == 6:  # 判断现在是不是早晨六点
		t.start()   
		break     # 线程不能重复开始，不然会有警告


通过Timer定时器实现每86400秒（一天）发送一次，通过递归实现程序一直运行此函数。
但是为了保证在六点发送，然后下一次发送也是六点，所有通过time.localtime判断现在的时间是不是到六点，一旦正确，线程开始启动

## 同时发送多个邮箱

为了保证同时发送多个邮箱，所以把要发送的邮箱写入了文件，然后通过文件一个一个的读取
	
	with open("emails.txt","r") as f:
		emails = f.readlines()
	

	    for to_addr in emails:
		msg['To'] = _format_addr('管理员 <%s>' % to_addr)
		
![](/static/editor.md/photoupdate/2017-08-15--3.png)
![](/static/editor.md/photoupdate/2017-08-15--4.png)