from django import template

from django.utils.html import format_html

register = template.Library()



@register.filter
def pricetwo(n):

	q = n*1.5

	return q

@register.simple_tag
def cheng(n1,n2):

	# print(type(n2))

	n3 = n1*n2

	return round(n3,2)

@register.simple_tag
def page(c,request):
	# c 总页数
	# p 当前页数
	p = int(request.GET.get('p',1))

	# print(c)
	# 开始页数
	start=p-4   
    # 结束页数   取10页数据
	e=p+5

	# 判断当前页数

	if p<5:

		start=1

		e=10
	# 结束页不能超出总页数
	if p > c-5:

		start = c-9

		e = c

	# 开始页数不能小于等于0
	if start <=0:

		start = 1

	
	u = ''
	for x in request.GET:
	    # 排除p参数
	    if x != 'p':
	        u+= '&'+x+'='+request.GET[x]




	s = ''
	s += '<li><a href="?p=1'+u+'">首页</a></li>'
	if p - 1 <= 0:
	    s += '<li class="am-disabled"><a href="?p=1'+u+'">上一页</a></li>'
	else:
	    s += '<li><a href="?p='+str(p-1)+u+'">上一页</a></li>'

	for x in range(start,e+1):
	    # 判断是否为当前页
	    if p == x:
	        s += '<li class="am-active"><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'
	    else:
	        s += '<li><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'


	if p+1 > c:
	    s += '<li class="am-disabled"><a href="?p='+str(c)+u+'">下一页</a></li>'
	else:
	    s += '<li><a href="?p='+str(p+1)+u+'">下一页</a></li>'

	s += '<li><a href="?p='+str(c)+u+'">尾页</a></li>'



	return format_html(s)


