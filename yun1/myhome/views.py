from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import Users,Types,Goods,Address,Orders,OrderInfo
from django.contrib.auth.hashers import make_password, check_password


# 首页
def index(request):
	'''
		[
			{
			'name':'点心/蛋糕',
			'sub':[
					{'name':'点心',
						'goodssub':[
							{goods objects},
							{goods objects},
							{goods objects}
						]
					},
					
					{'name':'蛋糕',
						'goodssub':[
							{goods objects},
							{goods objects},
							{goods objects}
						]
					}
				]
			},
			
			{
			'name':'饼干/膨化',
			'sub':[
					{'name':'饼干','goodssub':[{goods objects},{goods objects},{goods objects}]},
					{'name':'膨化','goodssub':[{goods objects},{goods objects},{goods objects}]}
				]
			},
		]
	'''
	# 获取所有的顶级分类
	date = Types.objects.filter(pid=0)

	# 定义二级分类

	erdate = []

	for i in date:
		# 获取当前顶级分类下的子类
		i.sub = Types.objects.filter(pid=i.id)

		for j in i.sub:
			# 获取子类下的商品
			j.goodssub = Goods.objects.filter(typeid=j.id)

			erdate.append(j)

	obj = {'tglist':date,'erdate':erdate}

	return render(request,'myhome/index.html',obj)
	
	# return HttpResponse('首页')


# 列表页
def list(request,tid):

	# 根据分类id获取商品

	date = Goods.objects.filter(typeid=tid)

	context = {'glist':date}
	return render(request,"myhome/list.html",context)

# 详情页
def info(request,sid):
	try:
		# 根据商品id获取商品信息
		date = Goods.objects.get(id=sid)
		
		# 修改商品的点击量
		date.clicknum = date.clicknum+1

		# print(date.clicknum)

		# date.price = float(date.price)

		date.save()

		context = {'ginfo':date,'pricea':float(date.price)}
		return render(request,"myhome/info.html",context)

	except:

		pass

# 登录
def login(request):

	nexturl = request.GET.get('next','/')
	if request.method == 'GET':

		return render(request,"myhome/login.html")

	elif request.method == 'POST':

		# 判断用户是否存在,密码是否正确

		try:

			ob = Users.objects.get(username=request.POST['username'])

			# 密码解密,检测密码是否一致

			pwd = check_password(request.POST['password'],ob.password)

			# 判断密码
			if pwd:


				request.session['VipUser'] = {'uid':ob.id,'username':ob.username}

				return HttpResponse('<script>alert("登录成功");location.href="'+nexturl+'"</script>')

		except:

			pass

		return HttpResponse('<script>alert("用户名或密码错误");history.back(-1)</script>')


# 退出登录
def logout(request):

	request.session['VipUser'] = {}
				
	return HttpResponse('<script>alert("退出成功");location.href="/"</script>')


# 注册
def register(request):

	if request.method == 'GET':

		return render(request,'myhome/register.html')

	elif request.method == 'POST':

		# 判断验证码是否一致

		if request.POST['vcode'].upper() != request.session['verifycode'].upper():

			return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')

		# 获取表单数据

		date = request.POST.copy().dict()

		# 删除掉 csrf验证的字段数据

		del date['csrfmiddlewaretoken']

		# 删除验证码
		del date['vcode']

		try:
			# 密码加密

			date['password'] = make_password(date['password'],None, 'pbkdf2_sha256')

			ob = Users.objects.create(**date)

			request.session['VipUser'] = {'uid':ob.id,'username':ob.username}

			return HttpResponse('<script>alert("注册成功");location.href="/"</script>')

		except:

			pass

		return HttpResponse('<script>alert("注册失败");history.back(-1)</script>')


# 搜索

def search(request):

	# 获取搜索参数值

	keywords = request.GET.get('keywords',None)

	if not keywords:

		# 如果搜索参数为空,则返回上一步

		return HttpResponse('<script>history.back(-1)</script>')

	date = Goods.objects.filter(title__contains=keywords)

	context = {'glist':date}

	return render(request,'myhome/search.html',context)



# 验证码
def vcode(request):
	#引入绘图模块
	from PIL import Image, ImageDraw, ImageFont
	#引入随机函数模块
	import random
	#定义变量，用于画面的背景色、宽、高
	bgcolor = (random.randrange(20, 100), random.randrange(
		20, 100), 255)
	width = 100
	height = 25
	#创建画面对象
	im = Image.new('RGB', (width, height), bgcolor)
	#创建画笔对象
	draw = ImageDraw.Draw(im)
	#调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		draw.point(xy, fill=fill)
	#定义验证码的备选值
	str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	#随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str1[random.randrange(0, len(str1))]
	#构造字体对象
	font = ImageFont.truetype('FreeMono.ttf', 23)
	#构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	#绘制4个字
	draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
	draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
	#释放画笔
	del draw
	#存入session，用于做进一步验证
	request.session['verifycode'] = rand_str
	#内存文件操作
	import io
	buf = io.BytesIO()
	#将图片保存在内存中，文件类型为png
	im.save(buf, 'png')
	#将内存中的图片数据返回给客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'image/png')


# 加入购物车
def addcart(request):

	# 获取商品id,商品购买数量
	sid = request.GET['sid']

	num = int(request.GET['num'])

	# 先获取购物车的商品数据

	date = request.session.get('cart',{})


	# 判断商品是否在购物车里
	if sid in date.keys():
		# 存在商品数量相加
		date[sid]['num'] += num

	else:
		# 不存在
		ob = Goods.objects.get(id=sid)

		goods = {'id':ob.id,'title':ob.title,'price':float(ob.price),'pics':ob.pics,'num':num}

		date[sid] = goods

	# 把购物车存入session

	request.session['cart'] = date

	return HttpResponse(1)


# 购物车列表
def cartlist(request):

	# ob = request.session.get('cart',None)	
	ob = request.session['cart']

	if ob:
		date = ob.values()
	else:
		date={}

	# for i in date:
	# 	print(i.num)

	return render(request,'myhome/cart.html',{'date':date})




# 删除购物车的商品
def delcart(request):
	# 获取商品id
	sid = request.GET['sid']
	# 获取购物车数据
	date = request.session['cart']
	# 删除商品id相等的购物车商品
	del date[sid]
	# 重新存入session
	request.session['cart'] = date

	return HttpResponse('0')



# 修改购物车的商品数量
def updatecart(request):
	
	sid = request.GET['sid']

	num = int(request.GET['num'])

	date = request.session['cart']

	date[sid]['num'] = num

	request.session['cart'] = date

	return HttpResponse('0')

# 清空购物车
def cartclear(request):
	
	request.session['cart'] = {}

	return HttpResponse('<script>location.href="/cartlist/"</script>')

# 订单确认
def ordercheck(request):
	items = eval(request.GET['items'])
	date = {}
	totalprice = 0
	totalnum = 0

	for i in items:
		ob = Goods.objects.get(id=i['goodsid'])
		i['title'] = ob.title
		i['price'] = float(ob.price)
		i['pics'] = ob.pics

		totalprice += i['num']*i['price']
		totalnum += i['num']
	date['totalprice'] = round(totalprice,2)
	date['totalnum'] = totalnum
	date['items'] = items

	request.session['order'] = date
	addlist = Address.objects.filter(uid=request.session['VipUser']['uid'])
	context = {'date':date,'addlist':addlist}

	return render(request,'myhome/ordercheck.html',context)




# 收货地址修改
def addressedit(request):
	aid = int(request.GET['aid'])
	uid = request.session['VipUser']['uid']
	# 获取当前用户的所有收货地址
	obs = Address.objects.filter(uid=uid)
	for i in obs:
		if i.id == aid:
			i.status = 1
		else:
			i.status = 0
		i.save()

	return HttpResponse(0)

# 收货地址增加
def addressadd(request):
	# 获取地址信息
	date = eval(request.GET['date'])
	# 地址信息拼接
	date['address']=','.join(date['address'])
	# 记录用户id
	date['uid'] = Users.objects.get(id=request.session['VipUser']['uid'])
	# 添加地址信息
	res = Address.objects.create(**date)

	return HttpResponse(0)

# 生成订单
def ordercreate(request):
	# 接收用户id
	uid = request.session['VipUser']['uid']
	# 收货地址id
	addressid = request.POST['addressid']
	# 商品信息
	date = request.session['order']
	# 购物车数据
	cart = request.session['cart']

	# 生成订单
	ob = Orders()

	ob.uid = Users.objects.get(id=uid)

	ob.addressid = Address.objects.get(id=addressid)

	ob.totalprice = date['totalprice']

	ob.totalnum = date['totalnum']

	ob.save()
	# 订单详情
	for i in date['items']:
		oinfo = OrderInfo()
		oinfo.orderid = ob
		oinfo.gid = Goods.objects.get(id=i['goodsid'])
		oinfo.num = i['num']
		oinfo.save()
		# 在购物车中删除当前购买的商品
		del cart[i['goodsid']]
	# 清除购物车中已经够买的商品,清除order数据
	request.session['cart'] = cart
	request.session['order'] = ''

	return HttpResponse('<script>location.href="/buy/?orderid='+str(ob.id)+'"</script>')

# 进行支付
def buy(request):
	# 获取订单id
	orderid = request.GET['orderid']
	# 获取订单信息
	date = Orders.objects.get(id=orderid)
	# 分配数据
	context = {'date':date}

	return render(request,'myhome/buy.html',context)

# 个人中心
def mycenter(request):
	
	return render(request,'myhome/word/index.html')


def information(request):
	
	uid = request.session['VipUser']['uid']

	date = Users.objects.get(id=uid)


	obj = {'uinfo':date}

	return render(request,'myhome/word/information.html',obj)

# 我的订单
def myorders(request):

	# 获取当前用户的所有订单信息
	
	date = Orders.objects.filter(uid=request.session['VipUser']['uid'])

	context = {'orderlist':date}

	return render(request,'myhome/word/myorders.html',context)



