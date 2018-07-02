from django.conf.urls import url
from . views import views,user,types,goods,order,authviews
urlpatterns = [
    # url(r'^admin/', admin.site.urls),

    # 后台首页
    url(r'^$',views.index,name="myadmin_index"),
    # 后台登录
    url(r'^login/$',views.login,name="myadmin_login"),

    # 后台权限管理

    # 后台用户添加
    url(r'^auth/user/add/$',authviews.useradd,name="auth_user_add"),

    # 后台用户列表
    url(r'^auth/user/list/$',authviews.userlist,name="auth_user_list"),



    # 会员管理
    url(r'^user/add/$',user.add,name="myadmin_user_add"),
    url(r'^user/list/$',user.list,name="myadmin_user_list"),
    url(r'^user/update/$',user.update,name="myadmin_user_update"),
    url(r'^user/delete/$',user.delete,name="myadmin_user_delete"),

    # 商品分类管理
	url(r'^types/add/$',types.add,name="myadmin_types_add"),
    url(r'^types/list/$',types.list,name="myadmin_types_list"),
    url(r'^types/update/$',types.update,name="myadmin_types_update"),
    url(r'^types/delete/$',types.delete,name="myadmin_types_delete"),

    # 商品管理

    url(r'^goods/add/$',goods.add,name="myadmin_goods_add"),
    url(r'^goods/list/$',goods.list,name="myadmin_goods_list"),
    url(r'^goods/update/$',goods.update,name="myadmin_goods_update"),
    url(r'^goods/delete/$',goods.delete,name="myadmin_goods_delete"),

    # 订单管理

    url(r'^order/list/$',order.list,name="myadmin_order_list"),
    url(r'^order/info/$',order.info,name="myadmin_order_info"),
    url(r'^order/status/$',order.status,name="myadmin_order_status"),

]
