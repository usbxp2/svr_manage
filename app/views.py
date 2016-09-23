from django.shortcuts import render,redirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app import models, forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required
import datetime, os


# Create your views here.

#检查用户权限
def check_permissions(request):
    user_perm = {}
    print('----->', request.user.is_superuser)
    if request.user.is_superuser is True:
        print('+++++', 'here')
        user_perm['add_customer_perm'] = 1
        user_perm['add_host_perm'] = 1
        user_perm['add_cloud_perm'] = 1
        user_perm['add_project_perm'] = 1
    else:
        if request.user.has_perm('app.add_projects'):
            user_perm['add_project_perm'] = 1
        else:
            add_project_perm = 0
        user_perm['add_customer_perm'] = 1 if request.user.has_perm('app.add_customers') else 0
        user_perm['add_host_perm'] = 1 if request.user.has_perm('app.add_hosts') else 0
        user_perm['add_cloud_perm'] = 1 if request.user.has_perm('app.add_cloud') else 0

    return user_perm


#全局
def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_TITLE = settings.SITE_TITLE
    user_perm = check_permissions(request)
    return locals()

def jw_logger(username, msg):
    file_name = '%s.txt' % datetime.datetime.now().date()
    file_path = os.path.join(os.path.join(settings.BASE_DIR, 'logs'), file_name)
    f = open(file_path, 'a')
    msg = '%s__%s__%s\n' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username, msg)
    f.write(msg)
    f.close()

def acc_login(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            #验证通过，登录
            login(request, user)
            msg = 'info__登录成功'
            jw_logger(username, msg)
            #登录后返回首页
            return redirect(projects)
        else:
            #认证不成功
            login_err = 'wrong username or password!'
            msg = 'error__登录失败:%s' % login_err
            jw_logger(username, msg)
            return render(request, 'app/login.html', locals())

def page_f(request, obj, num):
    paginator = Paginator(obj, num)
    page = request.GET.get('page')
    try:
        obj_list = paginator.page(page)
    except PageNotAnInteger:
        obj_list = paginator.page(1)
    except EmptyPage:
        obj_list = paginator.page(paginator._num_pages)
    return obj_list

@login_required
def projects(request):
    projects_obj = models.Projects.objects.all()
    paginator = Paginator(projects_obj, 10)
    page = request.GET.get('page')
    flag = 1
    try:
        projects_list = paginator.page(page)
    except PageNotAnInteger:
        projects_list = paginator.page(1)
    except EmptyPage:
        projects_list = paginator.page(paginator.num_pages)
    return render(request, 'app/projects.html',locals())

@login_required
def customers(request):
    customers_obj = models.Customers.objects.all()
    customers_list = page_f(request, customers_obj, 10)
    flag = 2

    return render(request, 'app/customers.html', locals())

@login_required
def hosts(request):
    hosts_obj = models.Hosts.objects.all()
    hosts_list = page_f(request, hosts_obj, 10)
    flag = 3
    return render(request, 'app/hosts.html', locals())

@login_required
def clouds(request):
    clouds_obj = models.Cloud.objects.all()
    clouds_list = page_f(request, clouds_obj, 10)
    flag = 4
    return render(request, 'app/clouds.html', locals())


def table_detail(request, table_obj, form_name, template_name, name_flag, p_flag):
    template_name = 'app/%s' % template_name
    if request.method == "GET":
        table_form = form_name(instance=table_obj)
        return render(request, template_name, locals())
    else:
        table_form = form_name(request.POST, instance=table_obj)
        if table_form.is_valid():
            if p_flag:
                table_form.save()
                if name_flag == '项目':
                    msg = 'info__修改%s成功,%s,%s' % (name_flag, models.Customers.objects.get(id=request.POST.get('com_name')).name, request.POST.get('name'))
                if name_flag == '客户':
                    msg = 'info__修改%s成功,%s,%s' % (name_flag, request.POST.get('name'), request.POST.get('name'))
                jw_logger(request.user.userjwcx.name, msg)
                base_url = '/'.join(request.path.split('/')[:-2])
                return redirect(base_url)
            else:
                err_msg = 'Not has add permission!'
                if name_flag == '项目':
                    msg = 'info__修改%s成功,%s,%s' % (name_flag, models.Customers.objects.get(id=request.POST.get('com_name')).name, request.POST.get('name'))
                if name_flag == '客户':
                    msg = 'info__修改%s成功,%s,%s' % (name_flag, request.POST.get('name'), request.POST.get('name'))
                jw_logger(request.user.userjwcx.name, msg)
                return render(request, 'app/403.html', locals())
        else:
            return render(request, template_name, locals())

@login_required
def customers_detail(request, id):
    name_flag = '客户'
    customers_obj = models.Customers.objects.get(id=id)
    form = forms.CustomerModelForm
    template_name = 'customers_detail.html'
    p_flag = False
    if request.user.has_perm('app.change_customers'):
        p_flag = True
    return table_detail(request, customers_obj, form, template_name, name_flag, p_flag)

@login_required
def clouds_detail(request, id):
    name_flag = '云服务商'
    cloud_obj = models.Cloud.objects.get(id=id)
    form = forms.CloudModelForm
    template_name = 'customers_detail.html'
    p_flag = False
    if request.user.has_perm('app.change_cloud'):
        p_flag = True
    return table_detail(request, cloud_obj, form, template_name, name_flag, p_flag)

@login_required
def hosts_detail(request, id):
    name_flag = '服务器'
    host_obj = models.Hosts.objects.get(id=id)
    form = forms.HostModelForm
    template_name = 'customers_detail.html'
    p_flag = False
    if request.user.has_perm('app.change_hosts'):
        p_flag = True
    return table_detail(request, host_obj, form, template_name, name_flag, p_flag)

@login_required
def projects_detail(request, id):
    name_flag = '项目'
    project_obj = models.Projects.objects.get(id=id)
    form = forms.ProjectModelForm
    template_name = 'customers_detail.html'
    p_flag = False
    if request.user.has_perm('app.change_projects'):
        p_flag = True
    return table_detail(request, project_obj, form, template_name, name_flag, p_flag)

@login_required
def update_password(request, id):
    if request.method == 'POST':
        user_obj = models.User.objects.get(id=id)
        password1 = request.POST.get('password')
        password2 = request.POST.get('password1')
        print(password1, password2)
        if password1 == password2 and password1 != '':
            try:
                print('begin')
                user_obj.set_password(password1)
                user_obj.save()
                print('end')
                return redirect(projects)
            except Exception as e:
                errors = e
                print('------->', e)
        else:
            errors = '密码输入不正确!'
    return render(request, 'app/password_html.html', locals())

def acc_logout(request):
    logout(request)
    return redirect('/')

def add_table(request, form_name, template_name, name_flag, flag, p_flag):
    template_name = 'app/%s' % template_name
    if request.method == "GET":
        table_form = form_name()
        return render(request, template_name, locals())
    else:
        table_form = form_name(request.POST)
        if table_form.is_valid():
            if p_flag:
                table_form.save()

                if flag == 1:
                    msg = 'info__新建项目成功,%s,%s' % (models.Customers.objects.get(id=request.POST.get('com_name')).name, request.POST.get('name'))
                    jw_logger(request.user.userjwcx.name, msg)
                    return redirect(projects)
                if flag == 2:
                    msg = 'info__新建客户成功,%s,%s' % (request.POST.get('name'), request.POST.get('name'))
                    jw_logger(request.user.userjwcx.name, msg)
                    return redirect(customers)
                if flag == 3:
                    msg = 'info__新建主机成功,%s,%s' % (request.POST.get('name'), request.POST.get('name'))
                    jw_logger(request.user.userjwcx.name, msg)
                    return redirect(hosts)
                if flag == 4:
                    msg = 'info__新建云服务商成功,%s,%s' % (request.POST.get('name'), request.POST.get('name'))
                    jw_logger(request.user.userjwcx.name, msg)
                    return redirect(clouds)
            else:
                err_msg = 'Not has add permission!'
                if flag == 1:
                    p_name = '新建项目'
                    msg = 'error__新建%s失败,%s,%s,%s' % (p_name, models.Customers.objects.get(id=request.POST.get('com_name')).name, request.POST.get('name'), err_msg)
                if flag == 2:
                    p_name = '新建客户'
                    msg = 'error__新建%s失败,%s,%s,%s' % (p_name, request.POST.get('name'), request.POST.get('name'), err_msg)
                if flag == 3:
                    p_name = '新建主机'
                    msg = 'error__新建%s失败,%s,%s,%s' % (p_name, request.POST.get('name'), request.POST.get('name'), err_msg)
                if flag == 4:
                    p_name = '新建云服务商'
                    msg = 'error__新建%s失败,%s,%s,%s' % (p_name, request.POST.get('name'), request.POST.get('name'), err_msg)

                jw_logger(request.user.userjwcx.name, msg)
                return render(request, 'app/403.html', locals())
        else:
            return render(request, template_name, locals())

@login_required
def add_project(request):
    name_flag = '添加项目'
    flag = 1
    form_name = forms.ProjectModelForm
    template_name = 'customers_detail.html'
    p_flag = False
    if request.user.has_perm('app.add_projects'):
        p_flag = True
    return add_table(request, form_name, template_name, name_flag, flag, p_flag)

@login_required
def add_customer(request):
    name_flag = '添加客户'
    flag = 2
    p_flag = False
    if request.user.has_perm('app.add_customers'):
        p_flag = True
    form_name = forms.CustomerModelForm
    template_name = 'customers_detail.html'
    return add_table(request, form_name, template_name, name_flag, flag, p_flag)

def add_host(request):
    name_flag = '添加主机'
    flag = 3
    p_flag = False
    if request.user.has_perm('app.add_hosts'):
        p_flag = True
    form_name = forms.HostModelForm
    template_name = 'customers_detail.html'
    return add_table(request, form_name, template_name, name_flag, flag, p_flag)

def add_cloud(request):
    name_flag = '添加云服务商'
    flag = 4
    p_flag = False
    if request.user.has_perm('app.app_cloud'):
        p_flag = True
    form_name = forms.CloudModelForm
    template_name = 'customers_detail.html'
    return add_table(request, form_name, template_name, name_flag, flag, p_flag)

def month_exp(request):
    startdate = datetime.datetime.now().date()
    enddate = startdate + datetime.timedelta(30)
    projects_obj = models.Projects.objects.filter(exp_date__range = (startdate, enddate))
    projects_list = page_f(request, projects_obj, 10)
    return render(request, 'app/projects.html',locals())