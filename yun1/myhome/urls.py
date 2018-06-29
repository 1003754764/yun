"""wang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
# from django.contrib import admin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^$',views.index,name="myhome_index"),
    # 列表
    url(r'^list/(?P<tid>[0-9]+)/$',views.list,name="myhome_list"),
    # 详情
    url(r'^info/(?P<sid>[0-9]+)/$',views.info,name="myhome_info"),
    # 登录
    url(r'^login/$',views.login,name="myhome_login"),
    # 退出登录
    url(r'^logout/$',views.logout,name="myhome_logout"),
    # 注册
    url(r'^register/$',views.register,name="myhome_register"),
    # 搜索
    url(r'^search/$',views.search,name="myhome_search"),
    # 验证码
    url(r'^vcode$',views.vcode,name="myhome_vcode"),

    #加入购物车

    url(r'^addcart/$',views.addcart,name="myhome_addcart"),

    # 购物车列表

    url(r'^cartlist/$',views.cartlist,name="myhome_cartlist"),

    # 删除购物车的一个商品

    url(r'^delcart/$',views.delcart,name="myhome_delcart"),

    # 修改购物车商品数量

    url(r'^updatecart/$',views.updatecart,name="myhome_updatecart"),

    # 清空购物车
    
    url(r'^cartclear/$',views.cartclear,name="myhome_cartclear"),

    # 订单确认
    url(r'^ordercheck/$',views.ordercheck,name="myhome_ordercheck"),

    # 收货地址修改
    url(r'^addressedit/$',views.addressedit,name="myhome_addressedit"),

    # 收货地址增加
    url(r'^addressadd/$',views.addressadd,name="myhome_addressadd"),

    # 生成订单
    url(r'^ordercreate/$',views.ordercreate,name="myhome_ordercreate"),

    # 进行支付
    url(r'^buy/$',views.buy,name="myhome_buy"),

    # 个人中心
    url(r'^mycenter/$',views.mycenter,name="myhome_mycenter"),

    # 我的订单
    url(r'^myorders/$',views.myorders,name="myhome_myorders"),



]
