# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Frank'
__mtime__ = '2017/10/31'
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃             ┣┓
                ┃　          ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import Group,Permission
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.shortcuts import render_to_response,render,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from accounts.models import User,Loginlog
from Log.models import Log_dnspod_config
from dnspod.models import Dnspod_domains,Dnspod_records,Dnspod_cdnrecords,Dnspod_stat
from django.core.urlresolvers import reverse
import uuid
import logging
import time
from django.utils import timezone as datetime
logger = logging.getLogger('myproject')

def UserLogin(request):
    if request.session.get('username') is not None:
        return HttpResponseRedirect('/', {"user": request.user})
    else:
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                client_ip = request.META['HTTP_X_FORWARDED_FOR']
                client_ip = client_ip.split(',')[0]
                print client_ip
            except:
                try:
                    client_ip = request.META['REMOTE_ADDR']
                except:
                    client_ip = ""
            print client_ip
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                request.session['username'] = username
                status = 1
                Loginlog_obj = Loginlog.objects.create(user=username,status=status,login_from=client_ip)
                Loginlog_obj.save()

                return HttpResponseRedirect('/accounts/center/')
            else:
                if request.method == "POST":
                    emsg = u"认证失败"
                    status = 0
                    Loginlog_obj = Loginlog.objects.create(user=username, status=status,login_from=client_ip)
                    Loginlog_obj.save()
                    print "+++++++++++++"
                    print emsg
                    return render(request,'dashboard/login.html',locals())
                else:
                    return render(request, 'dashboard/login.html', locals())
        except Exception,e:
            print e
        return render(request, 'dashboard/login.html', locals())


def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')

@login_required
def center(request):
    asset_count = []
    asset_type = [0, 1, 2, 3]
    op = ["新增","修改","删除","切换"]
    dict = {"新增":0,"修改":1,"删除":2,"切换":3}
    #now_time = datetime.datetime.now()
    #yes_time = now_time + datetime.timedelta(days=-1)
    #print yes_time
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    HH=" 00:00:00"
    today = today+HH
    try:
        stat_obj = Dnspod_stat.objects.filter(date_time__gte=today)
        assets = Log_dnspod_config.objects.all()
        domaincount = Dnspod_domains.objects.count()
        users = User.objects.count()
        usergroupcount = Group.objects.count()
        records = Dnspod_records.objects.count()
        user_top_five =Loginlog.objects.all().order_by('-login_time')[:5]
        lst = []
        for k,v in dict.items():
            opdata = {}
            count = Log_dnspod_config.objects.filter(op_type=v).count()
            opdata["value"] = count
            opdata["name"] = k
            lst.append(opdata)
        optype_json = json.dumps(op)
        opdata_json = json.dumps(lst)
        dlst = []
        dcount = []
        for line in stat_obj:
            dlst.append(str(line.domain))
            dcount.append(str(line.record_count))

    except Exception,e:
        print e

    return render(request, 'dashboard/index.html', locals())


@login_required
def UserProfile(request):
    user_selected_obj = User.objects.get(username=request.user)
    if request.method == "POST":
        user_name = request.POST.get("user_name", '')
        reset_password = request.POST.get("reset_password", '')
        if user_name:
            User.objects.filter(username=request.user).update(username=user_name)

        if reset_password:
            user_selected_obj.set_password(reset_password)
            user_selected_obj.save()
            return redirect("/accounts/login/")
    return render(request, 'confuser/user_profile.html', locals())


@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def UserList(request):
    user_obj = User.objects.exclude(username=request.user)
    return render(request, 'confuser/user_list.html', locals())

@login_required
@permission_required('accounts.can_change_user',login_url='/noperm/')
def ChangePwd(request):
    """给用户重置密码"""
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
        user_selected_obj = User.objects.get(id=user_id)
        user_status = user_selected_obj.is_active

    elif request.method == "POST":
        try:
            user_name = request.POST.get('user_name', '')
            reset_password = request.POST.get('reset_password', '')
            is_active = '0' if 'true' in request.POST.get('is_active', '') else '1'
            full_path = request.POST.get("full_path", '')
            user_id = full_path.split('=', 1)[-1]
            user_selected_obj = User.objects.get(id=user_id)
            user_filter_obj = User.objects.filter(id=user_id)
            user_filter_obj.update(username=user_name, is_active=is_active)
            if reset_password:
                user_selected_obj.set_password(reset_password)
                user_selected_obj.save()

            submit_status = json.dumps(0)
        except Exception, e:
            print e
            submit_status = json.dumps(-1)

        return HttpResponse(submit_status)

    return render(request, 'confuser/user_resetpwd.html', locals())

@login_required
@permission_required('accounts.can_change_user',login_url='/noperm/')
def UserEdit(request):
    user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通用户'}
    group_all = Group.objects.all()
    active = {"on":1,"off":0}
    if request.method == 'GET':
        user_id = request.GET.get('user_id', '')
        user_id = int(user_id)
        user_selected_obj = User.objects.get(id=user_id)
        groups_str = ' '.join([str(group.id) for group in user_selected_obj.groups.all()])
        user_status = user_selected_obj.is_active
        sql = '''select a.id,a.name,b.user_id,b.group_id from auth_group a,accounts_user_groups b where b.user_id=%s and a.id=b.group_id;''' % user_id
        group_selected = User.objects.raw(sql)

    elif request.method == "POST":
        try:
            user_name = request.POST.get('username', '')
            name = request.POST.get('name', '')
            reset_password = request.POST.get('password1', '')
            email = request.POST.get('email','')
            is_active = 0 if "true" in request.POST.get('is_active', '') else 1
            groups = request.POST.getlist("groups[]", [])
            User.objects.filter(username=user_name).update(is_active=is_active,name=name,email=email)
            user_selected_obj = User.objects.get(username=user_name)
            for group in groups:
                try:
                    user_selected_obj.groups.add(group)
                except Exception,e:
                    print e
            user_selected_obj.save()
            if reset_password:
                user_selected_obj.set_password(reset_password)
                user_selected_obj.save()

            submit_status = json.dumps(0)
        except Exception, e:
            print e
            submit_status = json.dumps(-1)

        return HttpResponse(submit_status)

    return render(request, 'confuser/user_edit.html', locals())

@login_required
@permission_required('accounts.can_del_user',login_url='/noperm/')
def UserDel(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            user_selected_obj = User.objects.get(id=user_id)
            # 清空用户具有权限的配置。
            user_selected_obj.delete()
            del_status = json.dumps(0)

        except Exception, e:
            del_status = json.dumps(-1)

        return HttpResponse(del_status)

@login_required
@permission_required('accounts.can_add_user',login_url='/noperm/')
def UserAdd(request):
    user_role = {'SU': u'超级管理员', 'GA': u'部门管理员', 'CU': u'普通用户'}
    group_all = Group.objects.all()
    active = {"on":1,"off":0}
    if request.method == 'POST':
        try:
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            name = request.POST.get('name', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            groups = request.POST.getlist('groups[]',[])
            role = request.POST.get('role', '')
            is_active = request.POST.get('is_active','')
            admin_groups = request.POST.get('admin_groups', '')
            user_uuid = uuid.uuid4().get_hex()
            userobj = User.objects.create(email=email, username=username,name=name,role=role,is_active=active[is_active])
            userobj.set_password(password1)
            userobj.groups.set(groups)
            userobj.save()
            create_status = json.dumps(0)

        except Exception, e:
            print e
            create_status = json.dumps(-1)

        return HttpResponse(create_status)

    return render(request, 'confuser/user_add-1.html', locals())
#    return render(request, 'confuser/user_add.html', locals())


@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def DeptList(request):
    try:
        dept_obj = Group.objects.all()
    except Exception,e:
        print e
    return render(request, 'confuser/dept_list.html', locals())

@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def DeptAdd(request):
    """新增组"""
    if request.method == 'POST':
        try:
            dept_name = request.POST.get('name', '')
            description = request.POST.get('description','')
            dept_obj = DepartmentGroup(dept_name=dept_name, description=description)
            dept_obj.save()
            create_status = json.dumps(0)
        except Exception, e:
            print e
            create_status = json.dumps(-1)
        return HttpResponse(create_status)
    return render(request, 'confuser/dept_add.html', locals())

@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def DeptDel(request):
    """删除组"""
    if request.method == "POST":
        try:
            dept_id = request.POST.get("dept_id",'')
            user_group = get_object_or_404(Group, id=dept_id)
            user_group.user_set.clear()
            Group.objects.filter(id=dept_id).delete()
            del_status = json.dumps(0)
        except Exception,e:
            print e
            del_status = json.dumps(-1)
        return HttpResponse(del_status)

@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def DeptEdit(request):
    """用户组编辑"""
    error = ''
    msg = ''
    if request.method == 'GET':
        gid = request.GET.get('gid', '')
        #users_remain = User.objects.all()
        user_group = Group.objects.filter(id=gid)
        user_group = user_group[0]
        users_selected = User.objects.filter(groups=user_group)
        users_remain = User.objects.filter(~Q(groups=user_group))
        users_all = User.objects.all()
    elif request.method == 'POST':
        group_id = request.POST.get('group_id', '')
        group_name = request.POST.get('group_name', '')
        comment = request.POST.get('comment', '')
        users_selected = request.POST.getlist('users_selected')
        user_group = get_object_or_404(Group, id=group_id)
        user_group.user_set.clear()
        for user in User.objects.filter(id__in=users_selected):
            user.groups.add(Group.objects.get(id=group_id))
        user_group.name = group_name
        user_group.save()
        return redirect('/accounts/deptlist/')
    return render(request, 'confuser/dept_edit.html', locals())


@login_required
@permission_required('accounts.can_read_user',login_url='/noperm/')
def DeptAdd(request):
    """
    添加用户组
    """
    if request.method == 'POST':
        try:
            dept_name = request.POST.get('name', '')
            dept_obj = Group(name=dept_name)
            dept_obj.save()
            create_status = json.dumps(0)
        except Exception, e:
            print e
            create_status = json.dumps(-1)
        return HttpResponse(create_status)
    return render(request, 'confuser/dept_add.html', locals())

def Noperm(request):
    return render(request,'403.html',locals())


def Perm_set(request,gid):
    """设置组权限"""
    if request.method == "GET":
        print request.GET
        try:
            group = Group.objects.get(id=gid)
        except Exception,e:
            print e
            msg = "该用户组不存在"
            return render(request,'confuser/dept_permset.html',locals())
        permList = Permission.objects.filter(codename__startswith="can_")
        groupPerm = [p.get('id') for p in group.permissions.values()]
        try:
            for ds in permList:
                if ds.id in groupPerm:
                    ds.status = 1
                else:
                    ds.status = 0
            return render(request,'confuser/dept_permset.html',locals())
        except Exception,e:
            print e
            msg = e
            return render(request,'confuser/dept_permset.html',locals())
    elif request.method == "POST":
        try:
            group = Group.objects.get(id=gid)
            Group.objects.filter(id=gid).update(
                                            name = request.POST.get('name')
                                            )
            #如果权限key不存在就单做清除权限
            if request.POST.getlist('perms') is None:
                group.permissions.clear()
            else:
                userPermList = []
                for perm in group.permissions.values():
                    userPermList.append(perm.get('id'))
                permList = [ int(i) for i in request.POST.getlist('perms')]
                addPermList = list(set(permList).difference(set(userPermList)))
                delPermList = list(set(userPermList).difference(set(permList)))
                #添加新增的权限
                for permId in addPermList:
                    perm = Permission.objects.get(id=permId)
                    Group.objects.get(id=gid).permissions.add(perm)
                #删除去掉的权限
                for permId in delPermList:
                    perm = Permission.objects.get(id=permId)
                    Group.objects.get(id=gid).permissions.remove(perm)
            return HttpResponseRedirect('/accounts/group/{gid}/'.format(gid=gid))
        except Exception,e:
            print e
            return render(request,'confuser/dept_permset.html',locals())


def page_not_found(request):
    return render(request,'404.html',locals())

def page_error(request):
    return render(request,'500.html',locals())




