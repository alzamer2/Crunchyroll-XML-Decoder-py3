#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
#from urllib.parse import urlparse
from configparser import ConfigParser
import requests
import cloudscraper
from lxml import etree
import json
from unidecode import unidecode

from urllib.request import url2pathname
import os

from requests.adapters import BaseAdapter
from requests.compat import urlparse, unquote
from requests.auth import HTTPBasicAuth
from requests import Response, codes
import errno
import os
import stat
import locale
import io

from bs4 import BeautifulSoup
import browser_cookie3
import subprocess
altfuncs_print_coding = False
from io import BytesIO

####### customs print
org_print = print
Green_c = '\x1b[32m'
Red_c = '\x1b[31m'
Default_c = '\x1b[0m'

def print_idle_cmd_txt_fix(value='', *args, **kwargs):
    if isinstance(value, str):
        if 'idlelib.run' in sys.modules:
            value = re.sub(r'\x1b.*?\[\d*(?:;\d*)?\w','',value)
    org_print(value, *args, **kwargs)

print = print_idle_cmd_txt_fix
#################

def config_old():
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

def config_old2():
    configr = ConfigParser()
    configr.read('settings.ini')
    config_dict = dict(configr['SETTINGS'])
    boolean_list = ['forcesubtitle', 'forceusa', 'localizecookies', 'onlymainsub', 'dubfilter']
    for i in boolean_list:
        config_dict[i] = {'True': True, '1': True, 'yes': True, 'true': True, 'on': True, 'False': False, '0': False,
                          'no': False, 'false': False, 'off': False}[config_dict[i]]
    int_list = ['connection_n_']
    for i in int_list:
        config_dict[i] = int(config_dict[i])
    langd = {'Espanol_Espana': u'Español (Espana)', 'Francais': u'Français (France)',
             'Portugues': u'Português (Brasil)',
             'English': u'English', 'Espanol': u'Español', 'Turkce': u'Türkçe', 'Italiano': u'Italiano',
             'Arabic': u'العربية', 'Deutsch': u'Deutsch', 'Russian': u'Русский'}
    language_list = ['language', 'language2']
    for i in language_list:
        config_dict[i] = langd[config_dict[i]]
    return config_dict

def config(defult=False, **kwargs):
    lastest_config_version = 1
    configr = ConfigParser()
    def set_with_comment(ConfigParser_obj, section, name, value='',comment=''):
        ConfigParser_obj.remove_option(section, name)
        if comment == '':
            ConfigParser_obj.set(section, name, value)
        else:
            ConfigParser_obj.set(section, '#'+comment+'\n'+name, str(value))

    comments = {
        'video_quality' : ''' Set this to the preferred quality. Possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
# Note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).
# We're not miracle workers.''',
        'language' : ''' Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option (below).
# Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch''',
        'language2' : ''' If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default''',
        'forcesubtitle' : ''' Set this if you want to use --forced-track rather than --default-track for subtitle''',
        'forceusa' : ''' Set this if you want to use a US session ID''',
        'localizecookies' : ''' Set this if you want to Localize the cookies (this option is under testing and may generate some problem and it willnot work with -forceusa- option)''',
        'onlymainsub' : ''' Set this if you only want to mux one subtitle only (this so make easy for some devices like TVs to play subtitle)''',
        'dubfilter' : ''' Set this if you autocatch dub links too''',
        'connection_n_' : ''' Set this option to increase the Number of the connection''',
        'proxy' : ''' Set this option to use proxy, example: US''',
        'download_dirctory' : '''the working dirctory where temp and downladed files saved'''
        }
    if os.path.lexists(os.path.join('.','settings.ini')):
        configr.read('settings.ini')
        if altfuncs_print_coding:   
            print(configr.sections())
            print('SETTINGS_v'+str(lastest_config_version) in configr.sections())
            input()
        check_setting_v = int(lastest_config_version)
        config_dict = dict()
        while check_setting_v>0:
            if 'SETTINGS_v'+str(check_setting_v) in configr.sections():
                if config_dict == {}:
                    config_dict = globals()['config_v'+str(check_setting_v)](defult,**kwargs)
            check_setting_v -=1
        if config_dict == {}:
            config_dict = config_v0(defult,**kwargs)
    else:
        config_dict = globals()['config_v'+str(lastest_config_version)](defult,**kwargs)
    config_dict_out = dict(config_dict)
    langd = {'Espanol_Espana': u'Español (Espana)',
             'Francais': u'Français (France)',
             'Portugues': u'Português (Brasil)',
             'English': u'English',
             'Espanol': u'Español',
             'Turkce': u'Türkçe',
             'Italiano': u'Italiano',
             'Arabic': u'العربية',
             'Deutsch': u'Deutsch',
             'Russian': u'Русский'}
    if config_dict['language'] in {v: k for k, v in langd.items()}:
        config_dict['language'] = {v: k for k, v in langd.items()}[config_dict['language']]
    if config_dict['language2'] in {v: k for k, v in langd.items()}:
        config_dict['language2'] = {v: k for k, v in langd.items()}[config_dict['language2']]
    if config_dict_out['language'] in {v: k for k, v in langd.items()}:
        config_dict_out['language'] = {v: k for k, v in langd.items()}[config_dict_out['language']]
    if config_dict_out['language2'] in {v: k for k, v in langd.items()}:
        config_dict_out['language2'] = {v: k for k, v in langd.items()}[config_dict_out['language2']]
    if not 'SETTINGS_v'+str(lastest_config_version) in configr.sections():
        configr.add_section('SETTINGS_v'+str(lastest_config_version))
    for opt in config_dict_out:
        set_with_comment(configr,'SETTINGS_v'+str(lastest_config_version), opt, config_dict_out[opt],comments[opt])
    with open('settings.ini', 'w') as configfile:
        configr.write(configfile)

    return config_dict


def config_v0(defult=False, **kwargs):
    dsettings = {
        'video_quality' : 'highest',
        'language' : 'English',
        'language2' : 'English',
        'forcesubtitle' : 'False',
        'forceusa' : 'False',
        'localizecookies' : 'False',
        'onlymainsub' : 'False',
        'dubfilter' : 'True',
        'connection_n_' : '1',
        'proxy' : ''
        }
    def set_with_comment(ConfigParser_obj, section, name, value='',comment=''):
        ConfigParser_obj.remove_option(section, name)
        if comment == '':
            ConfigParser_obj.set(section, name, value)
        else:
            ConfigParser_obj.set(section, '#'+comment+'\n'+name, str(value))

    comments = {
        'video_quality' : ''' Set this to the preferred quality. Possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
# Note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).
# We're not miracle workers.''',
        'language' : ''' Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option (below).
# Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch''',
        'language2' : ''' If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default''',
        'forcesubtitle' : ''' Set this if you want to use --forced-track rather than --default-track for subtitle''',
        'forceusa' : ''' Set this if you want to use a US session ID''',
        'localizecookies' : ''' Set this if you want to Localize the cookies (this option is under testing and may generate some problem and it willnot work with -forceusa- option)''',
        'onlymainsub' : ''' Set this if you only want to mux one subtitle only (this so make easy for some devices like TVs to play subtitle)''',
        'dubfilter' : ''' Set this if you autocatch dub links too''',
        'connection_n_' : ''' Set this option to increase the Number of the connection''',
        'proxy' : ''' Set this option to use proxy, example: US'''
        }
    configr = ConfigParser()
    if os.path.lexists(os.path.join('.','settings.ini')) and not defult:
        configr.read('settings.ini')
    else:
        configr.add_section('SETTINGS')
        for opt in dsettings:
            configr.set('SETTINGS', opt, dsettings[opt])
    config_dict ={}
    for opt in configr.options('SETTINGS'):
        config_dict[opt]=configr.get('SETTINGS', opt)
    boolean_list = ['forcesubtitle', 'forceusa', 'localizecookies', 'onlymainsub', 'dubfilter']
    for i in boolean_list:
        config_dict[i] = {'True': True, '1': True, 'yes': True, 'true': True, 'on': True, 'False': False, '0': False,
                               'no': False, 'false': False, 'off': False}[config_dict[i]]
    int_list = ['connection_n_']
    for i in int_list:
        config_dict[i] = int(config_dict[i])
    langd = {'Espanol_Espana': u'Español (Espana)', 'Francais': u'Français (France)',
             'Portugues': u'Português (Brasil)',
             'English': u'English', 'Espanol': u'Español', 'Turkce': u'Türkçe', 'Italiano': u'Italiano',
             'Arabic': u'العربية', 'Deutsch': u'Deutsch', 'Russian': u'Русский'}
    for kwargs_key in kwargs:
        if kwargs_key in boolean_list:
            if kwargs[kwargs_key].lower() == 'toggle'.lower():
                kwargs[kwargs_key] = not config_dict[kwargs_key]

    config_dict_out = dict(config_dict)
    config_dict['language']=langd[config_dict['language']]
    config_dict['language2'] = langd[config_dict['language2']]
        
    config_dict.update(kwargs)
    for opt in config_dict_out:
        set_with_comment(configr,'SETTINGS', opt, config_dict_out[opt],comments[opt])
    with open('settings.ini', 'w') as configfile:
        configr.write(configfile)
    return config_dict

def config_v1(defult=False, **kwargs):
    fun_ver = sys._getframe().f_code.co_name.replace('config_v','')
    dsettings = {
        'video_quality' : 'highest',
        'language' : 'English',
        'language2' : 'English',
        'forcesubtitle' : 'False',
        'forceusa' : 'False',
        'localizecookies' : 'False',
        'onlymainsub' : 'False',
        'dubfilter' : 'True',
        'connection_n_' : '1',
        'proxy' : '',
        'download_dirctory' : os.path.join('.','export')
        }

    configr = ConfigParser()
    if os.path.lexists(os.path.join('.','settings.ini')) and not defult:
        configr.read('settings.ini')
    else:
        configr.add_section('SETTINGS_v'+fun_ver)
        for opt in dsettings:
            configr.set('SETTINGS_v'+fun_ver, opt, dsettings[opt])
    config_dict ={}
    for opt in configr.options('SETTINGS_v'+fun_ver):
        config_dict[opt]=configr.get('SETTINGS_v'+fun_ver, opt)
    for opt in dsettings:
        if not opt in config_dict:
            config_dict.update({opt : dsettings[opt]})
    boolean_list = ['forcesubtitle', 'forceusa', 'localizecookies', 'onlymainsub', 'dubfilter']
    for i in boolean_list:
        config_dict[i] = {'True': True, '1': True, 'yes': True, 'true': True, 'on': True, 'False': False, '0': False,
                               'no': False, 'false': False, 'off': False}[config_dict[i]]
    int_list = ['connection_n_']
    for i in int_list:
        config_dict[i] = int(config_dict[i])
    for kwargs_key in kwargs:
        if kwargs_key in boolean_list:
            if kwargs[kwargs_key].lower() == 'toggle'.lower():
                kwargs[kwargs_key] = not config_dict[kwargs_key]
        
    config_dict.update(kwargs)
    return config_dict


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

    def close(self) -> object:
        pass



class FileAdapter(BaseAdapter):
    def send(self, request, **kwargs):
        """ Wraps a file, described in request, in a Response object.
            :param request: The PreparedRequest` being "sent".
            :returns: a Response object containing the file
        """

        # Check that the method makes sense. Only support GET
        if request.method not in ("GET", "HEAD"):
            raise ValueError("Invalid request method %s" % request.method)

        # Parse the URL
        url_parts = urlparse(request.url)

        # Reject URLs with a hostname component
        if url_parts.netloc and url_parts.netloc != "localhost":
            raise ValueError("file: URLs with hostname components are not permitted")

        resp = Response()

        # Open the file, translate certain errors into HTTP responses
        # Use urllib's unquote to translate percent escapes into whatever
        # they actually need to be
        try:
            # Split the path on / (the URL directory separator) and decode any
            # % escapes in the parts
            path_parts = [unquote(p) for p in url_parts.path.split('/')]

            # Strip out the leading empty parts created from the leading /'s
            while path_parts and not path_parts[0]:
                path_parts.pop(0)

            # If os.sep is in any of the parts, someone fed us some shenanigans.
            # Treat is like a missing file.
            if any(os.sep in p for p in path_parts):
                raise IOError(errno.ENOENT, os.strerror(errno.ENOENT))

            # Look for a drive component. If one is present, store it separately
            # so that a directory separator can correctly be added to the real
            # path, and remove any empty path parts between the drive and the path.
            # Assume that a part ending with : or | (legacy) is a drive.
            if path_parts and (path_parts[0].endswith('|') or
                               path_parts[0].endswith(':')):
                path_drive = path_parts.pop(0)
                if path_drive.endswith('|'):
                    path_drive = path_drive[:-1] + ':'

                while path_parts and not path_parts[0]:
                    path_parts.pop(0)
            else:
                path_drive = ''

            # Try to put the path back together
            # Join the drive back in, and stick os.sep in front of the path to
            # make it absolute.
            path = path_drive + os.sep + os.path.join(*path_parts)

            # Check if the drive assumptions above were correct. If path_drive
            # is set, and os.path.splitdrive does not return a drive, it wasn't
            # reall a drive. Put the path together again treating path_drive
            # as a normal path component.
            if path_drive and not os.path.splitdrive(path):
                path = os.sep + os.path.join(path_drive, *path_parts)

            # Use io.open since we need to add a release_conn method, and
            # methods can't be added to file objects in python 2.
            resp.raw = io.open(path, "rb")
            resp.raw.release_conn = resp.raw.close
        except IOError as e:
            if e.errno == errno.EACCES:
                resp.status_code = codes.forbidden
            elif e.errno == errno.ENOENT:
                resp.status_code = codes.not_found
            else:
                resp.status_code = codes.bad_request

            # Wrap the error message in a file-like object
            # The error message will be localized, try to convert the string
            # representation of the exception into a byte stream
            resp_str = str(e).encode(locale.getpreferredencoding(False))
            resp.raw = BytesIO(resp_str)
            resp.headers['Content-Length'] = len(resp_str)

            # Add release_conn to the BytesIO object
            resp.raw.release_conn = resp.raw.close
        else:
            resp.status_code = codes.ok
            resp.url = request.url

            # If it's a regular file, set the Content-Length
            resp_stat = os.fstat(resp.raw.fileno())
            if stat.S_ISREG(resp_stat.st_mode):
                resp.headers['Content-Length'] = resp_stat.st_size

        return resp

    def close(self):
        pass


def import_login_from_browser(browser = ''):
  url = 'http://www.crunchyroll.com'
  if browser.lower() == 'firfox':
    cookies_j = browser_cookie3.firefox(domain_name='.'.join(['']+urlparse(url).netloc.split('.')[-2:]))
    if len(cookies_j._cookies) == 0:
      cookies_j = browser_cookie3.firefox()
  if browser.lower() == 'chrome':
    cookies_j = browser_cookie3.chrome(domain_name='.'.join(['']+urlparse(url).netloc.split('.')[-2:]))
    if len(cookies_j._cookies) == 0:
      cookies_j = browser_cookie3.chrome()
  else:
    raise Exception('specify the browser to import login from')
  cookies = {}
  for cookie_item in cookies_j:
    cookies[cookie_item.name]=cookie_item.value
    #if cookie_item.name != 'sess_id' and cookie_item.name != 'session_id' and cookie_item.name != 'c_visitor':
    #if not cookie_item.name in ['sess_id', 'session_id', 'c_visitor', '__cf_bm', '__cfduid']:
      #cookies[cookie_item.name]=cookie_item.value
  return cookies

def update_headers(r,*arg,**kwarg):
    #print(r.status_code, r.url ,r.request.headers['Host'])
    if r.status_code == 307:
        if 'beta.crunchyroll.com' in r.url:
            r.request.headers['Host'] = 'beta.crunchyroll.com'
            r.request.headers['Referer']: 'https://beta.crunchyroll.com/'
    
def gethtml(url, req='', headers='', interpreter='nodejs', return_form='text'):
    if interpreter == 'nodejs':
        try:
            subprocess.call(['node','-v'],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            session = cloudscraper.create_scraper(interpreter=interpreter)
            #print('node is here')
        except FileNotFoundError:
            session = cloudscraper.create_scraper()
    session.mount('file://', LocalFileAdapter())
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    import_from_browser = False
    if import_from_browser:
        #if import_from_browser == 'chrome':
        #    headers = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
        #           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
        #if import_from_browser == 'firfox':
        #    headers = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
        #           'User-Agent': ''}
        browser_cookies = import_login_from_browser(import_from_browser)
        #for cookie_ in browser_cookies:
        if 'session_id' in browser_cookies:
            #session.cookies['session_id'] = browser_cookies['session_id']
            session.cookies.update(browser_cookies)
    if not 'session_id' in session.cookies:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
        session.cookies['session_id'] = cookies_.get('COOKIES', 'sess_id')
    #print(session.cookies)
    config_ = config()
    if config_['forceusa']:
        session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id_usa')
        session.cookies['session_id'] = cookies_.get('COOKIES', 'sess_id_usa')
    del session.cookies['c_visitor']
    if not config_['forceusa'] and config_['localizecookies']:
        session.cookies['c_locale'] = \
        {u'Español (Espana)': 'esES', u'Français (France)': 'frFR', u'Português (Brasil)': 'ptBR',
         u'English': 'enUS', u'Español': 'esLA', u'Türkçe': 'enUS', u'Italiano': 'itIT',
         u'العربية': 'arME', u'Deutsch': 'deDE', u'Русский': 'ruRU'}[config_['language']]

    if not urlparse(url).scheme and not urlparse(url).netloc:
        print('Apparently not a URL')
        sys.exit()
    if headers == '':
        headers = {'Referer': 'http://crunchyroll.com/', 'Host': 'www.crunchyroll.com',
                   'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
    #headers_beta = dict(headers)
    #if 'Host' in headers_beta:
    #    headers_beta['Host'] = headers_beta['Host'].replace('www.crunchyroll.com','beta.crunchyroll.com')
    try:
        #print('https://www.crunchyroll.com/beta-opt-out-survey?beta_optout=1', session.cookies)
        #session.get('https://www.crunchyroll.com/beta-opt-out-survey?beta_optout=1', headers=headers)
        #print(url, session.cookies)
        #res = session.get(url, params=req, headers=headers, allow_redirects=False)
        res = session.get(url, params=req, headers=headers, hooks={'response':update_headers})
        
    except requests.exceptions.TooManyRedirects:
        print("""Too many redirects.""")
        res = session.get(url, params=req, headers=headers, allow_redirects=False)
        print(res.status_code)
        open('Too many redirects.html','wb').write(res.content)
        raise requests.exceptions.TooManyRedirects
    res.cookies.update(session.cookies)
    #print(session.cookies)
    #print(res.cookies)
    res.encoding = 'UTF-8'
    #open('html.html','wb').write(res.content)
    if return_form == 'respond':
        return res
    else:
        return res.text


def getxml(req, med_id):
    url = 'http://www.crunchyroll.com/xml/'
    headers = {'Referer': 'http://static.ak.crunchyroll.com/versioned_assets/ChromelessPlayerApp.17821a0e.swf',
               'Host': 'www.crunchyroll.com', 'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    qualities = {'240p': ['107', '71'], '360p': ['106', '60'], '480p': ['106', '61'],
                 '720p': ['106', '62'], '1080p': ['108', '80'], 'highest': ['0', '0']}
    config_ = config()
    video_format = qualities[config_['video_quality']][0]
    resolution = qualities[config_['video_quality']][1]
    if req == 'RpcApiSubtitle_GetXml':
        payload = {'req': 'RpcApiSubtitle_GetXml', 'subtitle_script_id': med_id}
        html = gethtml(url, payload, headers)
        return html
    elif req == 'RpcApiVideoPlayer_GetStandardConfig':
        payload = {'req': 'RpcApiVideoPlayer_GetStandardConfig', 'media_id': med_id, 'video_format': video_format,
                   'video_quality': resolution, 'auto_play': '1', 'show_pop_out_controls': '1',
                   'current_page': 'http://www.crunchyroll.com/'}
        html = gethtml(url, payload, headers)
        xml_ = etree.fromstring(str.encode(html))
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

class autocatch():
    def __init__(self,url=None):
        if url is None:
            url = input(u'indicate the url :> ')
        #url ='{}{}{}'.format(*list(re.findall(r'((?:https?://)?(?:www\.)?crunchyroll\.com/)(?:[\w-]{2,5}/)?(.+?)(?=/|$)',url)[0])+['?skip_wall=1'])
        url ='{}{}{}'.format(*list(re.findall(r'((?:https?://)?(?:www\.)?crunchyroll\.com/)(?:[\w-]{2,5}/)?(series/.+?|.+?)(?=/|$)',url)[0])+['?skip_wall=1'])
        html = self.gethtml(url)
        #html_tree = etree.fromstring(html, etree.HTMLParser())

        links = self.getlinks(html)
        sortedlinks = self.sortlinks(links)
        self.choselinks(sortedlinks)
        
    def gethtml(self, URL):
        html_text = gethtml(URL)
        #html_text = open(r"D:\+Jwico\Manual & Catalog\a\l\z\project\Crunchyroll-XML-Decoder-py3-5-\crunchy-xml-decoder\military.html",'rb').read().decode()
        return html_text

    def getlinks(self,html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        links_dict = dict()
        #for dropdown in soup.find('ul',class_="list-of-seasons cf").find_all('a',class_="season-dropdown"):
        #    #print(dropdown['title'])
        #    links_dict[dropdown['title']] = list()
        #    for eps in dropdown.parent.find_all('a',class_="portrait-element")[::-1]:
        #        links_dict[dropdown['title']] += [f'http://www.crunchyroll.com{eps["href"]}']
        for season in soup.find('ul',class_="list-of-seasons cf").find_all('li',class_="season"):
            if season.find('a',class_="season-dropdown"):
                season_title = season.find('a',class_="season-dropdown")['title']
            else:
                season_title = soup.find(id="showview-content-header").find("h1").text.strip()
            links_dict[season_title] = list()
            for eps in season.find_all('a',class_="portrait-element")[::-1]:
                links_dict[season_title] += [f'http://www.crunchyroll.com{eps["href"]}']
        return links_dict

    def sortlinks(self, links_dict):
        sorted_keys = list()
        sorted_dict = list()
        sorted_dub_temp = dict()
        sorted_keys_temp = list(links_dict.keys())
        sorted_keys_temp.sort()
        for key in sorted_keys_temp:
            if not re.search(r"\((?:Russian|.+ Dub)\)",key):
                sorted_keys += [key]
        for key in sorted_keys_temp:
            check_key = re.search(r"\((?:Russian|.+ Dub)\)",key)
            if check_key:
                if not check_key.group(0) in sorted_dub_temp:
                    sorted_dub_temp[check_key.group(0)] = list()
                sorted_dub_temp[check_key.group(0)] += [key]
        for key in sorted_dub_temp:
            sorted_dub_temp[key].sort()

        for value in sorted_dub_temp.values():
            for i in value:
                sorted_keys += [i]

        for key in sorted_keys:
            sorted_dict += [(key, links_dict[key])]
        return sorted_dict

    def choselinks(self, links_dict):
        done_chossing = False
        index_chose = dict()
        while not done_chossing:
            for index_,item_ in enumerate(links_dict):
                #index_chose += [index_]
                if not index_ in index_chose:
                    index_chose[index_] = False
                pre_item = ''
                suf_item = ''
                if index_chose[index_]:
                    pre_item = '\033[30;42m'
                    suf_item = '\033[m'
                #print(item_)
                print_line =f'{index_+1} - {pre_item}{item_[0]} ({len(item_[1])} files){suf_item}'
                if 'idlelib.run' in sys.modules:
                    print_line = re.sub(r'\x1b.*?\[\d*(?:;\d*)?\w','**',print_line)
                print(print_line)
            selected_index = input(r'select which Season/Dub to autocatch(press any key to continue):>')
            
            #print(selected_index)
            if selected_index.isdigit():
                if int(selected_index)-1 in index_chose:
                    index_chose[int(selected_index)-1] = not index_chose[int(selected_index)-1]
                    print('\033[A'*(len(links_dict)+1), end='')
                    continue
            #print(index_chose)
            if not os.path.exists(r"queue.txt"):
                start_line = u'#the any line that has hash before the link will be skiped\n'
            else:
                start_line = None
            with open(r"queue.txt", "a") as queue_fp:
                if start_line:
                    queue_fp.write(start_line)
                for k,v in index_chose.items():
                    if v:
                        #print(links_dict[k][1][0])
                        for episode_link in links_dict[k][1]:
                            print(episode_link, file = queue_fp)
            done_chossing = True
	
    
    
        

        
def autocatch_old(url=None):
    if url is None:
        url = input(u'indicate the url : ')
    url = ''.join(re.findall(r'(https?://www\.crunchyroll\.com/)(?:[\w-]{2,5}/)?(.+?)(?=/|$)',url)[0])+'?skip_wall=1'
    html = gethtml(url)
    html_tree = etree.fromstring(html, etree.HTMLParser())
    if len(html_tree.xpath('//ul[@class="list-of-seasons cf"]/li')) == 1 or not config()['dubfilter']:
        episodes_link = html_tree.xpath('//ul[@class="list-of-seasons cf"]/li/ul/li/div/a/@href',
                                        namespaces={"re": "http://exslt.org/regular-expressions"})
    else:
        episodes_link = html_tree.xpath('//ul[@class="list-of-seasons cf"]/li/a[re:match(text(),"^(?:(?!Dub).)*$")]/../ul/li/div/a/@href',
                                    namespaces={"re": "http://exslt.org/regular-expressions"})
    if not os.path.exists("queue.txt"):
        take = open("queue.txt", "w")
        take.write(u'#the any line that has hash before the link will be skiped\n')
    else:
        take = open("queue.txt", "a")
    for link in episodes_link[::-1]:
        episode_link = 'http://www.crunchyroll.com'+re.findall(r'(\/[^\/]*?\/[^\/]*?)$',link)[0]
        print(episode_link, file = take)
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
        output_data_ = ''
        for i, k in enumerate(text_condition_):
            if k == 0:
                text_[i] = ''
        for i in text_:
            output_data_ += i
        loop_check_output = output_data_
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

def conver_beta_streams_to_classic(beta_dict):
    beta_streams={'streams':[],'subtitles':[],'preview':''}
    for format_k, format_v in beta_dict['streams'].items():
        for hardsub_lang_k, hardsub_lang_v in format_v.items():
            beta_streams['streams'] +=[{'format': format_k,
					'audio_lang': beta_dict['audio_locale'].replace('-',''),
					'hardsub_lang': hardsub_lang_k.replace('-','') if hardsub_lang_k != '' else None,
					'url': hardsub_lang_v['url'],
					'resolution': 'adaptive',
					'vcodec': hardsub_lang_v['vcodec']}]
    for language_k, language_v in beta_dict['subtitles'].items():
        beta_streams['subtitles'] +=[{'language': language_k.replace('-',''),
				    'url': language_v['url'],
				    'format': language_v['format']
				    }]
    return beta_streams

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def extract_streams(html_page_resp):
    media_dict =dict()
    beta_initialstate = dict()
    html_page_ = html_page_resp.text
    beta_initial_sttat_ = False
    if re.search(r'window.__INITIAL_STATE__ = ({.*})', html_page_):
        beta_initialstate = json.loads(re.findall(r'window.__INITIAL_STATE__ = ({.*})',html_page_)[0])
        if 'watch' in beta_initialstate:
            if beta_initialstate['watch']['id']:
                if beta_initialstate['watch']['id'] in beta_initialstate['content']['byId']:
                    beta_initial_sttat_ = True
            
    if re.search(r'vilos\.config\.media = ({.*})', html_page_):
        media_dict = json.loads(re.findall(r'vilos\.config\.media = ({.*})',html_page_)[0])
        media_dict['metadata']['series_title'] = json.loads(re.findall(r'vilos\.config\.analytics = ({.*})',html_page_)[0])['media_reporting_parent']['title']
    elif beta_initial_sttat_:
        media_dict['metadata']=beta_initialstate['content']['byId'][beta_initialstate['watch']['id']]['episode_metadata']
        media_dict['metadata']['title'] = beta_initialstate['content']['byId'][beta_initialstate['watch']['id']]['title']
        asset_object = requests.get(beta_initialstate['content']['byId'][beta_initialstate['watch']['id']]['playback']).json()
        media_dict.update(conver_beta_streams_to_classic(asset_object))
        
    elif re.search(r'window.__APP_CONFIG__ = ({.*})', html_page_):
        headers = {'Referer': 'https://beta.crunchyroll.com/', 'Host': 'beta-api.crunchyroll.com',
                   'User-Agent': 'Mozilla/5.0  Windows NT 6.1; rv:26.0 Gecko/20100101 Firefox/26.0'}
        beta_appconfig = json.loads(re.findall(r'window.__APP_CONFIG__ = ({.*})',html_page_)[0])
        eps_id = re.findall(r'(?:http.?://www\.|beta\.)?crunchyroll\.com/(?:.{0,2}/)?watch/(.+?)(?:/|$)',html_page_resp.url)[0]
        auth_tokens = requests.post('https://beta-api.crunchyroll.com/auth/v1/token', cookies=html_page_resp.cookies, headers=headers, data={'grant_type':'etp_rt_cookie'}, auth=HTTPBasicAuth(beta_appconfig['cxApiParams']['accountAuthClientId'], '')).json()
        #print(auth_tokens) #need to fix us
        params_data = requests.get('https://beta-api.crunchyroll.com/index/v2', headers=headers, auth=BearerAuth(auth_tokens["access_token"])).json()
        beta_objects = requests.get(f'https://beta-api.crunchyroll.com/cms/v2{params_data["cms"]["bucket"]}/objects/{eps_id}',
                                   params={'Signature': params_data["cms"]['signature'], 'Policy': params_data["cms"]['policy'], 'Key-Pair-Id': params_data["cms"]['key_pair_id']}).json()
        
        #print(beta_objects)
        media_dict['metadata']=beta_objects['items'][0]['episode_metadata']
        media_dict['metadata']['title'] = beta_objects['items'][0]['title']
        asset_object = requests.get(beta_objects['items'][0]['playback']).json()
        media_dict.update(conver_beta_streams_to_classic(asset_object))
        
        
        #pass
    else:
        raise Exception('No Media Data was found')
    media_dict['metadata']['episode_number'] = str(media_dict['metadata']['episode_number'])

    return media_dict


def vilos_subtitle(page_url_='', one_sub=None):
    print('''
------------------------------
---- Downloading Subtitle ----
------------------------------''')
    config_ = config()
    if not os.path.lexists(config_['download_dirctory']):
        os.makedirs(config_['download_dirctory'])
    if page_url_ == '':
        page_url_ = input('Please enter Crunchyroll video URL:\n')
    if not re.findall(r'(?:http.?://)?(?:www\.|beta\.)?crunchyroll\.com/(?:.{0,2}/)?(?:(?:.+/.+-|media-)\d+|watch/.+?(?:/|$))', page_url_):
        print(f"{Red_c}ERROR: Invalid URL.{Default_c}")
        exit()
    #html_page_ = gethtml(page_url_)
    #htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})', html_page_)[0])
    #htmlconfig['metadata']['series_title'] = \
    #json.loads(re.findall(r'vilos\.config\.analytics = ({.*})', html_page_)[0])['media_reporting_parent']['title']
    html_page_resp = gethtml(page_url_, return_form = 'respond')
    htmlconfig = extract_streams(html_page_resp)
    lang_iso = {'enUS' : 'English (US)', 'esLA' : u'Espa\xf1ol', 'esES' : u'Espa\xf1ol (Espa\xf1a)',
                'frFR' : u'Fran\xe7ais (France)', 'ptBR' : u'Portugu\xeas (Brasil)', 'itIT' : 'Italiano',
                'deDE' : 'Deutsch','arME' :  'العربية', 'ruRU' : 'Русский','enGB' : 'English (UK)', 'trTR':'uTürkçe'}
    lang_iso2 = {'enUS': 'eng', 'esLA': 'spa', 'esES': 'spa', 'frFR': 'fre', 'ptBR': 'por', 'itIT': 'ita',
                 'deDE': 'deu', 'arME': 'ara', 'ruRU': 'rus', 'enGB': 'eng', 'trTR': 'tur'}
    Loc_lang = {'Espanol_Espana': 'esES', 'Francais': 'frFR', 'Portugues': 'ptBR',
                'English': 'enUS', 'Espanol': 'esLA', 'Turkce': 'trTR', 'Italiano': 'itIT',
                'Arabic': 'arME', 'Deutsch': 'deDE', 'Russian': 'ruRU'}

    if one_sub is None:
        one_sub = config_['onlymainsub']
    one_sub_lang = ''
    for i in htmlconfig['subtitles']:
        if i["language"] == Loc_lang[config_['language']]:
            one_sub_lang = i["language"]
        if one_sub_lang == '':
            if i["language"] == Loc_lang[config_['language2']]:
                one_sub_lang = i["language"]
    if one_sub_lang == '':
        try:
            one_sub_lang = htmlconfig['subtitles'][0]["language"]
        except IndexError:
            print('The video has hardcoded subtitles.')

    for i in htmlconfig['subtitles']:
        if one_sub is True:
            if i["language"] != one_sub_lang:
                continue
        if htmlconfig['metadata']['episode_number'] != '':
            sub_file_ = dircheck([os.path.join(os.path.abspath(config_['download_dirctory']),''),
                                  clean_text(htmlconfig['metadata']['series_title']),
                                  ' Episode',
                                  ' - ' + clean_text(htmlconfig['metadata']['episode_number']),
                                  ' - ' + clean_text(htmlconfig['metadata']['title']),
                                  '[' + lang_iso2[i["language"]] + ']',
                                  '[' + lang_iso[i["language"]] + ']',
                                  '.ass'],
                                 ['True', 'True', 'False', 'True', 1, 'True', 'False', 'True'], 240)
        else:
            sub_file_ = dircheck([os.path.join(os.path.abspath(config_['download_dirctory']),''),
                                  clean_text(htmlconfig['metadata']['series_title']),
                                  ' - ' + clean_text(htmlconfig['metadata']['title']),
                                  '[' + lang_iso2[i["language"]] + ']',
                                  '[' + lang_iso[i["language"]] + ']',
                                  '.ass'],
                                 ['True', 'True', 1, 'True', 'False', 'True'], 240)
        try:
            print(f'Attempting to download {Green_c}{lang_iso[i["language"]]}{Default_c} subtitle...')
        except:
            print(unidecode(f'Attempting to download {Green_c}{lang_iso[i["language"]]}{Default_c} subtitle...'))
        subtitle_ = requests.get(i["url"]).content
        open(sub_file_,'wb').write(subtitle_)



#def idle_cmd_txt_fix(print_text):
#    if 'idlelib.run' in sys.modules:
#        print_text = re.sub(r'\x1b.*?\[\d*\w','',print_text)
#    return print_text

def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - ', u'”': "''", '«': '((', '»': '))', '“': "''", '>': "}", '<':'{'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))
