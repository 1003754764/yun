from django.shortcuts import render
from django.http import HttpResponse
import re


class LoginMiddleware:

	def __init__(self,get_response):

		self.get_response = get_response

	# 把该类实例化的对象当做方法或函数直接调用,触发
	def __call__(self,request):

		# 当前用户请求的url路径

		u = request.path

		# 定义后台验证

		if re.match('/myadmin/',u) and u not in ['/myadmin/mylogin/','/myadmin/vcode/']:

			# 判断是否登录

			if not request.session.get('_auth_user_id',None):

				return HttpResponse('<script>alert("请先登录");location.href="/myadmin/mylogin/"</script>')

		# 定义前台验证

		# 定义前台的需要登录的url路由

		urllist = ['/ordercheck/','/addressedit/','/addressadd/','/ordercreate/','/buy/','/mycenter/','/myorders/',]

		if u in urllist:

			# 验证是否登录

			if not request.session.get('VipUser',None):

				# 没有登录

				return HttpResponse('<script>alert("请先登录");location.href="/login/?next='+u+'"</script>')

		response = self.get_response(request)

		return response






