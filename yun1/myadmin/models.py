from django.db import models

# Create your models here.
# 会员模型
class Users(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=77)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11,null=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1,null=True)
    pic = models.CharField(max_length=100,null=True)
    # 0 正常会员  1禁用会员 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:

        # 指定生成权限
        permissions = (

            ("show_users","查看会员管理"),
            ("insert_users","添加会员"),
            ("edit_users","修改会员"),
            ("del_users","删除会员"),

        )


# 商品分类模型
class Types(models.Model):

    name = models.CharField(max_length=20)

    pics = models.CharField(max_length=100,null=True)

    pid = models.IntegerField()

    path = models.CharField(max_length=50)

    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:

        # 指定生成权限
        permissions = (

            ("show_types","查看商品分类管理"),
            ("insert_types","添加商品分类"),
            ("edit_types","修改商品分类"),
            ("del_types","删除商品分类"),

        )
   

# 商品信息模型

class Goods(models.Model):
    # 一对多
    typeid =  models.ForeignKey(to="Types", to_field="id")
    # 商品名
    title = models.CharField(max_length=255)
    # 商品描述
    descr = models.CharField(max_length=255,null=True)
    # 商品详情
    info = models.TextField(null=True)
    # 商品价格
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # 商品图片
    pics = models.CharField(max_length=100)
    # 商品大图
    picbig = models.CharField(max_length=100,null=True)
    # 商品状态 0 新发布,1下架
    status = models.IntegerField(default=0)
    # 商品库存数量
    store = models.IntegerField(default=0)
    # 购买数量
    num = models.IntegerField(default=0)
    # 商品点击量
    clicknum = models.IntegerField(default=0)
    # 商品添加时间
    addtime = models.DateTimeField(auto_now_add=True)

    class Meta:

        # 指定生成权限
        permissions = (

            ("show_goods","查看商品管理"),
            ("insert_goods","添加商品"),
            ("edit_goods","修改商品"),
            ("del_goods","删除商品"),

        )

# 会员地址
class Address(models.Model):
    uid =  models.ForeignKey(to="Users", to_field="id")
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=20)
    xiangxi = models.CharField(max_length=50)
    status = models.IntegerField(default=0)


# 订单模型
class Orders(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id")
    addressid = models.ForeignKey(to="Address", to_field="id")
    totalprice = models.FloatField()
    totalnum = models.IntegerField()
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True,null=True)


    class Meta:

        # 指定生成权限
        permissions = (

            ("show_order","查看订单管理"),
            ("insert_order","添加订单"),
            ("edit_order","修改订单"),
            ("del_order","删除订单"),

        )

# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Orders", to_field="id")
    gid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()