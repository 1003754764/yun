from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=77)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1,null=True)
    pic = models.CharField(max_length=100,null=True)
    # 0 正常会员  1禁用会员 
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)



class Types(models.Model):

    name = models.CharField(max_length=20)

    pid = models.IntegerField()

    path = models.CharField(max_length=50)