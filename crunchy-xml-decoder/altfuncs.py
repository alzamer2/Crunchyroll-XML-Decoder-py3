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
import json
from unidecode import unidecode

from urllib.request import url2pathname
import os


def config():
    configr = ConfigParser()
    configr.read('settings.ini')
    quality = configr.get('SETTINGS', 'video_quality')
    langd = {'Espanol_Espana': u'Español (Espana)', 'Francais': u'Français (France)',
             'Portugues': u'Português (Brasil)',
             'English': u'English', 'Espanol': u'Español', 'Turkce': u'Türkçe', 'Italiano': u'Italiano',
             'Arabic': u'العربية', 'Deutsch': u'Deutsch', 'Russian': u'Русский'}
    lang = langd[configr.get('SETTINGS', 'language')]
    lang2 = langd[configr.get('SETTINGS', 'language2')]
    forcesub = configr.getboolean('SETTINGS', 'forcesubtitle')
    forceusa = configr.getboolean('SETTINGS', 'forceusa')
    localizecookies = configr.getboolean('SETTINGS', 'localizecookies')
    onlymainsub = configr.getboolean('SETTINGS', 'onlymainsub')
    connection_n_ = int(configr.get('SETTINGS', 'connection_n_'))
    proxy_ = configr.get('SETTINGS', 'Proxy')
    return [lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_]

class LocalFileAdapter(requests.adapters.BaseAdapter):
    """Protocol Adapter to allow Requests to GET file:// URLs
    to use when debuging

    @todo: Properly handle non-empty hostname portions.
    """

    @staticmethod
    def _chkpath(method, path):
        """Return an HTTP status for the given filesystem path."""
        if method.lower() in ('put', 'delete'):
            return 501, "Not Implemented"  # TODO
        elif method.lower() not in ('get', 'head'):
            return 405, "Method Not Allowed"
        elif os.path.isdir(path):
            return 400, "Path Not A File"
        elif not os.path.isfile(path):
            return 404, "File Not Found"
        elif not os.access(path, os.R_OK):
            return 403, "Access Denied"
        else:
            return 200, "OK"

    def send(self, req, **kwargs):  # pylint: disable=unused-argument
        """Return the file specified by the given request

        @type req: C{PreparedRequest}
        @todo: Should I bother filling `response.headers` and processing
               If-Modified-Since and friends using `os.stat`?
        """
        path = os.path.normcase(os.path.normpath(url2pathname(req.path_url)))
        response = requests.Response()

        response.status_code, response.reason = self._chkpath(req.method, path)
        if response.status_code == 200 and req.method.lower() != 'head':
            try:
                response.raw = open(path, 'rb')
            except (OSError, IOError) as err:
                response.status_code = 500
                response.reason = str(err)

        if isinstance(req.url, bytes):
            response.url = req.url.decode('utf-8')
        else:
            response.url = req.url

        response.request = req
        response.connection = self

        return response

    def close(self):
        pass


def gethtml(url, req='', headers=''):
    # session = requests.session()
    session = cfscrape.create_scraper()
    session.mount('file://', LocalFileAdapter())
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
    session.cookies['session_id'] = cookies_.get('COOKIES', 'sess_id')
    lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    if forceusa:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id_usa')
        session.cookies['session_id'] = cookies_.get('COOKIES', 'sess_id_usa')
    del session.cookies['c_visitor']
    if not forceusa and localizecookies:
        session.cookies['c_locale'] = \
        {u'Español (Espana)': 'esES', u'Français (France)': 'frFR', u'Português (Brasil)': 'ptBR',
         u'English': 'enUS', u'Español': 'esLA', u'Türkçe': 'enUS', u'Italiano': 'itIT',
         u'العربية': 'arME', u'Deutsch': 'deDE', u'Русский': 'ruRU'}[lang]

    if not urlparse(url).scheme and not urlparse(url).netloc:
        print('Apparently not a URL')
        sys.exit()
    if headers == '':
        headers = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
                   'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    res = session.get(url, params=req, headers=headers)
    # print(session.get(url, params=req, headers=headers).url)
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
        # xml_ = etree.fromstring(html.encode('UTF-8'))
        return html
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': med_id, 'video_format': video_format,
                   'video_quality': resolution, 'auto_play': '1', 'show_pop_out_controls': '1',
                   'current_page': 'http://www.crunchyroll.com/'}
        html = gethtml(url, payload, headers)
        xml_ = etree.fromstring(str.encode(html))
        # print( {i.tag:i.text for i in xml_.findall('.//stream_info/.')[0]})
        # print( {'subtitle':[[i.attrib['id'],i.attrib['title'],i.attrib['link']] for i in xml_.findall('.//subtitle/.[@link]')]})
        # print(dict(list({i.tag:i.text for i in xml_.findall('.//stream_info/.')[0]}.items())+list({'subtitle':[[i.attrib['id'],i.attrib['title'],i.attrib['link']] for i in xml_.findall('.//subtitle/.[@link]')]}.items())+list({'media_metadata':{i.tag:i.text for i in xml_.findall('.//media_metadata/.')[0]}}.items())))
        return dict(list({i.tag: i.text for i in xml_.findall('.//stream_info/.')[0]}.items()) + list({'subtitle': [
            [i.attrib['id'], i.attrib['title'], i.attrib['link']] for i in
            xml_.findall('.//subtitle/.[@link]')]}.items()) + list(
            {'media_metadata': {i.tag: i.text for i in xml_.findall('.//media_metadata/.')[0]}}.items()))

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
    # sess_id_ = cookies_.get('COOKIES', 'sess_id')
    # if forceusa:
    #    sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
    payload = {'session_id': sess_id_, 'media_type': 'anime', 'fields': 'series.url,series.series_id', 'limit': '1500',
               'filter': 'prefix:' + re.sub(r'https?://www\.crunchyroll\.com/', '', url)[:1]}
    list_series = session.post('http://api.crunchyroll.com/list_series.0.json', params=payload).json()
    # print list_series['data'][877],len(list_series['data'])
    url_trim = re.findall(r'https?://www\.crunchyroll\.com/.+(/.+)',url)
    if url_trim == []:
        url_trim = ''
    else:
        url_trim = url_trim[0]
    url = re.sub(url_trim,'',url)
    series_id = ''
    for i in list_series['data']:
        if re.findall(r'https?://(www\.crunchyroll\.com/.+)',url) == re.findall(r'https?://(www\.crunchyroll\.com/.+)',i['url']):
            series_id = i['series_id']
    payload = {'session_id': sess_id_, 'series_id': series_id, 'fields': 'media.url', 'limit': '1500'}
    list_media = session.post('http://api.crunchyroll.com/list_media.0.json', params=payload).json()
    #print(list_media)
    aList = []
    take = open("queue.txt", "w")
    take.write(u'#the any line that has hash before the link will be skiped\n')
    aList.reverse()
    for i in list_media['data']:
        # print >> take, i['url']
        print(i['url'], file=take)
    take.close()


def dircheck(text_=[], text_condition_=[], max_len=255, max_retries=''):
    '''
    True	forced
    False	optinal
    0		remove
    1+		keep reducing untill deleting it
    '''
    if not text_:
        return 'nothing to do here'
    elif len(text_condition_) < len(text_):
        text_condition_ += ['False'] * (len(text_) - len(text_condition_))
    elif len(text_condition_) > len(text_):
        return 'something is wroung with inputed data'
    output_data_ = ''
    retries_ = 0
    for i in text_:
        output_data_ += i
    while len(output_data_) > max_len:
        retries_ += 1
        # output_data_ = output_data_[:-1]
        # for i,k in enumerate(reversed(text_condition_)):
        output_data_ = ''
        for i, k in enumerate(text_condition_):
            if k == 0:
                text_[i] = ''
        for i in text_:
            output_data_ += i
        loop_check_output = output_data_
        # print output_data_
        try:
            text_[len(text_condition_) - text_condition_[::-1].index('False') - 1] = ''
            text_condition_[len(text_condition_) - text_condition_[::-1].index('False') - 1] = 0
        except:
            for i, k in enumerate(text_condition_[::-1]):
                if type(k) is int:
                    if k != 0 and k < len(text_[::-1][i]):
                        text_[len(text_condition_) - i - 1] = text_[len(text_condition_) - i - 1][:-1]
        if not max_retries == '':
            if retries_ >= max_retries:
                break
        output_data_ = ''
        for i in text_:
            output_data_ += i
        if loop_check_output == output_data_:
            break
    return output_data_

def vilos_subtitle(page_url_='', one_sub=None):
    print('''
------------------------------
---- Downloading Subtitle ----
------------------------------''')
    lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    if page_url_ is '':
        page_url_ = input('Please enter Crunchyroll video URL:\n')
    if not re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)', page_url_):
        print(idle_cmd_txt_fix("\x1b[31m" + "ERROR: Invalid URL." + "\x1b[0m"))
        exit()
    html_page_ = gethtml(page_url_)
    htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})', html_page_)[0])
    htmlconfig['metadata']['series_title'] = \
    json.loads(re.findall(r'vilos\.config\.analytics = ({.*})', html_page_)[0])['media_reporting_parent']['title']
    lang_iso = {'enUS' : 'English (US)', 'esLA' : u'Espa\xf1ol', 'esES' : u'Espa\xf1ol (Espa\xf1a)',
                'frFR' : u'Fran\xe7ais (France)', 'ptBR' : u'Portugu\xeas (Brasil)', 'itIT' : 'Italiano',
                'deDE' : 'Deutsch','arME' :  'العربية', 'ruRU' : 'Русский','enGB' : 'English (UK)', 'trTR':'uTürkçe'}
    lang_iso2 = {'enUS': 'eng', 'esLA': 'spa', 'esES': 'spa', 'frFR': 'fre', 'ptBR': 'por', 'itIT': 'ita',
                 'deDE': 'deu', 'arME': 'ara', 'ruRU': 'rus', 'enGB': 'eng', 'trTR': 'tur'}
    Loc_lang = {u'Español (Espana)': 'esES', u'Français (France)': 'frFR', u'Português (Brasil)': 'ptBR',
                u'English': 'enUS', u'Español': 'esLA', u'Türkçe': 'trTR', u'Italiano': 'itIT',
                u'العربية': 'arME', u'Deutsch': 'deDE', u'Русский': 'ruRU'}

    if one_sub is None:
        one_sub = onlymainsub
    #avible_sub=[]
    one_sub_lang = ''
    for i in htmlconfig['subtitles']:
        #print(i["language"], Loc_lang[lang],Loc_lang[lang2],one_sub_lang)
        if i["language"] == Loc_lang[lang]:
            one_sub_lang = i["language"]
        if one_sub_lang == '':
            if i["language"] == Loc_lang[lang2]:
                one_sub_lang = i["language"]
        #avible_sub += [i["language"]]
    if one_sub_lang == '':
        try:
            one_sub_lang = htmlconfig['subtitles'][0]["language"]
        except IndexError:
            print('The video has hardcoded subtitles.')
            exit()

    for i in htmlconfig['subtitles']:
        if one_sub is True:
            if i["language"] != one_sub_lang:
                continue
        if not htmlconfig['metadata']['episode_number'] is '':
            sub_file_ = dircheck([os.path.abspath('export') + '\\',
                                  clean_text(htmlconfig['metadata']['series_title']),
                                  ' Episode',
                                  ' - ' + clean_text(htmlconfig['metadata']['episode_number']),
                                  ' - ' + clean_text(htmlconfig['metadata']['title']),
                                  '[' + lang_iso2[i["language"]] + ']',
                                  '[' + lang_iso[i["language"]] + ']',
                                  '.ass'],
                                 ['True', 'True', 'False', 'True', 1, 'True', 'False', 'True'], 240)
        else:
            sub_file_ = dircheck([os.path.abspath('export') + '\\',
                                  clean_text(htmlconfig['metadata']['series_title']),
                                  ' - ' + clean_text(htmlconfig['metadata']['title']),
                                  '[' + lang_iso2[i["language"]] + ']',
                                  '[' + lang_iso[i["language"]] + ']',
                                  '.ass'],
                                 ['True', 'True', 1, 'True', 'False', 'True'], 240)
        #print(i["language"], i["url"])
        try:
            print(idle_cmd_txt_fix("Attempting to download " + '\x1b[32m' + lang_iso[i["language"]] + '\x1b[0m' + " subtitle..."))
        except:
            print(unidecode(idle_cmd_txt_fix("Attempting to download " + '\x1b[32m' + lang_iso[i["language"]] + '\x1b[0m' + " subtitle...")))
        subtitle_ = requests.get(i["url"]).content
        #subtitle_.encoding = 'utf-8'
        open(sub_file_,'wb').write(subtitle_)



def idle_cmd_txt_fix(print_text):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub(r'\\x1b.*?\[\d*\w','',print_text)
    return print_text

def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - '}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))
