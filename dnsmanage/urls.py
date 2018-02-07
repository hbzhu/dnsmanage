"""dnsmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from accounts import views as AccoutView
from dnspod import views as DnspodView
from django.views.generic.base import RedirectView

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^$', AccoutView.center, name='UserCenter'),
    url(r'^accounts/login/', AccoutView.UserLogin, name='UserLogin'),
    url(r'^accounts/logout/', AccoutView.Logout, name='Logout'),
    url(r'^accounts/center/', AccoutView.center, name='UserCenter'),
    url(r'^accounts/list/', AccoutView.UserList, name='UserList'),
    url(r'^accounts/profile/', AccoutView.UserProfile, name='UserProfile'),
    url(r'^accounts/changepwd/', AccoutView.ChangePwd, name='ChangePwd'),
    url(r'^accounts/detailedit/', AccoutView.UserEdit, name='UserEdit'),
    url(r'^accounts/del/', AccoutView.UserDel, name='UserDel'),
    url(r'^accounts/add/', AccoutView.UserAdd, name='UseraAdd'),
    url(r'^accounts/deptlist/', AccoutView.DeptList, name='DeptList'),
    url(r'^accounts/deptadd/', AccoutView.DeptAdd, name='DeptAdd'),
    url(r'^accounts/deptdel/', AccoutView.DeptDel, name='DeptDel'),
    url(r'^accounts/deptedit/', AccoutView.DeptEdit, name='DeptEdit'),
    url(r'^accounts/group/(?P<gid>[0-9]+)/$',AccoutView.Perm_set,name='Perm_set'),
    url(r'^noperm/',AccoutView.Noperm,name="Noperm"),

    url(r'^dnspod/dnsrecord/', DnspodView.DnsRecord, name='DnsRecord'),
    url(r'^dnspod/domlist/', DnspodView.DomLst, name='DomLst'),
    url(r'^dnspod/recordedit/', DnspodView.DnsRecordEdit, name='DnsRecordEdit'),
    url(r'^dnspod/recordadd/', DnspodView.DnsRecordAdd, name='DnsRecordAdd'),
    url(r'^dnspod/recorddel/', DnspodView.DnsRecordDel, name='DnsRecordDel'),
    url(r'^dnspod/ldnsrecord/', DnspodView.LdnsRecord, name='LdnsRecord'),
    url(r'^dnspod/dnsrecordswitch/$', DnspodView.DnsRecordSwitch, name='DnsRecordSwitch'),
    url(r'^dnspod/dnsrecordsync/$', DnspodView.DnsRecordSync, name='DnsRecordSync'),
    url(r'^dnspod/cdnsync/$', DnspodView.CdnSync, name='CdnSync'),
    url(r'^dnspod/cdnrecord/$', DnspodView.CdnRcord, name='CdnRcord'),
    url(r'^dnspod/cdndetail/$', DnspodView.CDNDetail,name='CDNDetail'),

    url(r'^dnspod/oplog/', DnspodView.Dnsoplog, name='Dnsoplog'),
]
