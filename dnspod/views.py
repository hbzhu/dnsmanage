# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2017/12/14'
"""
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import dnspod_api,qcloud_api,upyun_api
from models import Dnspod_domains,Dnspod_records,Dnspod_cdnrecords
from Log.models import Log_dnspod_config
import json
from django.forms.models import model_to_dict
from django.db.models import Q
import logging

logger = logging.getLogger('myproject')


@login_required
def DnsRecord(request):
    """通过api获取，速度慢
    dnsp =  dnspod_api.Dnspod()
    if request.method == 'GET':
        domain_id = request.GET.get('domain_id','')
        try:
            domain = dnsp.get_domain(domain_id)
#        Record = dnsp.Get_Record(domain_id)
            Record = dnsp.getRecords(domain_id)
            keyword = request.GET.get('keyword','')
            if keyword:
                Record = []
                r = dnsp.record(domain,keyword)
                Record.append(r)
        except Exception,e:
            print e
        """
    if request.method == 'GET':
        domain_id = request.GET.get('domain_id', '')
        try:
            domain = Dnspod_domains.objects.filter(domain_id=domain_id)
            domain=domain[0].domain
            Record = Dnspod_records.objects.filter(domain_id_id=domain_id)[:1000]
            keyword = request.GET.get('keyword', '')
            if keyword:
                Record = Dnspod_records.objects.filter(Q(domain_id_id=domain_id),Q(record__contains=keyword)|Q(record_value__contains=keyword))
        except Exception,e:
            print e

    return render(request, 'dnspod/dns_record.html', locals())

@login_required
def DomLst(request):
    """
    dnsp = dnspod_api.Dnspod()
    domlst = dnsp.get_domainlist()
#将域名插入本地数据库
#    domstest = []
#    for line in domlst:
#        domstest.append(Dnspod_domains(domain=line["name"], domain_id=line["id"]))
#    print domstest
#    Dnspod_domains.objects.bulk_create(domstest)
    """
    try:
        domlst = Dnspod_domains.objects.all()
    except Exception,e:
        print e

    return render(request, 'dnspod/dom_list.html', locals())

@login_required
def DnsRecordEdit(request):
    dnsp = dnspod_api.Dnspod()
    if request.method == 'GET':
        record_name = request.GET.get('record_name')
        domain_id = request.GET.get('domain_id', '')
        record_type = request.GET.get('record_type')
        rs =  request.GET
        #return render(request, 'dnspod/record_edit.html', locals())
    elif request.method == "POST":
        try:
            record_name = request.POST.get('record_name', '')
            record_id = request.POST.get('record_id', '')
            record_type = request.POST.get('record_type', '')
            record_line = request.POST.get('record_line', '')
            record_value = request.POST.get('record_value', '')
            record_ttl = request.POST.get('record_ttl', '')
            domain_id = request.POST.get('domain_id', '')
            domain = dnsp.get_domain(domain_id)
            status = dnsp.record_update(domain_id,record_name,record_id,record_value,record_line,record_type)
            status = int(status["status"]["code"])
            if status != 1:
                submit_status = json.dumps(-1)
            else:
                submit_status = json.dumps(0)
                obj = Log_dnspod_config.objects.create(op_user=str(request.user), domain_name=domain,
                                                       domain_record=record_name, op_type=1,
                                                       op_content=str(record_type + ',' + record_value))
                obj.save()

        except Exception, e:
            print e
            submit_status = json.dumps(-1)

        return HttpResponse(submit_status)

    return render(request, 'dnspod/record_edit.html', locals())

@login_required
def DnsRecordAdd(request):
    dnsp = dnspod_api.Dnspod()
    if request.method == 'GET':
        domain_id = request.GET.get('domain_id', '')
        rs = request.GET
        domain = dnsp.get_domain(domain_id)
    elif request.method == "POST":
        try:
            domain_id = request.POST.get('domain_id', '')
            record_name = request.POST.get('record_name', '')
            record_type = request.POST.get('record_type', '')
            record_line = request.POST.get('record_line', '')
            record_value = request.POST.get('record_value', '')
            record_ttl = request.POST.get('record_ttl', '')
            domain = dnsp.get_domain(domain_id)
            status = dnsp.record_add(domain_id,record_name,record_type,record_value)
            print domain_id,record_name,record_type,record_value
            status = int(status["status"]["code"])

            if status != 1:
                submit_status = json.dumps(-1)
            else:
                submit_status = json.dumps(0)
                obj = Log_dnspod_config.objects.create(op_user=str(request.user),domain_name=domain,domain_record=record_name,op_type=0,op_content=str(record_type+','+record_value))
                obj.save()
        except Exception,e:
            print e
            submit_status = json.dumps(-1)

        return HttpResponse(submit_status)

    return render(request, 'dnspod/record_add.html', locals())

@login_required
def DnsRecordDel(request):
    dnsp = dnspod_api.Dnspod()
    if request.method == 'POST':
        try:
            record_id = request.POST.get('record_id','')
            domain_id = request.POST.get('domain_id','')
            domain = dnsp.get_domain(domain_id)
            record_name = request.POST.get('record_name', '')
            record_type = request.POST.get('record_type', '')
            record_value = request.POST.get('record_value', '')
            status = dnsp.Record_del(domain_id,record_id)
            status = int(status["status"]["code"])
            if status != 1:
                del_status = json.dumps(-1)
            else:
                del_status = json.dumps(0)
                obj = Log_dnspod_config.objects.create(op_user=str(request.user),domain_name=domain,domain_record=record_name,op_type=2,op_content=str(record_type+','+record_value))
                obj.save()
        except Exception,e:
            print e
            del_status = json.dumps(-1)

        return HttpResponse(del_status)




@login_required
def LdnsRecord(request):
    #record_obj = Dnspod_records.objects.order_by('?')[:500]
    if request.method == 'GET':
        try:
            record_obj = Dnspod_cdnrecords.objects.raw('select a.id,a.record_id,a.record,a.record_type,a.record_value,a.record_line,a.qcloud_record,a.upyun_record,a.source_record,a.domain_id_id,a.sync_time,a.update_time,a.client_ip,b.domain from dnspod_records a ,dnspod_domains b where a.domain_id_id=b.domain_id limit 1000;')
            keyword = request.GET.get('keyword', '')
            if keyword:
                sql ="""select a.id,a.record_id,a.record,a.record_type,a.record_value,a.record_line,a.qcloud_record,a.upyun_record,a.source_record,a.domain_id_id,a.sync_time,a.update_time,a.client_ip,b.domain from dnspod_records a ,dnspod_domains b where a.domain_id_id=b.domain_id and a.record='%s';""" % keyword
                record_obj = Dnspod_cdnrecords.objects.raw(sql)
        except Exception,e:
            print e
    return render(request,'dnspod/dns_lrecord.html',locals())

@login_required
def DnsRecordSwitch(request):
    dnsp = dnspod_api.Dnspod()
    if request.method == 'POST':
        try:
            record_id = request.POST.get('record_id','')
            domain_id = request.POST.get('domain_id','')
            #domain = dnsp.get_domain(domain_id)
            record_name = request.POST.get('record_name', '')
            #record_value = request.POST.get('record_value', '')
            record_type = request.POST.get('record_type','')
            record_line = request.POST.get('record_line','')
            domain = request.POST.get('domain','')
            full_domain = record_name+'.'+domain
            flag = request.POST.get('flag','')
            sql = """select * from dnspod_cdnrecords where full_domain='%s';""" % full_domain
            obj = Dnspod_cdnrecords.objects.raw(sql)
            if flag == 'qcloud':
                record_value = obj[0].qcloud_record
            if flag == 'upyun':
                record_value = obj[0].upyun_record
            if flag == 'origin':
                record_value = obj[0].source_record
                if ';' in record_value:
                    record_value = record_value.split(';')[0]

            if len(record_value) > 5:
                status = dnsp.record_update(domain_id, record_name, record_id, record_value, record_line, record_type)
                status = int(status["status"]["code"])
                print domain_id, record_name, record_id, record_value, record_line, record_type,full_domain
            else:
                sw_status = json.dumps(-1)
            if status != 1:
                sw_status = json.dumps(-1)
            else:
                Dnspod_records.objects.filter(domain_id_id=domain_id).filter(record_id=record_id).update(record_value=record_value,record_type=record_type)
                obj = Log_dnspod_config.objects.create(op_user=str(request.user), domain_name=domain,
                                                       domain_record=record_name, op_type=3,
                                                       op_content=str(record_type + ',' + record_value))
                obj.save()
                sw_status = json.dumps(0)

        except Exception,e:
            print e
            sw_status = json.dumps(-1)

        return HttpResponse(sw_status)


@login_required
def DnsRecordSync(request):
    dnsp =  dnspod_api.Dnspod()
    domlst = dnsp.get_domainlist()
    if request.method == 'POST':
        try:
            domain_id = request.POST.get('domain_id','')
            Dnspod_records.objects.filter(domain_id=domain_id).delete()
            record = dnsp.getRecords(domain_id)
            record_lst = []
            for line in record:
                record_lst.append(Dnspod_records(record_id=line["id"], record=line["name"], record_type=line["type"],domain_id_id=domain_id,record_value=line["value"]))
            Dnspod_records.objects.bulk_create(record_lst)
            status = json.dumps(0)
        except Exception,e:
            print e
            status = json.dumps(-1)
        return HttpResponse(status)



@login_required
def CdnSync(request):
    qcdn = qcloud_api.Cdn()
    ucdn = upyun_api.UpyunCDN()
    if request.method == 'POST':
        try:
            cdnlst = qcdn.DescribeCdnHosts()
            lst = []
            Dnspod_cdnrecords.objects.all().delete()
            for line in cdnlst:
                lst.append(Dnspod_cdnrecords(full_domain=line["host"],qcloud_record=line["cname"],source_record=line["origin"]))
            Dnspod_cdnrecords.objects.bulk_create(lst)
            upyun = ucdn.get_upyuncdn()
            for line in upyun:
                Dnspod_cdnrecords.objects.filter(full_domain=line["domain"]).update(upyun_record=line["cname_domain"])
            status = json.dumps(0)
        except Exception,e:
            print e
            status = json.dumps(-1)

        return HttpResponse(status)

@login_required
def CdnRcord(request):
    if request.method == 'GET':
        try:
            record_obj = Dnspod_cdnrecords.objects.all()
            keyword = request.GET.get('keyword', '')
            keyword = keyword.strip()
            if keyword:
                record_obj = Dnspod_cdnrecords.objects.filter(Q(full_domain__contains=keyword)|Q(qcloud_record__contains=keyword)|Q(upyun_record__contains=keyword)|Q(source_record__contains=keyword))
        except Exception,e:
            print e
    return render(request,'dnspod/cdn_record.html',locals())


@login_required
def Dnsoplog(request):
    obj = Log_dnspod_config.objects.all().order_by("create_time")

    return render(request,'dnspod/dns_oplog.html',locals())









