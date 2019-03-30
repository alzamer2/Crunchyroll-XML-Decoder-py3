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
"""
def decode_old(page_url):
    print '''
--------------------------
---- Start New Export ----
--------------------------

CrunchyRoll Downloader Toolkit DX v0.98

Crunchyroll hasn't changed anything.

If you don't have a premium account, go and sign up for one now. It's well worthit, and supports the animators.

----------
Booting up...
'''
    if page_url == '':
        page_url = raw_input('Please enter Crunchyroll video URL:\n')

    lang1, lang2, forcesub, forceusa, localizecookies, vquality, onlymainsub, connection_n_, proxy_ = altfuncs.config()
    #player_revision = altfuncs.playerrev(page_url)
    html = altfuncs.gethtml(page_url)

    #h = HTMLParser.HTMLParser()
    title = re.findall('<title>(.+?)</title>', html)[0].replace('Crunchyroll - Watch ', '')
    if len(os.path.join('export', title+'.ass')) > 255:
        title = re.findall('^(.+?) \- ', title)[0]

    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings ###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G':'a G', '*': '#', u'\u2026': '...'}

    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    title = unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], title))

    ### End stolen code ###

    media_id = page_url[-6:]
    xmlconfig = BeautifulSoup(altfuncs.getxml('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')

    try:
        if '4' in xmlconfig.find_all('code')[0]:
            print xmlconfig.find_all('msg')[0].text
            sys.exit()
    except IndexError:
        pass

    xmllist = altfuncs.getxml('RpcApiSubtitle_GetListing', media_id)
    xmllist = unidecode(xmllist).replace('><', '>\n<')



    if '<media_id>None</media_id>' in xmllist:
        print 'The video has hardcoded subtitles.'
        hardcoded = True
        sub_id = False
    else:
        try:
            sub_id2 = re.findall("id=([0-9]+)", xmllist)
            sub_id3 = re.findall("title='(\[.+\]) ", xmllist)
            sub_id4 = re.findall("title='(\[.+\]) ", xmllist)
            hardcoded = False
        except IndexError:
            print "The video's subtitles cannot be found, or are region-locked."
            hardcoded = True
            sub_id = False
    sub_id3 = [word.replace('[English (US)]','eng') for word in sub_id3]
    sub_id3 = [word.replace('[Deutsch]','deu') for word in sub_id3]
    sub_id3 = [word.replace('[Portugues (Brasil)]','por') for word in sub_id3]
    sub_id3 = [word.replace('[Francais (France)]','fre') for word in sub_id3]
    sub_id3 = [word.replace('[Espanol (Espana)]','spa') for word in sub_id3]
    sub_id3 = [word.replace('[Espanol]','spa') for word in sub_id3]
    sub_id3 = [word.replace('[Italiano]','ita') for word in sub_id3]
    sub_id3 = [word.replace('[l`rby@]','ara') for word in sub_id3]
    #sub_id4 = [word.replace('[l`rby@]',u'[العربية]') for word in sub_id4]
    sub_id4 = [word.replace('[l`rby@]',u'[Arabic]') for word in sub_id4]#else:
    #	try:
    #		sub_id = re.findall("id=([0-9]+)' title='\["+re.escape(unidecode(lang1)), xmllist)[0]
    #		hardcoded = False
    #		lang = lang1
    #	except IndexError:
    #		try:
    #			sub_id = re.findall("id=([0-9]+)' title='\["+re.escape(unidecode(lang2)), xmllist)[0]
    #			print 'Language not found, reverting to ' + lang2 + '.'
    #			hardcoded = False
    #			lang = lang2
    #		except IndexError:
    #			try:
    #				sub_id = re.findall("id=([0-9]+)' title='\[English", xmllist)[0]  # default back to English
    #				print 'Backup language not found, reverting to English.'
    #				hardcoded = False
    #				lang = 'English'
    #			except IndexError:
    #				print "The video's subtitles cannot be found, or are region-locked."
    #				hardcoded = True
    #				sub_id = False
    if not hardcoded:
        for i in sub_id2:
            #xmlsub = altfuncs.getxml('RpcApiSubtitle_GetXml', sub_id)
            xmlsub = altfuncs.getxml('RpcApiSubtitle_GetXml', i)
            formattedsubs = CrunchyDec().returnsubs(xmlsub)
            if formattedsubs is None:
                continue
            #subfile = open(eptitle + '.ass', 'wb')
            subfile = open(os.path.join('export', title+'['+sub_id3.pop(0)+']'+sub_id4.pop(0)+'.ass'), 'wb')
            subfile.write(formattedsubs.encode('utf-8-sig'))
            subfile.close()
        #shutil.move(title + '.ass', os.path.join(os.getcwd(), 'export', ''))

    print 'Subtitles for '+title+' have been downloaded'
"""
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
    lang1, lang2, forcesub, forceusa, localizecookies, vquality, onlymainsub, connection_n_, proxy_ = config()
    if argv_ == '':
        argv_ = input('Please enter Crunchyroll video URL:\n')
    #print(argv_, re.findall('https?:\/\/www\.crunchyroll\.com\/.+\/.+-(\d*)',argv_))
    if re.findall('https?:\/\/www\.crunchyroll\.com\/.+\/.+-(\d*)',argv_)==[]:
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
    media_id = re.findall('https?:\/\/www\.crunchyroll\.com\/.+\/.+-(\d*)',argv_)[0]
    #xmlconfig = BeautifulSoup(altfuncs.getxml('RpcApiVideoPlayer_GetStandardConfig', media_id), 'xml')
    xmlconfig = getxml('RpcApiVideoPlayer_GetStandardConfig', media_id)
    #print xmlconfig
    #print xmlconfig['subtitle']
    if xmlconfig['subtitle'] == []:
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
            sub_file_ = dircheck([os.path.abspath('export')+'\\',xmlconfig['media_metadata']['series_title'],' Episode',' - '+xmlconfig['media_metadata']['episode_number'],' - '+xmlconfig['media_metadata']['episode_title'],'['+lang_iso[re.findall('\[(.+)\]',i[1])[0]]+']','['+re.findall('\[(.+)\]',i[1])[0]+']','.ass'],['True','True','False','True',1,'True','False','True'],240)
            #print os.path.join('export', xmlconfig['media_metadata']['series_title'] + ' Episode ' + xmlconfig['media_metadata']['episode_number']+'['+lang_iso[re.findall('\[(.+)\]',i[1])[0]]+']['+re.findall('\[(.+)\]',i[1])[0]+'].ass')
            #xmlsub = altfuncs.getxml('RpcApiSubtitle_GetXml', sub_id)
            print("Attempting to download "+re.findall('\[(.+)\]',i[1])[0]+" subtitle...")
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
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    return print_text

if __name__ == '__main__':
    try:
        page_url = sys.argv[1]
    except IndexError:
        page_url = ''

    decode(page_url)
