#!/usr/bin/env python3.5.3
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import math

def xroxy_parser(url, params = {}):
    table = []
    if 'pnum' in params:
        params['pnum'] = 0
    proxy_html = requests.get(url, params=params)
    soup = BeautifulSoup(proxy_html.text, 'html.parser')
    table = soup.find_all('th', text='IP address')[0].find_parent("table")
    headings = [th.get_text().strip().replace('\n', ' ') for th in table.find_all('th', text='IP address')[0].find_parent("tr").find_all("th")][:-1]
    datasets = []
    for row in table.find_all("tr")[3:]:
        for td in row.find_all("td"):
            dataset = dict(zip(headings, (td.get_text().strip() for td in row.find_all("td"))))
            if re.match('\d+\.\d+\.\d+\.\d+', dataset['IP address']):
                if not dataset in datasets:
                    datasets.append(dataset)
    page_numb = math.ceil(int(soup.find_all('b', text='Page 1')[0].find_parent("table").find_all('td')[-1].b.text)/10)
    #print(page_numb)
    if page_numb >1:
        for i_page_numb in range(1,page_numb):
            params['pnum'] = i_page_numb
            proxy_html = requests.get(url, params=params)
            soup = BeautifulSoup(proxy_html.text, 'html.parser')
            table = soup.find_all('th', text='IP address')[0].find_parent("table")
            for row in table.find_all("tr")[3:]:
                for td in row.find_all("td"):
                    dataset = dict(zip(headings, (td.get_text().strip() for td in row.find_all("td"))))
                    if re.match('\d+\.\d+\.\d+\.\d+', dataset['IP address']):
                        if not dataset in datasets:
                            datasets.append(dataset)
    
    return datasets

def get_proxy_(types_,countries_):
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

def get_proxy_from_web(countries_):
    proxy_list = {}
    if countries_[0] == 'US':
        http_ = []
        https_ = []
        socks4_ = []
        socks5_ = []
        proxy_html = requests.get('https://www.us-proxy.org/')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            if not dataset in datasets:
                datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == 'US':
                    if item['Anonymity'] == 'elite proxy':
                        https_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    else:
                        http_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
        proxy_html = requests.get('https://www.socks-proxy.net/')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == 'US':
                    if item['Version'] == 'Socks4':
                        socks4_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    elif item['Version'] == 'Socks5':
                        socks5_ += ['{}:{}'.format(item['IP Address'], item['Port'])]

        #http_ = []
        #https_ = []
        #socks4_ = []
        #socks5_ = []

        datasets = []
        datasets = xroxy_parser('https://www.xroxy.com/proxylist.php', {'ssl': 'ssl', 'country': 'US'})
        #print(datasets)
        for item in datasets:
            #print(item)
            if len(item) > 0:
                if item['Type'] == 'Distorting':
                    https_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks4':
                    socks4_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks5':
                    socks5_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                else:
                        http_ += ['{}:{}'.format(item['IP address'], item['Port'])]
        #print(http_)
        #print(https_)
        #print(socks4_)
        #print(socks5_)
        proxy_list = {'http': http_, 'https': https_, 'socks4': socks4_, 'socks5': socks5_}

    elif countries_[0] == 'GB' or countries_[0] == 'UK':
        http_ = []
        https_ = []
        socks4_ = []
        socks5_ = []
        proxy_html = requests.get('https://free-proxy-list.net/uk-proxy.html')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            if not dataset in datasets:
                datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == 'GB':
                    if item['Anonymity'] == 'elite proxy':
                        https_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    else:
                        http_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
        proxy_html = requests.get('https://www.socks-proxy.net/')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == 'GB':
                    if item['Version'] == 'Socks4':
                        socks4_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    elif item['Version'] == 'Socks5':
                        socks5_ += ['{}:{}'.format(item['IP Address'], item['Port'])]

        #print(http_)
        #print(https_)
        #print(socks4_)
        #print(socks5_)

        datasets = []
        datasets = xroxy_parser('https://www.xroxy.com/proxylist.php', {'ssl': 'ssl', 'country': 'GB'})
        #print(datasets)
        for item in datasets:
            #print(item)
            if len(item) > 0:
                if item['Type'] == 'Distorting':
                    https_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks4':
                    socks4_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks5':
                    socks5_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                else:
                    http_ += ['{}:{}'.format(item['IP address'], item['Port'])]

        #proxy_html = requests.get('https://www.xroxy.com/proxylist.php', params={'ssl': 'ssl', 'country': 'GB'})
        #soup = BeautifulSoup(proxy_html.text, 'html.parser')
        #table = soup.find_all('th', text='IP address')[0].find_parent("table")
        #headings = [th.get_text().strip().replace('\n', ' ') for th in table.find_all('th', text='IP address')[0].find_parent("tr").find_all("th")][:-1]
        #datasets = []
        #for row in table.find_all("tr")[3:]:
        #    for td in row.find_all("td"):
        #        dataset = dict(zip(headings, (td.get_text().strip() for td in row.find_all("td"))))
        #        if not dataset in datasets:
        #            datasets.append(dataset)
        #for item in datasets:
        #    print(item)
        #    if len(item) > 0:
        #        if re.match('\d+\.\d+\.\d+\.\d+', item['IP address']):
        #            if item['Type'] == 'Distorting':
        #                https_ += ['{}:{}'.format(item['IP address'], item['Port'])]
        #            elif item['Type'] == 'Socks4':
        #                socks4_ += ['{}:{}'.format(item['IP address'], item['Port'])]
        #            elif item['Type'] == 'Socks5':
        #                socks5_ += ['{}:{}'.format(item['IP address'], item['Port'])]
        #            else:
        #                http_ += ['{}:{}'.format(item['IP address'], item['Port'])]
        #print(http_)
        #print(https_)
        #print(socks4_)
        #print(socks5_)
        proxy_list = {'http': http_, 'https': https_, 'socks4': socks4_, 'socks5': socks5_}
    else:
        http_ = []
        https_ = []
        socks4_ = []
        socks5_ = []
        proxy_html = requests.get('https://www.sslproxies.org/')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            if not dataset in datasets:
                datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == countries_[0]:
                    if item['Anonymity'] == 'elite proxy':
                        https_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    else:
                        http_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
        proxy_html = requests.get('https://www.socks-proxy.net/')
        soup = BeautifulSoup(proxy_html.text, 'html.parser')
        table = soup.find("table")
        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]
        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            datasets.append(dataset)
        for item in datasets:
            if len(item) > 0:
                if item['Code'] == countries_[0]:
                    if item['Version'] == 'Socks4':
                        socks4_ += ['{}:{}'.format(item['IP Address'], item['Port'])]
                    elif item['Version'] == 'Socks5':
                        socks5_ += ['{}:{}'.format(item['IP Address'], item['Port'])]


        datasets = []
        datasets = xroxy_parser('https://www.xroxy.com/proxylist.php', {'ssl': 'ssl', 'country': countries_[0]})
        for item in datasets:

            if len(item) > 0:
                if item['Type'] == 'Distorting':
                    https_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks4':
                    socks4_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                elif item['Type'] == 'Socks5':
                    socks5_ += ['{}:{}'.format(item['IP address'], item['Port'])]
                else:
                    http_ += ['{}:{}'.format(item['IP address'], item['Port'])]

        proxy_list = {'http': http_, 'https': https_, 'socks4': socks4_, 'socks5': socks5_}

    return proxy_list
        
            
            
def get_proxy(*arg):
    #print(len(arg))
    if len(arg) == 1:
        return get_proxy_from_web(arg[0])
    elif len(arg) == 2:
        return get_proxy_from_web(arg[1])[arg[0][0].lower()]
        

if __name__ == '__main__':
    print(get_proxy(['GB']))
    #print(get_proxy(['HTTPS'],['US']))
    
