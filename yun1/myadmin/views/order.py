from django.shortcuts import render,reverse
from django.http import HttpResponse
# Create your views here.
from ..models import Orders,OrderInfo
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

# 订单列表
@permission_required('myadmin.show_order',raise_exception = True)
def list(request):
	# 获取搜索条件
	types = request.GET.get('type',None)
	# 获取关键字信息
	keywords = request.GET.get('keywords',None)

	if types:

		if types=='all':

			#根据所有关键字段搜索
			orderlist = Orders.objects.filter(
				Q(id__contains=keywords)|
				Q(totalprice__contains=keywords)|
				Q(totalnum__contains=keywords)|
				Q(status__contains=keywords)|
				Q(addtime__contains=keywords)
				)
		# 根据id查询
		elif types=='id':

			orderlist = Orders.objects.filter(id__contains=keywords)
		# 根据会员名查询
		elif types=='username':

			orderlist = Orders.objects.filter(uid__username__contains=keywords)
		# 根据商品总价查询
		elif types=='totalprice':

			orderlist = Orders.objects.filter(title__contains=keywords)
		# 根据商品数量查询
		elif types=='totalnum':

			orderlist = Orders.objects.filter(price__contains=keywords)
		# 根据订单状态查询
		elif types=='status':

			orderlist = Orders.objects.filter(store__contains=keywords)

		# 根据订单添加时间查询
		elif types=='addtime':

			orderlist = Orders.objects.filter(addtime__contains=keywords)

	else:
		# 获取所有的订单信息
		orderlist = Orders.objects.filter()
	# 分配数据
	paginator = Paginator(orderlist, 10)
    # 获取当前页码数
	p = request.GET.get('p',1)
    # 获取当前页的数据
	olist = paginator.page(p)

	obj = {'olist':olist}

	return render(request,'myadmin/order/list.html',obj)



# 订单详情
def info(request):
	
	oid = request.GET.get('oid')

	date = OrderInfo.objects.filter(orderid=oid)

	obj = {'oinfo':date,'oid':oid}

	return render(request,'myadmin/order/info.html',obj)




# 订单状态
@permission_required('myadmin.edit_order',raise_exception = True)
def status(request):
	
	oid = request.GET.get('oid')

	date = Orders.objects.get(id=oid)

	if request.method == 'GET':

		obj = {'oinfo':date}

		return render(request,'myadmin/order/status.html',obj)

	elif request.method == 'POST':

		try:
		# print(request.POST['status'],type(int(request.POST['status'])))
			date.status = int(request.POST['status'])
		# print(date.status,type(date.status))
			date.save()
		# return HttpResponse('0')
			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_order_list')+'"</script>')
		except:
			return HttpResponse('<script>alert("修改失败");location.href="'+reverse('myadmin_order_status')+'?oid='+str(date.id)+'"</script>')





