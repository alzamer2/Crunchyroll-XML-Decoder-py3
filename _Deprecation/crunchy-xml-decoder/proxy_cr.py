#!/usr/bin/env python3.5.3
# -*- coding: utf-8 -*-
def get_proxy2(types_,countries_):
    import asyncio
    from proxybroker import Broker

    async def show(proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            return str(proxy.host) + ":" + str(proxy.port)
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=types_, countries=countries_,limit=1),show(proxies))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

def get_proxy3(types_,countries_):
    from base64 import b64decode
    import requests
    import re
    _pattern = re.compile(
        r'''decode\("([\w=]+)".*?\("([\w=]+)"\)''', flags=re.DOTALL
    )
    for i in types_:
        for l in countries_:
            #proxy_html = requests.post('http://free-proxy.cz/en/proxylist/country/'+l.upper()+'/'+i.lower()+'/ping/level1')
            proxy_html = requests.post('http://free-proxy.cz/en/proxylist/country/US/https/ping/level1')
            print(proxy_html)
            return [
                (b64decode(h).decode(), b64decode(p).decode())
                for h, p in _pattern.findall(proxy_html.text)
            ]

def get_proxy(types_,countries_):
    import requests
    import re
    if countries_[0] == 'US':
        proxy_html = requests.get('https://www.us-proxy.org/')
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)<\/td><td>(\d+)<\/td><td>(..)<\/td><td class='hm'>.+?<\/td><td>(.+?)<\/td><td class='hm'>.+?<\/td><td class='hx'>(.+?)<\/td><td class='hm'>'''
        )
        proxy_list = []
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                #print(i[0], i[1], i[2], i[3], i[4])
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        return proxy_list


    elif countries_[0] == 'GB':
        proxy_html = requests.get('https://free-proxy-list.net/uk-proxy.html')
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)<\/td><td>(\d+)<\/td><td>(..)<\/td><td class='hm'>.+?<\/td><td>(.+?)<\/td><td class='hm'>.+?<\/td><td class='hx'>(.+?)<\/td><td class='hm'>'''
        )
        proxy_list = []
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                #print(i[0], i[1], i[2], i[3], i[4])
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        return proxy_list

    else:
        proxy_html = requests.get('https://www.sslproxies.org/')
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)<\/td><td>(\d+)<\/td><td>(..)<\/td><td class='hm'>.+?<\/td><td>(.+?)<\/td><td class='hm'>.+?<\/td><td class='hx'>(.+?)<\/td><td class='hm'>'''
        )
        proxy_list = []
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        return proxy_list



if __name__ == '__main__':
    print(get_proxy(['HTTPS'],['US']))
