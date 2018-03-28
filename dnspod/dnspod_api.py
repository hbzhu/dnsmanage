#!/usr/bin/env python
#coding:utf-8
#dnspod api
import sys
import os
import json
import time
import requests
import logging
from logging.handlers import RotatingFileHandler
from dnsmanage import settings






class Dnspod:
    def __init__(self):
        self.LOGIN_TOKEN = settings.dnspod_login_token
        self.FORMAT = "json"



    def domain_info(self,domain):
        url = "https://dnsapi.cn/Domain.Info"
        data = {
            "login_token": self.LOGIN_TOKEN,
            "format": self.FORMAT,
            "domain": domain
            }
        try:
          r = requests.post(url, data=data, timeout=5)
          return r.json()["domain"]
        except Exception as e:
          return e

    def get_domain(self,domain_id):
        url = "https://dnsapi.cn/Domain.Info"
        data = {
            "login_token": self.LOGIN_TOKEN,
            "format": self.FORMAT,
            "domain_id": domain_id
            }
        try:
          r = requests.post(url, data=data, timeout=5)
          return r.json()["domain"]["name"]
        except Exception as e:
          return e


    def domain_id(self,domain):
        info = domain_info(domain)
        return info["id"]

    def record_info(self,domain,sub_domain):
        url = "https://dnsapi.cn/Record.List"
        data = {
            "login_token": self.LOGIN_TOKEN,
            "format": self.FORMAT,
            "domain": domain,
            "sub_domain": sub_domain
        }
        try:
            r = requests.post(url, data=data, timeout=5)
            return r.json()["records"][0]
#          result = r.json()
#          return result
#          result =  r.json()["records"]
#          domain_record = {}
#          for line in result:
#              full_domain = line["name"] +'.'+domain
#              domain_record[full_domain] = line["value"]
         #return domain_record



        except Exception as e:
          return e

    def record(self,domain, sub_domain):
        info = self.record_info(domain,sub_domain)
        return info

    def record_line(self,domain, sub_domain):
        info = self.record_info(domain, sub_domain)
        return info["line"]

    def record_value(self,domain, sub_domain):
        info = self.record_info(domain, sub_domain)
        return info["value"]

    def record_data(self,domain, sub_domain):
        info = self.record_info(domain)
        return info["id"], info["line"], info["value"],info["type"]


    def record_add(self,domain_id,record_name,record_type,record_value,record_line):
        url = "https://dnsapi.cn/Record.Create"
        data = {
            "login_token": self.LOGIN_TOKEN,
            "format": self.FORMAT,
            "domain_id": domain_id,
            "sub_domain": record_name,
            "record_type": record_type,
            "record_line": record_line,
            "value": record_value

        }
        try:
            r = requests.post(url, data=data, timeout=5)
        except Exception,e:
            print e
        return r.json()


    def record_update(self,domain_id, record_name,record_id,record_value,record_line,record_type,record_status="enable"):
        url = "https://dnsapi.cn/Record.Modify"
        data = {
            "login_token": self.LOGIN_TOKEN,
            "format": self.FORMAT,
            "domain_id": domain_id,
            "record_id": record_id,
            "sub_domain": record_name,
            "record_line": record_line,
            "value": record_value,
            "record_type": record_type,
            "status": record_status
        }
        try:
            r = requests.post(url, data=data, timeout=10)
        except Exception,e:
            print e
        return r.json()

    def get_domainlist(self):
        url = 'https://dnsapi.cn/Domain.List'
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT
                }
        try:
          r = requests.post(url, data=data, timeout=10)
          result = r.json()
          #print result
        except Exception as e:
          return e
        doms = []
        if "domains" in result:
            for domain in result["domains"]:
                dominfo = {}
                dominfo["name"] = domain["name"]
                dominfo["id"] = domain["id"]
                doms.append(dominfo)

        return doms

    def getDomainList(self):
        domians = []
        url = 'https://dnsapi.cn/Domain.List'
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT
                }
        r = requests.post(url, data=data, timeout=10)
        result = r.json()
        if "domains" in result:
            for domian in result["domains"]:
                domians.append(domian)
                line = "%s:%s record:%s" % (domian["id"], domian["name"], domian["records"])
        else:
            raise Exception("no domain found")
        return domians

    def getRecords(self,domain_id):
        url = "https://dnsapi.cn/Record.List"
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT,
                "domain_id": domain_id
                }
        try:
            r = requests.post(url, data=data, timeout=10)
        except Exception,e:
            print e
        result = r.json()
        records = int(result["info"]["record_total"])
        record_lst = []
        data = {'login_token': self.LOGIN_TOKEN, 'format': self.FORMAT, "domain_id": domain_id}
        r = requests.post(url, data=data, timeout=10)
        result = r.json()
        if "records" in result:
            for line in result["records"]:
                record_lst.append(line)

        else:
            raise Exception("get records failed")
        return record_lst

############################ NEW ############################取所有记录，比较慢
    def Get_Record(self,domain_id):
        url = "https://dnsapi.cn/Record.List"
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT,
                "domain_id": domain_id
                }
        r = requests.post(url, data=data, timeout=10)
        result = r.json()
        records = int(result["info"]["record_total"])
        record_lst = []
        offset, length, i = 0, 0, 0
        while (i < records):
            if records - offset < 3000:
                length = records - offset
            else:
                length = 3000
            data = {'login_token': self.LOGIN_TOKEN, 'format': self.FORMAT, "domain_id": domain_id, 'offset': offset,
                    "length": length}
            r = requests.post(url, data=data, timeout=10)
            result = r.json()

            i += 3000
            offset = i

            #print result
            if "records" in result:
                for line in result["records"]:
                    record_lst.append(line)

                #for record in result["records"]:
                #    print record["name"],record["type"],record["value"]
            else:
                raise Exception("get records failed")
        return record_lst

    def Record_del(self,domain_id,record_id):
        url = "https://dnsapi.cn/Record.Remove"
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT,
                "domain_id": domain_id,
                "record_id": record_id
                }
        r = requests.post(url, data=data, timeout=5)
        return r.json()

    def Get_domainlog(self,domain_id):
        url = "https://dnsapi.cn/Domain.Log"
        data = {'login_token': self.LOGIN_TOKEN,
                'format': self.FORMAT,
                "domain_id": domain_id,
                "length": 5
                }
        r = requests.post(url, data=data, timeout=5)
        result =  r.json()
        result = result['log']
        print result
        for line in result:
            print line

 #   def record_detail(self,domain,record_id):
 #       url = "https://dnsapi.cn/Record.Info"
 #       data = {'login_token': self.LOGIN_TOKEN,
 #               'format': self.FORMAT,
 #               "domain": domain,
 #               "record_id": record_id
 #               }













if __name__ == "__main__":
    aa = Dnspod()
    #print aa.domain_info('5678i.cn')
    #domains = aa.get_domainlist()
    #print domains
    #aa.get_records(domains)
   # print aa.record_info('2144.cn')
   # print aa.getRecords('5678i.cn')
    #print aa.Get_Record('37784273')
   # print aa.get_domainlist()
    #record_update(self, domain_id, record_name, record_id, record_value, record_line, record_type):
 #   print aa.record_update('37784273','optest3','335761325','www98.qq.com.','默认','CNAME')

    #print aa.get_records('5678i.cn')
    #print aa.get_domain('37784273')
    #print aa.record_add("37784273", "test8", "CNAME", "www.baidu.com")
    #print len(aa.Get_Record('207395'))
    #print aa.record_id('2144.cn','xxzb')
    domlst = aa.get_domainlist()
    print domlst
