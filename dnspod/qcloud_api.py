#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import requests
import binascii
import hmac
import random
import sys
import time
from pprint import pprint
from dnsmanage import settings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding("utf-8")

try: import simplejson as json
except: import json




class Sign:
    def __init__(self, secretId, secretKey):
        self.secretId = secretId
        self.secretKey = secretKey

    def make(self, requestHost, requestUri, params, method = 'GET'):
        srcStr = method.upper() + requestHost + requestUri + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
        hashed = hmac.new(self.secretKey, srcStr, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]


class Request:
    def __init__(self, secretId, secretKey):
        self.timeout = 10
        self.version = 'Python_Tools'
        self.secretId = secretId
        self.secretKey = secretKey

    def send(self, requestHost, requestUri, params, method = 'GET', debug = 0):
        params['RequestClient'] = self.version
        params['SecretId'] = self.secretId
        sign = Sign(self.secretId, self.secretKey)
        params['Signature'] = sign.make(requestHost, requestUri, params, method)
        url = 'https://%s%s' % (requestHost, requestUri)

        if debug:
            print(method.upper(), url)
            print('Request Args:')
            pprint(params)
        if method.upper() == 'GET':
            req = requests.get(url, params=params, timeout=self.timeout, verify=False)
        else:
            req = requests.post(url, data=params, timeout=self.timeout, verify=False)
        if debug:
            print("Response:", req.status_code, req.text)
        if req.status_code != requests.codes.ok:
            return req.status_code
        else:
            return req.text


class Cdn:
    def __init__(self):
        self.secretId = settings.qcloud_secretId
        self.secretKey = settings.qcloud_secretKey
        self.host = 'cdn.api.qcloud.com'
        self.uri = '/v2/index.php'
        self.method = "POST"
        self.debug = 0


    def DescribeCdnHosts(self):
        """
        查询CDN加速域名对应的CNAME
        Action:'DescribeCdnHosts'
        Qcloud API URL: https://www.qcloud.com/document/api/228/3937
        """
        params = {
            'Nonce': random.randint(1, sys.maxint),
            'Timestamp': int(time.time()),
            'Action': 'DescribeCdnHosts',
        }
        # params["Action"] = 'DescribeCdnHosts'
        request = Request(self.secretId, self.secretKey)
        result = request.send(self.host, self.uri, params, self.method, self.debug)
        result = json.loads(result)
        result = result["data"]["hosts"]
        cdnlst = []
        for line in result:
            cdndict = {}
            if line["host_type"] == 'cname':
                cdndict["host"] = line["host"]
                cdndict["cname"] = line["cname"]
                cdndict["origin"] = line["origin"]
                cdnlst.append(cdndict)

        return cdnlst




if __name__ == '__main__':
    aa = Cdn()
    print aa.DescribeCdnHosts()