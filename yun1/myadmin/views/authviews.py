from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse

from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,login,logout


# 用户添加
def useradd(request):

	if request.method == 'GET':

		# 显示添加页面
		# 获取组信息
		glist = Group.objects.all()

		obj = {'glist':glist}

		return render(request,'auth/user/add.html',obj)

	elif request.method == 'POST':
		# 进行管理员添加

		# 判断是否创建超级用户

		if request.POST['is_superuser'] == '1':

			ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])

		else:

			ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])


		# 添加
		ob.save()

		gs = request.POST.getlist('gs',None)

		if gs:

			ob.groups.set(gs)

			ob.save()
		
		return HttpResponse('<script>alert("添加成功");location.href="/myadmin/auth/user/list"</script>')



# 用户列表
def userlist(request):

	date = User.objects.all()

	obj = {'ulist':date}
	
	return render(request,'auth/user/list.html',obj)

# 用户删除
def userdel(request,uid):

	ob = User.objects.get(id=uid)

	ob.delete()

	return HttpResponse('<script>alert("删除成功");location.href="/myadmin/auth/user/list"</script>')

# 组添加
def groupadd(request):
	
	if request.method == 'GET':

		# perms = Permission.objects.all()

		perms = Permission.objects.exclude(name__istartswith='Can')

		obj = {'perms':perms}

		return render(request,'auth/group/add.html',obj)

	elif request.method == 'POST':


		g = Group(name=request.POST['name'])

		g.save()

		perms = request.POST.getlist('prms',None)

		if perms:

			g.permissions.set(perms)

			g.save()

		return HttpResponse('<script>alert("添加成功");location.href="/myadmin/auth/group/list"</script>')





# 组列表
def grouplist(request):

	date = Group.objects.all()

	obj = {'glist':date}
	

	return render(request,'auth/group/list.html',obj)


# 修改组
def groupedit(request,gid):
	
	# 获取当前组的信息

	ginfo = Group.objects.get(id=gid)

	if request.method == 'GET':

		perms = Permission.objects.exclude(group=ginfo).exclude(name__istartswith='Can')
		
		obj = {'ginfo':ginfo,'perms':perms}

		return render(request,'auth/group/edit.html',obj)

	elif request.method == 'POST':

		ginfo.name = request.POST['name']

		perms = request.POST.getlist('prms',None)

		ginfo.permissions.clear()

		if perms:

			ginfo.permissions.set(perms)

		ginfo.save()


		return HttpResponse('<script>alert("修改成功");location.href="/myadmin/auth/group/list"</script>')


# 后台登录
def mylogin(request):
	
	if request.method == 'GET':

		return render(request,'myadmin/login.html')

	elif request.method == 'POST':

		# 判断验证码是否正确
		if request.POST['vcode'].lower()!= request.session['verifycode'].lower():

			return HttpResponse('<script>alert("验证码错误");location.href="/myadmin/mylogin"</script>')

		# 使用django验证后台用户

		username = request.POST['username']

		password = request.POST['password']

		user = authenticate(request,username=username,password=password)

		if user:

			login(request,user)
			return HttpResponse('<script>alert("登录成功");location.href="/myadmin/"</script>')

		return HttpResponse('<script>alert("用户名或密码不正确");location.href="/myadmin/mylogin"</script>')



# 退出登录
def mylogout(request):

	logout(request)

	return HttpResponse('<script>alert("退出成功");location.href="/myadmin/mylogin"</script>')







