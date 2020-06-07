#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
from urllib.parse import urlparse
from configparser import ConfigParser
import requests
# import cfscrape
import cloudscraper
from lxml import etree
import json
from unidecode import unidecode

from urllib.request import url2pathname
import os

from requests.adapters import BaseAdapter
from requests.compat import urlparse, unquote
from requests import Response, codes
import errno
import os
import stat
import locale
import io

#from six import BytesIO
from io import BytesIO

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
    config_dict['language']=langd[config_dict['language']]
    config_dict['language2'] = langd[config_dict['language2']]
    for kwargs_key in kwargs:
        if kwargs_key in boolean_list:
            if kwargs[kwargs_key].lower() == 'toggle'.lower():
                kwargs[kwargs_key] = not config_dict[kwargs_key]
        
    config_dict.update(kwargs)
    #print(config_dict)
    config_dict_out = dict(config_dict)
    config_dict_out['language'] = {v: k for k, v in langd.items()}[config_dict_out['language']]
    config_dict_out['language2'] = {v: k for k, v in langd.items()}[config_dict_out['language2']]
    #print(config_dict)
    for opt in config_dict_out:
        set_with_comment(configr,'SETTINGS', opt, config_dict_out[opt],comments[opt])
    with open('settings.ini', 'w') as configfile:
        configr.write(configfile)
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


def gethtml(url, req='', headers='', interpreter='nodejs'):
    # session = requests.session()
    # session = cfscrape.create_scraper()
    session = cloudscraper.create_scraper(interpreter=interpreter)
    session.mount('file://', LocalFileAdapter())
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    session.cookies['sess_id'] = cookies_.get('COOKIES', 'sess_id')
    session.cookies['session_id'] = cookies_.get('COOKIES', 'sess_id')
    #lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
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
    res = session.get(url, params=req, headers=headers)
    res.encoding = 'UTF-8'
    #print(session.get(url, params=req, headers=headers).url)
    #open('page.html', 'a',encoding='UTF-8').write(res.text)
    return res.text


def getxml(req, med_id):
    url = 'http://www.crunchyroll.com/xml/'
    headers = {'Referer': 'http://static.ak.crunchyroll.com/versioned_assets/ChromelessPlayerApp.17821a0e.swf',
               'Host': 'www.crunchyroll.com', 'Content-type': 'application/x-www-form-urlencoded',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0)'}
    qualities = {'240p': ['107', '71'], '360p': ['106', '60'], '480p': ['106', '61'],
                 '720p': ['106', '62'], '1080p': ['108', '80'], 'highest': ['0', '0']}
    #lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    config_ = config()
    video_format = qualities[config_['video_quality']][0]
    resolution = qualities[config_['video_quality']][1]
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


def autocatch(url=None):
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
    #lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    config_ = config()
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
        one_sub = config_['onlymainsub']
    #avible_sub=[]
    one_sub_lang = ''
    #print(config_)
    for i in htmlconfig['subtitles']:
        # print(i["language"], config_['language'], config_['language2'], one_sub_lang)
        # print(i["language"], Loc_lang[config_['language']],Loc_lang[config_['language2']],one_sub_lang)
        if i["language"] == Loc_lang[config_['language']]:
            one_sub_lang = i["language"]
        if one_sub_lang == '':
            if i["language"] == Loc_lang[config_['language2']]:
                one_sub_lang = i["language"]
        #avible_sub += [i["language"]]
    if one_sub_lang == '':
        try:
            one_sub_lang = htmlconfig['subtitles'][0]["language"]
        except IndexError:
            print('The video has hardcoded subtitles.')
            #exit()

    for i in htmlconfig['subtitles']:
        if one_sub is True:
            if i["language"] != one_sub_lang:
                continue
        if not htmlconfig['metadata']['episode_number'] is '':
            sub_file_ = dircheck([os.path.join(os.path.abspath('export'),''),
                                  clean_text(htmlconfig['metadata']['series_title']),
                                  ' Episode',
                                  ' - ' + clean_text(htmlconfig['metadata']['episode_number']),
                                  ' - ' + clean_text(htmlconfig['metadata']['title']),
                                  '[' + lang_iso2[i["language"]] + ']',
                                  '[' + lang_iso[i["language"]] + ']',
                                  '.ass'],
                                 ['True', 'True', 'False', 'True', 1, 'True', 'False', 'True'], 240)
        else:
            sub_file_ = dircheck([os.path.join(os.path.abspath('export'),''),
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
        print_text = re.sub(r'\x1b.*?\[\d*\w','',print_text)
    return print_text

def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - ', u'”': "''", '«': '((', '»': '))', '“': "''", '>': "}", '<':'{'}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))
