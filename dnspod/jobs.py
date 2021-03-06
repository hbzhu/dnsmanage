# -*- coding: utf-8 -*-
"""
__author__ = 'Frank'
__mtime__ = '2018/1/18'
"""
import dnspod_api,qcloud_api,upyun_api
from models import Dnspod_domains,Dnspod_records,Dnspod_cdnrecords,Dnspod_stat
import time
import MysqlHandle

def CdnSync():
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    qcdn = qcloud_api.Cdn()
    ucdn = upyun_api.UpyunCDN()
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

    except Exception,e:
        print e

def dnspodSync():
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dnsp =  dnspod_api.Dnspod()
    try:
        domlst = dnsp.get_domainlist()
        Dnspod_records.objects.filter().delete()
        Dnspod_domains.objects.filter().delete()
        new_domlst = []
        for dlst in domlst:
            new_domlst.append(Dnspod_domains(domain_id=dlst["id"],domain=dlst["name"]))
        Dnspod_domains.objects.bulk_create(new_domlst)
        for v in domlst:
            print v
            domain_id = v["id"]
            record = dnsp.Get_Record(domain_id)
            record_lst = []
            for line in record:
                record_lst.append(Dnspod_records(record_id=line["id"], record=line["name"], record_type=line["type"],domain_id_id=domain_id,record_value=line["value"],record_line=line["line"]))
            Dnspod_records.objects.bulk_create(record_lst)
        sql = """insert into dnsmanagev2.dnspod_stat (domain,record_count)  select b.domain ,count(a.domain_id_id) as record_count from dnsmanagev2.dnspod_records a join  dnsmanagev2.dnspod_domains b  on a.domain_id_id=b.domain_id  group by a.domain_id_id;"""
        db = MysqlHandle.database()
        db.update(sql)
        db.close()


    except Exception,e:
        print e



#if  __name__ == '__main__':
#    CdnSync()