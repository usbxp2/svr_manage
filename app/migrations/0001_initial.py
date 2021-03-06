# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-07 08:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cloud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='公司名称')),
                ('web_site', models.URLField(verbose_name='官网')),
                ('link_man', models.CharField(max_length=64, verbose_name='联系人姓名')),
                ('phone', models.BigIntegerField(verbose_name='联系电话')),
                ('qq', models.IntegerField(verbose_name='QQ号码')),
            ],
            options={
                'verbose_name': '云服务商管理',
                'verbose_name_plural': '云服务商管理',
            },
        ),
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='公司名称')),
                ('link_man', models.CharField(max_length=64, verbose_name='联系人姓名')),
                ('phone', models.BigIntegerField(verbose_name='联系电话')),
                ('email', models.EmailField(max_length=254, verbose_name='电子邮箱')),
                ('address', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='公司地址')),
            ],
            options={
                'verbose_name': '客户管理',
                'verbose_name_plural': '客户管理',
            },
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(verbose_name='IP地址')),
                ('hardware', models.TextField(help_text='cpu: 内存：硬盘：', max_length=200, verbose_name='硬件配置')),
                ('bandwidth', models.IntegerField(help_text='填写带宽，不需要加MB', verbose_name='带宽')),
                ('os_system', models.IntegerField(choices=[(1, 'windows server 2003'), (2, 'windows server 2008'), (3, 'windows server 2012'), (4, 'centos 6.5'), (5, 'ubuntu')], verbose_name='操作系统')),
            ],
            options={
                'verbose_name': '主机管理',
                'verbose_name_plural': '主机管理',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='项目名称')),
                ('code_path', models.CharField(help_text='example: windows类似 D:\\web\\project; linux下类似 /var/www/project', max_length=64, verbose_name='代码目录')),
                ('domain', models.CharField(help_text='example: www.qq.com', max_length=200, verbose_name='域名')),
                ('status', models.CharField(choices=[('online', '已上线'), ('offline', '测试中'), ('nothing', '未开始')], max_length=64, verbose_name='项目状态')),
                ('db_addr', models.CharField(max_length=200, verbose_name='数据库地址')),
                ('db_name', models.CharField(max_length=64, verbose_name='数据库名称')),
                ('db_password', models.CharField(max_length=64, verbose_name='数据库密码')),
                ('db_type', models.CharField(choices=[('mysql', 'MySQL'), ('sqlserver', 'SQL Server')], max_length=64)),
                ('ftp', models.TextField(max_length=200, verbose_name='FTP')),
                ('com_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customers', verbose_name='公司名称')),
                ('on_server', models.ManyToManyField(to='app.Hosts')),
            ],
            options={
                'verbose_name': '项目管理',
                'verbose_name_plural': '项目管理',
            },
        ),
        migrations.CreateModel(
            name='ServerGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='组名')),
            ],
            options={
                'verbose_name': '主机组管理',
                'verbose_name_plural': '主机组管理',
            },
        ),
        migrations.CreateModel(
            name='UserJwcx',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='姓名')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
            },
        ),
        migrations.AddField(
            model_name='hosts',
            name='host_group',
            field=models.ManyToManyField(to='app.ServerGroup'),
        ),
        migrations.AddField(
            model_name='hosts',
            name='source_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Cloud', verbose_name='云服务商'),
        ),
    ]
