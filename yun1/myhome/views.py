from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from myadmin.models import Users,Types,Goods
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
		date = Goods.objects.filter(id=sid)

		context = {'ginfo':date}
		return render(request,"myhome/info.html",context)

	except:

		pass

# 登录
def login(request):

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

				return HttpResponse('<script>alert("登录成功");location.href="/"</script>')

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