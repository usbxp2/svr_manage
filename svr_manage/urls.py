from django.conf.urls import url, include
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls')),
    url(r'^accounts/login/$', views.acc_login),
    url(r'^accounts/logout/$', views.acc_logout),
    url(r'^$', views.acc_login, name='acc_logout'),
]
