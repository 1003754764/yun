# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('descr', models.CharField(max_length=255, null=True)),
                ('info', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pics', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0)),
                ('store', models.IntegerField(default=0)),
                ('num', models.IntegerField(default=0)),
                ('clicknum', models.IntegerField(default=0)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('pid', models.IntegerField()),
                ('path', models.CharField(max_length=50)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=77)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=11)),
                ('age', models.IntegerField(null=True)),
                ('sex', models.CharField(max_length=1, null=True)),
                ('pic', models.CharField(max_length=100, null=True)),
                ('status', models.IntegerField(default=0)),
                ('addtime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='typeid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.Types'),
        ),
    ]
