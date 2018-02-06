#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import urllib
import urllib2
import json
from dnsmanage import settings

class UpyunCDN:

    def __init__(self):
        self.access_token = settings.upyun_token
        self.token_headers = {"Authorization": "Bearer %s" % self.access_token}

    def url_get(self, url, values=None, headers=None):
        """
        Get 访问
        """
        if values:
            data = urllib.urlencode(values)
            new_url = url + '?' + data
        else:
            new_url = url
        request = urllib2.Request(new_url, headers=self.token_headers)
        try:
            response = urllib2.urlopen(request, timeout=10)
            content = json.loads(response.read())
            return content
        except Exception as e:
            return e

    def url_post(self, url, values=None, headers=None):
        """
        Post 访问
        """
        if values:
            data = urllib.urlencode(values)
        else:
            data = None
        request = urllib2.Request(url, data, headers)
        try:
            response = urllib2.urlopen(request, timeout=10)
            content = json.loads(response.read())
            return content
        except Exception as e:
            return e

    def get_all_bucket(self):
        """
        获取所有的buckent,
        成功返回:{"status":"ok","buckets":[buckent1,buckent2,....]}
        错误返回:{"status":error,"info":str}
        """
        url = "https://api.upyun.com/buckets?limit=500"
        #url = "https://api.upyun.com/domains?limit=500"
        content = self.url_get(url)
        buckets_result = {}
        buckets_list = []
        if isinstance(content, (dict, list)):
            all_buckets = content.get("buckets")
            for bucket in all_buckets:
                buckets_list.append(bucket.get("bucket_name"))

            buckets_result["status"] = "ok"
            buckets_result["buckets"] = buckets_list
        else:
            buckets_result["status"] = "error"
            buckets_result["info"] = content
        return buckets_result

    def get_bucket_info(self, bucket_name):
        """
        获取单个bucket详细信息
        成功返回: {"status":"ok","info":{"status":status,domains:domains}}
        错误返回:{"status":error,"info":str}
        """
        url = "https://api.upyun.com/buckets/info/"
        bucket_info_result = {}
        values = {"bucket_name": bucket_name}
        content = self.url_get(url, values)
        if isinstance(content, (dict, list)):
            status = content.get("status",'')
            domains = content.get("approval_domains","")
            cname_domain = content.get("default_domain","")
            bucket_dic = {"bucket_name": bucket_name, "status": status, "domains": domains,"cname_domain": cname_domain}
            bucket_info_result["status"] = 'ok'
            bucket_info_result["info"] = bucket_dic
        else:
            bucket_info_result["status"] = 'error'
            bucket_info_result["info"] = content
        return bucket_info_result

    def get_domains_info(self,bucket_name):
        """
        获取domains详细信息
        """
        url = "https://api.upyun.com/buckets/domains/"
        bucket_info_result = {}
        values = {"bucket_name": bucket_name,"page": 1,"limit": 10 }
        content = self.url_get(url,values)
        return content
#        if isinstance(content, (dict, list)):
#            status = content.get("status",'')
#            domains = content.get("approval_domains","")
#            cname_domain = content.get("default_domain","")
#            bucket_dic = {"bucket_name": bucket_name, "status": status, "domains": domains,"cname_domain": cname_domain}
#            bucket_info_result["status"] = 'ok'
#            bucket_info_result["info"] = bucket_dic
#        else:
#            bucket_info_result["status"] = 'error'
#            bucket_info_result["info"] = content
#        return bucket_info_result


    def get_bucket_top(self, domain, date):
        url = "https://api.upyun.com/analysis/"
        # values = {"bucket_name": bucket_name, "date": date, 'type': 'url', 'domain':'box.2144.cn'}
        values = {"date": date, 'type': 'url', 'domain':domain, 'order_by':1}
        progress_content = self.url_get(url, values)
        print progress_content
        result = {}
        if isinstance(progress_content, dict):
            result["status"] = 'ok'
            result["info"] = progress_content.get("result")
        else:
            result["status"] = 'error'
            result["info"] = progress_content
        return result


    def get_cname(self,cdndomain):
        url = "https://api.upyun.com/buckets?limit=500"
        #url = "https://api.upyun.com/domains?limit=500"
        content = self.url_get(url)
        buckets_result = {}
        buckets_list = []
        if isinstance(content, (dict, list)):
            all_buckets = content.get("buckets")
            for bucket in all_buckets:
                buckets_list.append(bucket.get("bucket_name"))

            buckets_result["status"] = "ok"
            buckets_result["buckets"] = buckets_list
        else:
            buckets_result["status"] = "error"
            buckets_result["info"] = content
        buckets = buckets_result['buckets']
        cname_info = {}
        for bucket_name in  buckets:
          cname =  (upyun_obj.get_bucket_info(bucket_name))['info']['cname_domain']['domain']
	  for domain in (upyun_obj.get_bucket_info(bucket_name))['info']['domains']:
            cname_info[domain] = cname
        print cname_info[cdndomain]

    def get_upyuncdn(self):
        buckets = self.get_all_bucket()['buckets']
        lst = []
        try:
            for bucket in buckets:
                bukdict = {}
                rs = self.get_bucket_info(bucket)
                cname = rs["info"]["cname_domain"]["domain"]
                domains = rs["info"]["domains"]
                if len(domains) < 1:
                    pass
                elif len(domains) >= 1:
                    for domain in domains:
                        bukdict = {}
                        bukdict["domain"] = domain
                        bukdict["cname_domain"] = cname
                        lst.append(bukdict)
        except Exception,e:
            print e
        return lst


        




if __name__ == "__main__":
    upyun_obj = UpyunCDN()
#    bucket_top = upyun_obj.get_bucket_top('img.2258.com','2017-02-23')
#    print bucket_top
#    all_buckets = upyun_obj.get_all_bucket()
#    print(all_buckets)
#    bucket_info = upyun_obj.get_bucket_info('pdf-92wu-cn')    
#    print bucket_info
    #domain_info = upyun_obj.get_domains_info('pdf-92wu-cn')
    #print domain_info
#    upyun_obj.get_cname('kaer.2144.cn')
    # bucket_info = upyun_obj.get_bucket_info("www-2258-com")
    # bucket_info = upyun_obj.get_bucket_info("static-92wu")
    # bucket_info = upyun_obj.get_bucket_info("caijingstatic")
    # print(bucket_info)
    buckets = upyun_obj.get_all_bucket()['buckets']
    lst = []
    for bucket in buckets:
        bukdict = {}
        rs = upyun_obj.get_bucket_info(bucket)
        cname = rs["info"]["cname_domain"]["domain"]
        domains = rs["info"]["domains"]
        if len(domains)<1:
            pass
        elif len(domains) >= 1:
            for domain in domains:
                bukdict = {}
                bukdict["domain"] = domain
                bukdict["cname_domain"] = cname
                lst.append(bukdict)
    print lst
    print len(lst)




    #print upyun_obj.get_bucket_info('www-6255-com')
