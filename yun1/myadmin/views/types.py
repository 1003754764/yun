from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types,Goods
from django.core.paginator import Paginator
from django.db.models import Q
from .user import uploads
# Create your views here.
from django.contrib.auth.decorators import permission_required

# 获取所有的分类信息
def gettypes():

	tlist = Types.objects.extra(select={'paths':'concat(path,id)'}).order_by('paths')
	for i in tlist:
		if i.pid == 0:

			i.pname = '顶级分类'

		else:

			t = Types.objects.get(id=i.pid)
			i.pname = t.name
		num = i.path.count(',')-1
		i.name = (num*'|----')+i.name

	return tlist

# 商品分类添加
@permission_required('myadmin.insert_types',raise_exception = True)
def add(request):

	if request.method == 'GET':

		tlist = gettypes()

		# ob = Types.objects.all()

		obj={'content':tlist}

		return render(request,'myadmin/types/add.html',obj)

	elif request.method == 'POST':

		# 执行分类添加

		tlist = Types()

		tlist.name = request.POST['name']

		tlist.pid = request.POST['pid']

		if tlist.pid == '0':

			tlist.path = '0,'

		else:

			t = Types.objects.get(id=tlist.pid)

			tlist.path = t.path+tlist.pid+','

		if request.FILES.get('pic',None):

			tlist.pics = uploads(request)

			# 判断分类图片类型

			if tlist.pics==1:
				return HttpResponse('<script>alert("上传的图片类型不符合要求");location.href="'+reverse('myadmin_user_add')+'"</script>')		

		tlist.save()

		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')

		
# 商品分类列表

@permission_required('myadmin.show_types',raise_exception = True)
def list(request):

	# 获取搜索条件
	types = request.GET.get('type',None)
	# 获取关键字信息
	keywords = request.GET.get('keywords',None)

	if types:

		if types=='all':

			#根据所有关键字段搜索
			typelist = Types.objects.filter(
				Q(id__contains=keywords)|
				Q(name__contains=keywords)|
				Q(pid__contains=keywords)
				).extra(select={'paths':'concat(path,id)'}).order_by('paths')
		# 根据id查询
		elif types=='id':

			typelist = Types.objects.filter(id__contains=keywords).extra(select={'paths':'concat(path,id)'}).order_by('paths')
		# 根据分类名查询
		elif types=='name':

			typelist = Types.objects.filter(name__contains=keywords).extra(select={'paths':'concat(path,id)'}).order_by('paths')

		# elif types=='pname':
			
		# 	typelist = Types.objects.filter(name__contains=keywords).extra(select={'paths':'concat(path,id)'}).order_by('paths')

	else:
		# 获取所有的分类信息
		# typelist = Types.objects.filter()
		typelist = Types.objects.extra(select={'paths':'concat(path,id)'}).order_by('paths')
 	
	for i in typelist:
		if i.pid == 0:

			i.pname = '顶级分类'

		else:

			t = Types.objects.get(id=i.pid)
			i.pname = t.name
		num = i.path.count(',')-1
		i.name = (num*'|----')+i.name
	# 分配数据
	paginator = Paginator(typelist, 10)

    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	tlist = paginator.page(p)


	# for i in tlist:
	# 	if i.pid == 0:
	# 		i.pname = '顶级分类'
	# 	else:
	# 		t = Types.objects.get(id=i.pid)
	# 		i.pname = t.name

	# obj = {'typelist':tylist}

	# return render(request,'myadmin/types/list.html',obj)

	# tlist= gettypes()

	obj = {'tlist':tlist}

	return render(request,'myadmin/types/list.html',obj)

# 商品分类删除
@permission_required('myadmin.del_types',raise_exception = True)
def delete(request):

	uid = request.GET.get('uid',None)
	# 判断是否有子类

	num = Types.objects.filter(pid=uid).count()

	# num2 = Types.objects.get(id=uid)

	# print(num2.Goods_set)
	if num !=0:
		date = {'msg':'当前商品类有其他子类,不能删除','code':1}
	else:
		ob = Types.objects.get(id=uid)
		os.remove('.'+obj.pics)
		ob.delete()

		date = {'msg':'删除成功','code':0}

	return JsonResponse(date)

# 商品分类修改
@permission_required('myadmin.edit_types',raise_exception = True)
def update(request):
	# 获取点击删除的商品分类的id

	uid = request.GET.get('uid',None)

	if not uid:

		return HttpResponse('<script>alert("没有分类信息");location.href="'+reverse('myadmin_types_list')+'"</script>')

	# 根据id在数据库查出此商品分类

	ob = Types.objects.get(id=uid)

	if request.method == 'GET':

		# 分配数据

		obj = {'uinfo':ob}
		
		# 显示修改页面
		return render(request,'myadmin/types/update.html',obj)

	elif request.method == 'POST':

		try:
			if request.FILES.get('pic',None):

                # 判断是否使用的默认图

				if ob.pics:

                    # 如果使用的不是默认图,则删除之前上传的头像

					os.remove('.'+ob.pics)

                # 执行上传
				ob.pics = uploads(request)			
			ob.name = request.POST['name']
			ob.save()

			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_types_list')+'"</script>')
		except:
			return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_types_update')+'?uid='+str(ob.id)+'"</script>')



	



















