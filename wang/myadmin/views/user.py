from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
# Create your views here.
from .. models import Users
from django.contrib.auth.hashers import make_password
import time,random,os
from django.core.paginator import Paginator
from django.db.models import Q

# 会员添加
def add(request):
	if request.method == 'GET':

		# 显示添加页面
		return render(request,'myadmin/user/add.html')

	elif request.method == 'POST':

		# 执行会员添加
		try:
			# 格式化表单提及的数据

			date = request.POST.copy().dict()

			# 删除掉 csrf验证的字段数据

			del date['csrfmiddlewaretoken']

			# 加密密码

			date['password']=make_password(date['password'],None, 'pbkdf2_sha256')

			# 会员头像上传
			if request.FILES.get('pic',None):

				date['pic'] = uploads(request)

				# 判断头像图片类型

				if date['pic']==1:
					return HttpResponse('<script>alert("上传的图片类型不符合要求");location.href="'+reverse('myadmin_user_add')+'"</script>')
				# else:
					# del date['pic']
			# 会员创建

			Users.objects.create(**date)

			return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_user_list')+'"</script>')

		except:

			return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_user_add')+'"</script>')


# 会员列表
def list(request):


	# 获取搜索条件
	types = request.GET.get('type',None)
	# 获取关键字信息
	keywords = request.GET.get('keywords',None)

	if types:

		if types=='all':

			#根据所有关键字段搜索
			userlist = Users.objects.filter(
				Q(id__contains=keywords)|
				Q(username__contains=keywords)|
				Q(age__contains=keywords)|
				Q(email__contains=keywords)|
				Q(phone__contains=keywords)|
				Q(sex__contains=keywords)
				)
		# 根据id查询
		elif types=='id':

			userlist = Users.objects.filter(id__contains=keywords)
		# 根据会员名查询
		elif types=='username':

			userlist = Users.objects.filter(username__contains=keywords)
		# 根据年龄查询
		elif types=='age':

			userlist = Users.objects.filter(age__contains=keywords)
		# 根据邮箱查询
		elif types=='email':

			userlist = Users.objects.filter(email__contains=keywords)
		# 根据手机号查询
		elif types=='phone':

			userlist = Users.objects.filter(phone__contains=keywords)
		# 根据性别查询
		elif types=='sex':

			userlist = Users.objects.filter(sex__contains=keywords)
	else:
		# 获取所有的会员信息
		userlist = Users.objects.filter()

	# 获取所有的会员信息

	# userlist = Users.objects.all()

	# 分配数据
	paginator = Paginator(userlist, 10)
    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	ulist = paginator.page(p)

	obj = {'userlist':ulist}

	return render(request,'myadmin/user/list.html',obj)


# 会员删除

def delete(request):

	# 获取点击删除的会员的id

	uid = request.GET.get('uid',None)

	# 根据id在数据库查出此会员

	obj = Users.objects.get(id=uid)

	try:

		# 判断此会员有没有头像

		if obj.pic:

			os.remove('.'+obj.pic)

		# 在数据库中删除此会员

		obj.delete()

		date = {'str':'删除成功','code':1}
		# return JsonResponse(date)

	except:

		date = {'str':'删除失败','code':0}
		
	return JsonResponse(date)


	# return HttpResponse('删除')



# 会员修改

def update(request):
	# 获取点击删除的会员的id

	uid = request.GET.get('uid',None)

	# 根据id在数据库查出此会员

	ob = Users.objects.get(id=uid)

	if request.method == 'GET':

		# 分配数据

		obj = {'uinfo':ob}
		
		# 显示修改页面
		return render(request,'myadmin/user/update.html',obj)

	elif request.method == 'POST':

		try:
            # 判断是否上传新的图片
			if request.FILES.get('pic',None):

                # 判断是否使用的默认图

				if ob.pic:

                    # 如果使用的不是默认图,则删除之前上传的头像

					os.remove('.'+ob.pic)

                # 执行上传
				ob.pic = uploads(request)
                

			ob.username = request.POST['username']
			ob.email = request.POST['email']
			ob.age = request.POST['age']
			ob.sex = request.POST['sex']
			ob.phone = request.POST['phone']
			ob.save()

			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
		except:
			return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_user_update')+'?uid='+str(ob.id)+'"</script>')




# 图片上传
def uploads(request):
    
    # 获取请求中的 文件
    myfile = request.FILES.get('pic',None)

    # 获取上传的文件后缀名
    p = myfile.name.split('.').pop()

    # 定义图片类型

    arr = ['jpg','png','jpeg','gif']

    # 判断图片类型

    if p not in arr:
        return 1


    # 生成新的文件名
    filename = str(time.time())+str(random.randint(1,99999))+'.'+p
    
    # 打开文件
    destination = open("./static/pics/"+filename,"wb+")

    # 分块写入文件  
    for chunk in myfile.chunks():      
       destination.write(chunk)  

    # 关闭文件
    destination.close()
    
    # 返回拼接的图片地址

    return '/static/pics/'+filename