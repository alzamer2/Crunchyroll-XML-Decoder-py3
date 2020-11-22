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

        datasets = []
        datasets = xroxy_parser('https://www.xroxy.com/proxylist.php', {'ssl': 'ssl', 'country': 'US'})
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

        datasets = []
        datasets = xroxy_parser('https://www.xroxy.com/proxylist.php', {'ssl': 'ssl', 'country': 'GB'})
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
    if len(arg) == 1:
        return get_proxy_from_web(arg[0])
    elif len(arg) == 2:
        return get_proxy_from_web(arg[1])[arg[0][0].lower()]
        

if __name__ == '__main__':
    print(get_proxy(['GB']))
   #print(get_proxy(['HTTPS'],['US']))
    
