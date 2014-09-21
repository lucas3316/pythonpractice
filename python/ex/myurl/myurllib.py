#!/usr/bin/env python

# -*- coding: utf-8 -*-

import time
import timeit
import sys
import gzip
import socket
import urllib.request, urllib.parse, urllib.error
import http.cookiejar

class httptest:

    def __init__(self, timeout=10, addHeaders=True):

        socket.setdefaulttimeout(timeout)

        self.__opener = urllib.request.build_opener()

        urllib.request.install_opener(self.__opener)

        if addHeaders: self.__addHeaders()
        

    def __error(self, e):
    
        print(e)
        
    
    def __addHeaders(self):
    
    
        self.__opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'),
    
                                    ('Connection', 'keep-alive'),
    
                                    ('Cache-Control', 'no-cache'),
    
                                    ('Accept-Language:', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
    
                                    ('Accept-Encoding', 'gzip, deflate'),
    
                                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
    
    def __decode(self, webPage, charset):
    
    
        if webPage.startswith(b'x1fx8b'):
    
            return gzip.decompress(webPage).decode(charset)
    
        else:
    
            return webPage.decode(charset)
        
    
    def addCookiejar(self):
    
    
        cj = http.cookiejar.CookieJar()
    
        self.__opener.add_handler(urllib.request.HTTPCookieProcessor(cj))
        
    
    def addProxy(self, host, type='http'):
    
    
        proxy = urllib.request.ProxyHandler({type: host})
    
        self.__opener.add_handler(proxy)
        
    
    def addAuth(self, url, user, pwd):
    
    
        pwdMsg = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        pwdMsg.add_password(None, url, user, pwd)
        auth = urllib.request.HTTPBasicAuthHandler(pwdMsg)
        self.__opener.add_handler(auth)
    
    def get(self, url, params={}, headers={}, charset='UTF-8'):
    
        if params: url += '?' + urllib.parse.urlencode(params)
        request = urllib.request.Request(url)
        for k,v in headers.items(): request.add_header(k, v)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset)
                        
    
    def post(self, url, params={}, headers={}, charset='UTF-8'):
    
        params = urllib.parse.urlencode(params)
        request = urllib.request.Request(url, data=params.encode(charset))
        for k,v in headers.items(): request.add_header(k, v)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            self.__error(e)
        else:
            return self.__decode(response.read(), charset)
        
    def download(self, url, savefile):
        header_gzip = None
        block_num = 0
        for header in self.__opener.addheaders:
            if 'Accept-Encoding' in header:
                header_gzip = header
                self.__opener.addheaders.remove(header)
    
        def reporthook(a, b, c):
            nonlocal block_num
            block_total = c/b
            per = 100 * a * b / c
            if per > 100: per = 100   
            if a-block_num==100 or per==100:
                print('%.1f%%\r' % (per),end='')
                block_num = a
            #time.sleep(1)

                
        try:
            urllib.request.urlretrieve(url, savefile, reporthook)
        except urllib.error.HTTPError as e:
            self.__error(e)
        finally:
            self.__opener.addheaders.append(header_gzip)