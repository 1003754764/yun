from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=77)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1,null=True)
    pic = models.CharField(max_length=100,null=True)
    # 0 正常会员  1禁用会员 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


# 商品分类模型
class Types(models.Model):

    name = models.CharField(max_length=20)

    pics = models.CharField(max_length=100,null=True)

    pid = models.IntegerField()

    path = models.CharField(max_length=50)

    addtime = models.DateTimeField(auto_now_add=True)
    

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