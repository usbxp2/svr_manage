from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^login/$', views.acc_login, name='acc_login'),
    url(r'projects/$', views.projects, name='projects'),
    url(r'customers/$', views.customers, name='customers'),
    url(r'hosts/$', views.hosts, name='hosts'),
    url(r'clouds/$', views.clouds, name='clouds'),
    url(r'customers/(\d+)/$', views.customers_detail, name='customers_detail'),
    url(r'clouds/(\d+)/$', views.clouds_detail, name='clouds_detail'),
    url(r'hosts/(\d+)/$', views.hosts_detail, name='hosts_detail'),
    url(r'projects/(\d+)/$', views.projects_detail, name='projects_detail'),
    url(r'update_password/(\d+)/$', views.update_password, name='update_password'),
    url(r'add_project/$', views.add_project, name='add_project'),
    url(r'add_customer/$', views.add_customer, name='add_customer'),
    url(r'add_host/$', views.add_host, name='add_host'),
    url(r'add_cloud/$', views.add_cloud, name='add_cloud'),
    url(r'month/$', views.month_exp, name='month'),
]
