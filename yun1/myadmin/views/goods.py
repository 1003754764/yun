from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
# Create your views here.
from ..models import Types,Goods
from django.core.paginator import Paginator
from django.db.models import Q
from .user import uploads

import os

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

def add(request):

	if request.method=='GET':
		tlist = gettypes()
		obj = {'tlist':tlist}
		return render(request,'myadmin/goods/add.html',obj)
	elif request.method == 'POST':

		# 执行商品添加
		try:
			# 判断商品图片是否上传
			if request.FILES.get('pic',None):

				pic = uploads(request)

				# 判断头像图片类型

				if pic==1:
					return HttpResponse('<script>alert("上传的图片类型不符合要求");location.href="'+reverse('myadmin_goods_add')+'"</script>')
				# else:
					# del date['pic']
			else:

				return HttpResponse('<script>alert("请上传商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')

			# 格式化表单提交的数据

			date = request.POST.copy().dict()

			# 删除掉 csrf验证的字段数据

			del date['csrfmiddlewaretoken']

			date['pics'] = pic
			date['typeid'] = Types.objects.get(id=date['typeid'])
			# 商品创建

			Goods.objects.create(**date)

			return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')

		except:

			return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_goods_add')+'"</script>')



def list(request):
	# 获取搜索条件
	types = request.GET.get('type',None)
	# 获取关键字信息
	keywords = request.GET.get('keywords',None)

	if types:

		if types=='all':

			#根据所有关键字段搜索
			goodslist = Goods.objects.filter(
				Q(id__contains=keywords)|
				Q(title__contains=keywords)|
				Q(price__contains=keywords)|
				Q(store__contains=keywords)|
				Q(clicknum__contains=keywords)|
				Q(num__contains=keywords)|
				Q(addtime__contains=keywords)
				)
		# 根据id查询
		elif types=='id':

			goodslist = Goods.objects.filter(id__contains=keywords)
		# 根据商品名查询
		elif types=='title':

			goodslist = Goods.objects.filter(title__contains=keywords)
		# 根据商品价格查询
		elif types=='price':

			goodslist = Goods.objects.filter(price__contains=keywords)
		# 根据商品库存查询
		elif types=='store':

			goodslist = Goods.objects.filter(store__contains=keywords)
		# 根据商品点击量查询
		elif types=='clicknum':

			goodslist = Goods.objects.filter(clicknum__contains=keywords)
		# 根据商品购买量查询
		elif types=='num':

			goodslist = Goods.objects.filter(num__contains=keywords)
		# 根据商品添加时间查询
		elif types=='addtime':

			goodslist = Goods.objects.filter(addtime__contains=keywords)
	else:
		# 获取所有的商品信息
		goodslist = Goods.objects.filter()
	# 分配数据
	paginator = Paginator(goodslist, 3)
    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	glist = paginator.page(p)

	obj = {'glist':glist}

	return render(request,'myadmin/goods/list.html',obj)

def delete(request):

	gid = request.GET.get('gid',None)

	obj = Goods.objects.get(id=gid)

	try:

		obj.delete()

		os.remove('.'+obj.pics)

		date = {'msg':"删除成功",'code':1}

	except:

		date = {'msg':'删除失败','code':0}

	return JsonResponse(date)


def update(request):

	# 获取商品ID

	gid = request.GET.get('gid',None)

	# 根据商品id查出商品

	ob = Goods.objects.get(id=gid)

	if request.method == 'GET':

		tlist = gettypes()

		obj = {'glist':ob,'tlist':tlist}

		return render(request,'myadmin/goods/update.html',obj)

	elif request.method == 'POST':

		try:
            # 判断是否上传新的图片
			if request.FILES.get('pic',None):

                # 判断是商品图片是否存在

				if ob.pics:

                    # 删除之前上传的商品

					os.remove('.'+ob.pics)

                # 执行上传
				ob.pics = uploads(request)
                
			ob.typeid = Types.objects.get(id=request.POST['typeid'])
			ob.title = request.POST['title']
			ob.descr = request.POST['descr']
			ob.price = request.POST['price']
			ob.store = request.POST['store']
			# ob.pics = request.POST['pic']
			ob.info = request.POST['info']

			ob.save()

			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
		except:
			return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_goods_update')+'?gid='+str(ob.id)+'"</script>')
















