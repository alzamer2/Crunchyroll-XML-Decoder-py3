﻿#!/usr/bin/env python3.5.3
# -*- coding: utf-8 -*-
def get_proxy(types_,countries_):
    import requests
    import re
    if countries_[0] == 'US':
        proxy_list = []
        proxy_html = requests.get('https://www.us-proxy.org/')
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>(..)</td><td class='hm'>.+?</td><td>(.+?)</td><td class='hm'>.+?</td><td class='hx'>(.+?)</td><td class='hm'>'''
        )
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                #print(i[0], i[1], i[2], i[3], i[4])
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        proxy_html = requests.get(
            'https://www.xroxy.com/free-proxy-lists/?port=&type=Distorting&ssl=ssl&country=US&latency=&reliability=')
        _pattern = re.compile(
            r'''<td tabindex="\d" class="sorting_\d">(\d+\.\d+\.\d+\.\d+)<\/td>\n\s+<td>(\d+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td><img.+?><small>(?:&nbsp;)?(.+)<\/small>''')
        for i in _pattern.findall(proxy_html.text):
            proxy_list += [i[0] + ':' + i[1]]


    elif countries_[0] == 'GB':
        proxy_list = []
        proxy_html = requests.get('https://free-proxy-list.net/uk-proxy.html')
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>(..)</td><td class='hm'>.+?</td><td>(.+?)</td><td class='hm'>.+?</td><td class='hx'>(.+?)</td><td class='hm'>'''
        )
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                #print(i[0], i[1], i[2], i[3], i[4])
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        proxy_html = requests.get(
            'https://www.xroxy.com/free-proxy-lists/?port=&type=Distorting&ssl=ssl&country=GB&latency=&reliability=')
        _pattern = re.compile(
            r'''<td tabindex="\d" class="sorting_\d">(\d+\.\d+\.\d+\.\d+)<\/td>\n\s+<td>(\d+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td><img.+?><small>(?:&nbsp;)?(.+)<\/small>''')
        for i in _pattern.findall(proxy_html.text):
            proxy_list += [i[0] + ':' + i[1]]

    else:
        proxy_html = requests.get('https://www.sslproxies.org/')
        proxy_list = []
        _pattern = re.compile(
            r'''<tr><td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td><td>(..)</td><td class='hm'>.+?</td><td>(.+?)</td><td class='hm'>.+?</td><td class='hx'>(.+?)</td><td class='hm'>'''
        )
        for i in _pattern.findall(proxy_html.text):
            if i[4] == 'yes':
                if i[3] == 'elite proxy':
                    if i[2] == countries_[0]:
                        proxy_list += [i[0] + ':' + i[1]]
        proxy_html = requests.get(
            'https://www.xroxy.com/free-proxy-lists/?port=&type=Distorting&ssl=ssl&country='+countries_[0]+'&latency=&reliability=')
        _pattern = re.compile(
            r'''<td tabindex="\d" class="sorting_\d">(\d+\.\d+\.\d+\.\d+)<\/td>\n\s+<td>(\d+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td>(\w+)<\/td>\n\s+<td><img.+?><small>(?:&nbsp;)?(.+)<\/small>''')
        for i in _pattern.findall(proxy_html.text):
            proxy_list += [i[0] + ':' + i[1]]
    return proxy_list


if __name__ == '__main__':
    print(get_proxy(['HTTPS'],['US']))
