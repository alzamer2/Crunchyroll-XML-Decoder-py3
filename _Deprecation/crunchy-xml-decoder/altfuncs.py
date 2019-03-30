#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from time import sleep
from urllib.parse import urlparse
from configparser import ConfigParser
import pickle
import requests
import cfscrape
from lxml import etree


def config():
    #global video_format
    #global resolution
    #global lang
    #global lang2
    #global forceusa
    #global localizecookies
    configr = ConfigParser()
    configr.read('settings.ini')
    quality = configr.get('SETTINGS', 'video_quality')
    #qualities = {'240p': ['107', '71'], '360p': ['106', '60'], '480p': ['106', '61'],
    #             '720p': ['106', '62'], '1080p': ['108', '80'], 'highest': ['0', '0']}
    #video_format = qualities[quality][0]
    #resolution = qualities[quality][1]

    langd = {'Espanol_Espana': u'Español (Espana)', 'Francais': u'Français (France)', 'Portugues': u'Português (Brasil)',
            'English': u'English', 'Espanol': u'Español', 'Turkce': u'Türkçe', 'Italiano': u'Italiano',
            'Arabic': u'العربية', 'Deutsch': u'Deutsch'}
    lang = langd[configr.get('SETTINGS', 'language')]
    lang2 = langd[configr.get('SETTINGS', 'language2')]
    forcesub = configr.getboolean('SETTINGS', 'forcesubtitle')
    forceusa = configr.getboolean('SETTINGS', 'forceusa')
    localizecookies = configr.getboolean('SETTINGS', 'localizecookies')
    onlymainsub = configr.getboolean('SETTINGS', 'onlymainsub')
    connection_n_ = int(configr.get('SETTINGS', 'connection_n_'))
    proxy_ = configr.get('SETTINGS', 'Proxy')
    return [lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_]

"""
#def playerrev(url):
#    global player_revision 
#
#    revision_regex = r"swfobject.embedSWF\(\"(?:.+)'(?P<revision>[\d.]+)'(?:.+)\)"
#    try:
#        player_revision = re.search(revision_regex, gethtml(url)).group("revision")
#    except IndexError:
#        try:
#            url += '?skip_wall=1'  # perv
#            html = gethtml(url)
#            player_revision = re.search(revision_regex, html).group("revision")
#        except IndexError:
#            open('debug.html', 'w').write(html.encode('utf-8'))
#            sys.exit('Sorry, but it looks like something went wrong with accessing the Crunchyroll page. Please make an issue on GitHub and attach debug.html which should be in the folder.')
#    return player_revision


def gethtml_old(url):
    with open('cookies') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        session = requests.session()
        session.cookies = cookies
        del session.cookies['c_visitor']
        if not forceusa and localizecookies:
            session.cookies['c_locale']={u'Español (Espana)' : 'esES', u'Français (France)' : 'frFR', u'Português (Brasil)' : 'ptBR',
                                        u'English' : 'enUS', u'Español' : 'esLA', u'Türkçe' : 'enUS', u'Italiano' : 'itIT',
                                        u'العربية' : 'arME' , u'Deutsch' : 'deDE'}[lang]
        if forceusa:
            try:
                session.cookies['sess_id'] = session.cookies['usa_sess_id']
            except:
                print 'get new season id'
                try:
                    session.cookies['sess_id'] = requests.get('https://cr.onestay.moe/getid').json()['sessionId'].encode('ascii', 'ignore')
                    #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
                except:
                    sleep(10)  # sleep so we don't overload crunblocker
                    session.cookies['sess_id'] = requests.get('https://rubbix.net/crunchyroll/').json()['sessionId'].encode('ascii', 'ignore')
    parts = urlparse.urlsplit(url)
    if not parts.scheme or not parts.netloc:
        print 'Apparently not a URL'
        sys.exit()
    data = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
            'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    res = session.get(url, params=data)
    res.encoding = 'UTF-8'
    return res.text


def getxml_old(req, med_id):
    url = 'http://www.crunchyroll.com/xml/'
    if req == 'RpcApiSubtitle_GetXml':
        payload = {'req': 'RpcApiSubtitle_GetXml', 'subtitle_script_id': med_id}
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': med_id, 'video_format': video_format,
                   'video_quality': resolution, 'auto_play': '1', 'show_pop_out_controls': '1',
                   'current_page': 'http://www.crunchyroll.com/'}
    else:
        payload = {'req': req, 'media_id': med_id, 'video_format': video_format, 'video_encode_quality': resolution}
    with open('cookies') as f:
        cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
        session = requests.session()
        session.cookies = cookies
        del session.cookies['c_visitor']
        if not forceusa and localizecookies:
            session.cookies['c_locale']={u'Español (Espana)' : 'esES', u'Français (France)' : 'frFR', u'Português (Brasil)' : 'ptBR',
                                        u'English' : 'enUS', u'Español' : 'esLA', u'Türkçe' : 'enUS', u'Italiano' : 'itIT',
                                        u'العربية' : 'arME' , u'Deutsch' : 'deDE'}[lang]
        if forceusa:
            try:
                session.cookies['sess_id'] = session.cookies['usa_sess_id']
            except:
                print 'get new season id'
                try:
                    session.cookies['sess_id'] = requests.get('https://cr.onestay.moe/getid').json()['sessionId'].encode('ascii', 'ignore')
                    #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
                except:
                    sleep(10)  # sleep so we don't overload crunblocker
                    session.cookies['sess_id'] = requests.get('https://rubbix.net/crunchyroll/').json()['sessionId'].encode('ascii', 'ignore')
                    #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
    headers = {'Referer': 'http://static.ak.crunchyroll.com/versioned_assets/ChromelessPlayerApp.17821a0e.swf',
               'Host': 'www.crunchyroll.com', 'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    res = session.post(url, params=payload, headers=headers)
    res.encoding = 'UTF-8'
    #print session.cookies
    return res.text


def vidurl(url, season, ep):  # experimental, although it does help if you only know the program page.
    res = gethtml(url)
    try:
        print re.findall('<img id=\"footer_country_flag\".+?title=\"(.+?)\"', res, re.DOTALL)[0]
    except:
        pass
    # open('video.html', 'w').write(res.encode('utf-8'))
    slist = re.findall('<a href="#" class="season-dropdown content-menu block text-link strong(?: open| ) '
                       'small-margin-bottom" title="(.+?)"', res)
    if slist:  # multiple seasons
        if len(re.findall('<a href=".+episode-(01|1)-(.+?)"', res)) > 1:  # dirty hack, I know
            # print list(reversed(slist))
            # season = int(raw_input('Season number: '))
            # season = sys.argv[3]
            # ep = raw_input('Episode number: ')
            # ep = sys.argv[2]
            season = slist[int(season)]
            # import pdb
            # pdb.set_trace()
            return 'http://www.crunchyroll.com' + re.findall(
                '<a href="(.+episode-0?' + ep + '-(?:.+-)?[0-9]{6})"', res)[slist.index(season)]
        else:
            # print list(reversed(re.findall('<a href=".+episode-(.+?)-',res)))
            # ep = raw_input('Episode number: ')
            # ep = sys.argv[2]
            return 'http://www.crunchyroll.com' + re.findall('<a href="(.+episode-0?' + ep + '-(?:.+-)?[0-9]{6})"',
                                                             res).pop()
    else:
        # 'http://www.crunchyroll.com/media-'
        # print re.findall('<a href=\"(.+?)\" title=\"(.+?)\"
        #  class=\"portrait-element block-link titlefix episode\"', res)
        # epnum = raw_input('Episode number: ')
        # epnum = sys.argv[2]
        return 'http://www.crunchyroll.com' + \
               re.findall('<a href=\"(.+?)\" .+ class=\"portrait-element block-link titlefix episode\"', res)[int(ep)]

def autocatch():
    url = raw_input(u'indicate the url : ')
    session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
    #sess_id_ = cookies_.get('COOKIES', 'sess_id')
    #if forceusa:
    #    sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
    payload = {'session_id' : sess_id_, 'media_type' : 'anime','fields':'series.url,series.series_id','limit':'1500','filter':'prefix:'+url.replace('http://www.crunchyroll.com/','')[:1]}
    list_series = session.post('http://api.crunchyroll.com/list_series.0.json', data=payload).json()
    #print list_series['data'][877],len(list_series['data'])
    series_id = ''
    for i in list_series['data']:
        if url == i['url']:
                series_id = i['series_id']
    payload = {'session_id' : sess_id_, 'series_id': series_id,'fields':'media.url','limit':'1500'}
    list_media = session.post('http://api.crunchyroll.com/list_media.0.json', data=payload).json()
    aList = []
    take = open("queue.txt", "w")
    take.write(u'#the any line that has hash before the link will be skiped\n')
    aList.reverse()
    for i in list_media['data']:
        print >> take, i['url']
    take.close()

def gethtml_old2(url):
    #with open('cookies') as f:
    #cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    session = requests.session()
    #session.cookies = cookies
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
    if forceusa:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id_usa')
    del session.cookies['c_visitor']
    if not forceusa and localizecookies:
        session.cookies['c_locale']={u'Español (Espana)' : 'esES', u'Français (France)' : 'frFR', u'Português (Brasil)' : 'ptBR',
                                    u'English' : 'enUS', u'Español' : 'esLA', u'Türkçe' : 'enUS', u'Italiano' : 'itIT',
                                    u'العربية' : 'arME' , u'Deutsch' : 'deDE'}[lang]
    '''
    if forceusa:
        try:
            session.cookies['sess_id'] = session.cookies['usa_sess_id']
        except:
            print 'get new season id'
            try:
                session.cookies['sess_id'] = requests.get('https://cr.onestay.moe/getid').json()['sessionId'].encode('ascii', 'ignore')
                #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
            except:
                sleep(10)  # sleep so we don't overload crunblocker
                session.cookies['sess_id'] = requests.get('https://rubbix.net/crunchyroll/').json()['sessionId'].encode('ascii', 'ignore')
    '''
    parts = urlparse.urlsplit(url)
    if not parts.scheme or not parts.netloc:
        print 'Apparently not a URL'
        sys.exit()
    data = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
            'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    res = session.get(url, params=data)
    res.encoding = 'UTF-8'
    return res.text

def getxml_old2(req, med_id):
    url = 'http://www.crunchyroll.com/xml/'
    if req == 'RpcApiSubtitle_GetXml':
        payload = {'req': 'RpcApiSubtitle_GetXml', 'subtitle_script_id': med_id}
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': med_id, 'video_format': video_format,
                   'video_quality': resolution, 'auto_play': '1', 'show_pop_out_controls': '1',
                   'current_page': 'http://www.crunchyroll.com/'}
    else:
        payload = {'req': req, 'media_id': med_id, 'video_format': video_format, 'video_encode_quality': resolution}
    #with open('cookies') as f:
    #cookies = requests.utils.cookiejar_from_dict(pickle.load(f))
    session = requests.session()
    #session.cookies = cookies
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
    if forceusa:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id_usa')
    del session.cookies['c_visitor']
    if not forceusa and localizecookies:
        session.cookies['c_locale']={u'Español (Espana)' : 'esES', u'Français (France)' : 'frFR', u'Português (Brasil)' : 'ptBR',
                                    u'English' : 'enUS', u'Español' : 'esLA', u'Türkçe' : 'enUS', u'Italiano' : 'itIT',
                                    u'العربية' : 'arME' , u'Deutsch' : 'deDE'}[lang]
    '''
    if forceusa:
        try:
            session.cookies['sess_id'] = session.cookies['usa_sess_id']
        except:
            print 'get new season id'
            try:
                session.cookies['sess_id'] = requests.get('https://cr.onestay.moe/getid').json()['sessionId'].encode('ascii', 'ignore')
                #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
            except:
                sleep(10)  # sleep so we don't overload crunblocker
                session.cookies['sess_id'] = requests.get('https://rubbix.net/crunchyroll/').json()['sessionId'].encode('ascii', 'ignore')
                #print 'I recommend to re-login so we don\'t overload crunchyroll unblocker'
    '''
    headers = {'Referer': 'http://static.ak.crunchyroll.com/versioned_assets/ChromelessPlayerApp.17821a0e.swf',
               'Host': 'www.crunchyroll.com', 'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    res = session.post(url, params=payload, headers=headers)
    res.encoding = 'UTF-8'
    #print session.cookies
    return res.text
"""
def gethtml(url,req='',headers=''):
    #session = requests.session()
    session = cfscrape.create_scraper()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
    lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    if forceusa:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id_usa')
    del session.cookies['c_visitor']
    if not forceusa and localizecookies:
        session.cookies['c_locale']={u'Español (Espana)' : 'esES', u'Français (France)' : 'frFR', u'Português (Brasil)' : 'ptBR',
                                    u'English' : 'enUS', u'Español' : 'esLA', u'Türkçe' : 'enUS', u'Italiano' : 'itIT',
                                    u'العربية' : 'arME' , u'Deutsch' : 'deDE'}[lang]

    if not urlparse(url).scheme and not urlparse(url).netloc:
        print('Apparently not a URL')
        sys.exit()
    if headers == '':
        headers = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
            'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    res = session.get(url, params=req, headers=headers)
    #print(session.get(url, params=req, headers=headers).url)
    res.encoding = 'UTF-8'
    return res.text

def getxml(req, med_id):
    url = 'http://www.crunchyroll.com/xml/'
    headers = {'Referer': 'http://static.ak.crunchyroll.com/versioned_assets/ChromelessPlayerApp.17821a0e.swf',
               'Host': 'www.crunchyroll.com', 'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    qualities = {'240p': ['107', '71'], '360p': ['106', '60'], '480p': ['106', '61'],
                 '720p': ['106', '62'], '1080p': ['108', '80'], 'highest': ['0', '0']}
    lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    video_format = qualities[quality][0]
    resolution = qualities[quality][1]
    if req == 'RpcApiSubtitle_GetXml':
        payload = {'req': 'RpcApiSubtitle_GetXml', 'subtitle_script_id': med_id}
        html = gethtml(url, payload, headers)
        #xml_ = etree.fromstring(html.encode('UTF-8'))
        return html
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': med_id, 'video_format': video_format,
                   'video_quality': resolution, 'auto_play': '1', 'show_pop_out_controls': '1',
                   'current_page': 'http://www.crunchyroll.com/'}
        html = gethtml(url, payload, headers)
        xml_ = etree.fromstring(str.encode(html))
        #print( {i.tag:i.text for i in xml_.findall('.//stream_info/.')[0]})
        #print( {'subtitle':[[i.attrib['id'],i.attrib['title'],i.attrib['link']] for i in xml_.findall('.//subtitle/.[@link]')]})
        #print(dict(list({i.tag:i.text for i in xml_.findall('.//stream_info/.')[0]}.items())+list({'subtitle':[[i.attrib['id'],i.attrib['title'],i.attrib['link']] for i in xml_.findall('.//subtitle/.[@link]')]}.items())+list({'media_metadata':{i.tag:i.text for i in xml_.findall('.//media_metadata/.')[0]}}.items())))
        return dict(list({i.tag:i.text for i in xml_.findall('.//stream_info/.')[0]}.items())+list({'subtitle':[[i.attrib['id'],i.attrib['title'],i.attrib['link']] for i in xml_.findall('.//subtitle/.[@link]')]}.items())+list({'media_metadata':{i.tag:i.text for i in xml_.findall('.//media_metadata/.')[0]}}.items()))


                   
        exit()
    else:
        payload = {'req': req, 'media_id': med_id, 'video_format': video_format, 'video_encode_quality': resolution}
        html = gethtml(url, payload, headers)
        xml_ = etree.fromstring(html)
        return xml_
def autocatch():
    url = input(u'indicate the url : ')
    session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
    #sess_id_ = cookies_.get('COOKIES', 'sess_id')
    #if forceusa:
    #    sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
    payload = {'session_id' : sess_id_, 'media_type' : 'anime','fields':'series.url,series.series_id','limit':'1500','filter':'prefix:'+re.sub('https?:\/\/www\.crunchyroll\.com\/','',url)[:1]}
    list_series = session.post('http://api.crunchyroll.com/list_series.0.json', params=payload).json()
    #print list_series['data'][877],len(list_series['data'])
    series_id = ''
    for i in list_series['data']:
        if url == i['url']:
                series_id = i['series_id']
    payload = {'session_id' : sess_id_, 'series_id': series_id,'fields':'media.url','limit':'1500'}
    list_media = session.post('http://api.crunchyroll.com/list_media.0.json', params=payload).json()
    aList = []
    take = open("queue.txt", "w")
    take.write(u'#the any line that has hash before the link will be skiped\n')
    aList.reverse()
    for i in list_media['data']:
        #print >> take, i['url']
        print(i['url'],file=take)
    take.close()
    
def dircheck(text_=[],text_condition_=[],max_len=255,max_retries=''):
    '''
    True	forced
    False	optinal
    0		remove
    1+		keep reducing untill deleting it
    '''
    if text_==[]:
        return 'nothing to do here'
    elif len(text_condition_) < len(text_):
        text_condition_ += ['False']*(len(text_)-len(text_condition_))
    elif len(text_condition_) > len(text_):
        return 'something is wroung with inputed data'
    output_data_ =''
    retries_=0
    for i in text_:
        output_data_ += i
    while len(output_data_) > max_len:
        retries_ += 1
        #output_data_ = output_data_[:-1]
        #for i,k in enumerate(reversed(text_condition_)):
        output_data_ =''
        for i,k in enumerate(text_condition_):
            if k == 0:
                text_[i] = ''		
        for i in text_:
            output_data_ += i
        loop_check_output = output_data_
        #print output_data_
        try:
            text_[len(text_condition_)-text_condition_[::-1].index('False')-1] = ''
            text_condition_[len(text_condition_)-text_condition_[::-1].index('False')-1] = 0
        except:
            for i,k in enumerate(text_condition_[::-1]):
                if type(k) is int:
                    if k != 0 and k < len(text_[::-1][i]):
                        text_[len(text_condition_)-i-1] = text_[len(text_condition_)-i-1][:-1]
        if not max_retries == '':
            if retries_ >= max_retries:
                break
        output_data_ =''
        for i in text_:
            output_data_ += i
        if loop_check_output == output_data_:
            break
    return output_data_

