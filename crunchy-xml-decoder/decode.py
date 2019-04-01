#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Subtitle Decoder
Uses some library files from
http://xbmc-addon-repository.googlecode.com
Thanks!
"""

'''old code''' #will be deleted later on if no problem found in new code
# import lxml
#import shutil
#import HTMLParser
import sys
import warnings
from bs4 import BeautifulSoup
from unidecode import unidecode
#import cfscrape

'''new code'''
import os.path
import re


from altfuncs import config, gethtml, getxml, dircheck
from crunchyDec import CrunchyDec
import requests
from colorama import Fore, Style, init
init()

# ----------

def decode(argv_ = ''):
    print('''
--------------------------
---- Start New Export ----
--------------------------

CrunchyRoll Downloader Toolkit DX v0.98

Crunchyroll hasn't changed anything.

If you don't have a premium account, go and sign up for one now. It's well worthit, and supports the animators.

----------
Booting up...
''')
    lang, lang2, forcesub, forceusa, localizecookies, quality, onlymainsub, connection_n_, proxy_ = config()
    if argv_ == '':
        argv_ = input('Please enter Crunchyroll video URL:\n')
    #print(argv_, re.findall('https?:\/\/www\.crunchyroll\.com\/.+\/.+-(\d*)',argv_))
    if not re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)', argv_):
        print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid URL."+"\x1b[0m"))
        exit()
    #html = gethtml(argv_)
        #print str(argv_)[:15]
        
    
    #if html == '':

        #with open('.\html_ex.txt', 'r') as myfile:
        #    html = myfile.read().strip()
        #import urllib
        #html = urllib.urlopen('E:\+Jwico\Manual & Catalog\a\l\z\project\Military! Episode 1 - Watch on Crunchyroll.html').read()
     #   with open("..\..\Military! Episode 1 - Watch on Crunchyroll.html", 'r') as myfile:
     #       html = myfile.read()
        #BeautifulSoup(unicode(html, errors='ignore')).get_text()
        #html = BeautifulSoup(open('.\html_ex.txt', 'r', 'utf-8').read()).get_text()
        #print html
    '''
    title = re.findall('<title>(.+?)</title>', html)[0].replace('Crunchyroll - Watch ', '')
    title = title.replace(' - Watch on Crunchyroll', '')

    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings ###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G':'a G', '*': '#', u'\u2026': '...'}

    warnings.simplefilter("ignore")
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    title = unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], title))
    warnings.simplefilter("default")

    ### End stolen code ###

    if len(os.path.join(os.path.abspath('export'), title + '.ass')) > 255:
        eps_num = re.findall('([0-9].*?)$', title)[0]
        title = title[:246-len(os.path.join(os.path.abspath('export')))-len(eps_num)] + '~ Ep' +eps_num
	
    print os.path.join(os.path.abspath('export'), title +'.ass')
    '''
    media_id = re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)',argv_)[0]
    #xmlconfig = BeautifulSoup(altfuncs.getxml('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')
    xmlconfig = getxml('RpcApiVideoPlayer_GetStandardConfig', media_id)
    #print xmlconfig
    #print xmlconfig['subtitle']
    if not xmlconfig['subtitle']:
        print('The video has hardcoded subtitles.')
        hardcoded = True
        sub_id = False
    else:
        #lang_iso = {'English (US)':'eng',u'Espa\xc3\xb1ol':'spa',u'Espa\xc3\xb1ol (Espa\xc3\xb1a)':'spa',u'Fran\xc3\xa7ais (France)':'fre',u'Portugu\xc3\xaas (Brasil)':'por','Italiano':'ita','Deutsch':'deu'}
        #lang_iso = {'English (US)':'eng',u'Espa\xf1ol':'spa',u'Espa\xf1ol (Espa\xf1a)':'spa',u'Fran\xe7ais (France)':'fre',u'Portugu\xeas (Brasil)':'por','Italiano':'ita','Deutsch':'deu'}
        lang_iso = {'English (US)': 'eng', u'Espa\xf1ol': 'spa', u'Espa\xf1ol (Espa\xf1a)': 'spa',
                    u'Fran\xe7ais (France)': 'fre', u'Portugu\xeas (Brasil)': 'por', 'Italiano': 'ita',
                    'Deutsch': 'deu', 'العربية': 'ara','Русский':'rus'}

#    sub_id3 = [word.replace('[l`rby@]','ara') for word in sub_id3]
        for i in xmlconfig['subtitle']:
            sub_file_ = dircheck([os.path.abspath('export')+'\\',
                                  clean_text(xmlconfig['media_metadata']['series_title']),' Episode',
                                  ' - '+xmlconfig['media_metadata']['episode_number'],
                                  ' - '+clean_text(xmlconfig['media_metadata']['episode_title']),
                                  '['+lang_iso[re.findall(r'\[(.+)\]',i[1])[0]]+']',
                                  '['+re.findall(r'\[(.+)\]',i[1])[0]+']','.ass'],
                                 ['True','True','False','True',1,'True','False','True'],240)
            #print os.path.join('export', xmlconfig['media_metadata']['series_title'] + ' Episode ' + xmlconfig['media_metadata']['episode_number']+'['+lang_iso[re.findall('\[(.+)\]',i[1])[0]]+']['+re.findall('\[(.+)\]',i[1])[0]+'].ass')
            #xmlsub = altfuncs.getxml('RpcApiSubtitle_GetXml', sub_id)
            try:
                print("Attempting to download "+re.findall(r'\[(.+)\]',i[1])[0]+" subtitle...")
            except:
                print(unidecode("Attempting to download "+re.findall(r'\[(.+)\]',i[1])[0]+" subtitle..."))
            xmlsub = getxml('RpcApiSubtitle_GetXml', i[0])
            formattedsubs = CrunchyDec().returnsubs(xmlsub)
            if formattedsubs is None:
                continue
            #subfile = open(eptitle + '.ass', 'wb')
            subfile = open(sub_file_, 'wb')
            subfile.write(formattedsubs.encode('utf8'))
            subfile.close()
        

        
    
    pass
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

if __name__ == '__main__':
    try:
        page_url = sys.argv[1]
    except IndexError:
        page_url = ''

    decode(page_url)
