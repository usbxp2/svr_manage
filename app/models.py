from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserJwcx(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=64, verbose_name='姓名')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

class ServerGroup(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='组名')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '主机组管理'
        verbose_name_plural = verbose_name

class Cloud(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='公司名称')
    web_site = models.URLField(verbose_name='官网')
    link_man = models.CharField(max_length=64, verbose_name='联系人姓名')
    phone = models.BigIntegerField(verbose_name='联系电话')
    qq = models.IntegerField(verbose_name='QQ号码')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '云服务商管理'
        verbose_name_plural = verbose_name

class Customers(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='公司名称')
    link_man = models.CharField(max_length=64, verbose_name='联系人姓名')
    phone = models.BigIntegerField(verbose_name='联系电话')
    email = models.EmailField(verbose_name='电子邮箱')
    address = models.CharField(max_length=200, blank=True, null=True, default='', verbose_name='公司地址')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户管理'
        verbose_name_plural = verbose_name

class Hosts(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='主机名')
    source_from = models.ForeignKey(Cloud, verbose_name='云服务商')
    ip = models.GenericIPAddressField(verbose_name="公网IP")
    private_ip = models.GenericIPAddressField(verbose_name="内网IP", default='')
    hardware = models.TextField(max_length=200, verbose_name='硬件配置', help_text="cpu: 内存：硬盘：")
    bandwidth = models.IntegerField(verbose_name='带宽', help_text='填写带宽，不需要加MB')
    os_choices = ((1, 'windows server 2003'),
                  (2, 'windows server 2008'),
                  (3, 'windows server 2012'),
                  (4, 'centos 6.5'),
                  (5, 'ubuntu'),
                 )
    os_system = models.IntegerField(choices=os_choices, verbose_name='操作系统')
    host_group = models.ManyToManyField(ServerGroup)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '主机管理'
        verbose_name_plural = verbose_name

class Projects(models.Model):
    com_name = models.ForeignKey(Customers, verbose_name='公司名称')
    name = models.CharField(max_length=128, verbose_name='项目名称')
    on_server = models.ManyToManyField(Hosts, verbose_name='服务器')
    code_path = models.CharField(max_length=64, verbose_name='代码目录',
                                 help_text='example: windows类似 D:\web\project; linux下类似 /var/www/project')
    domain = models.CharField(max_length=200, verbose_name='域名', help_text='example: www.qq.com')
    status_choices = (('online', '运维中'),
                      ('offline', '测试中'),
                      ('nothing', '已存档'),
                      )
    archive_dir = models.CharField(max_length=64, verbose_name='归档目录', help_text='百度云 archive/2015/wwse', default='',blank=True, null=True)
    status = models.CharField(choices=status_choices, verbose_name='项目状态', max_length=64)
    db_addr = models.CharField(max_length=200, verbose_name='数据库地址', blank=True, null=True)
    db_name = models.CharField(max_length=64, verbose_name='数据库名称', blank=True, null=True)
    db_user = models.CharField(max_length=64, verbose_name='数据库用户', blank=True, null=True)
    db_password = models.CharField(max_length=64, verbose_name='数据库密码',blank=True, null=True, default='')
    jenkins = models.CharField(max_length=64, default='', blank=True, null=True)
    db_choices = (('mysql', 'MySQL'),('sqlserver', 'SQL Server'),)
    db_type = models.CharField(choices=db_choices, max_length=64)
    ssh = models.TextField(max_length=200, verbose_name='ssh', default='')
    exp_date = models.DateField(verbose_name='到期日期', default='2016-6-6', help_text='example: 2016-6-6')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = verbose_name
