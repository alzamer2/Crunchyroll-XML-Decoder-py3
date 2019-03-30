#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Crunchyroll Export Script DX - Last Updated 2014/07/16
Removes need for rtmpExplorer
ORIGINAL SOURCE:
  http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-%28noob-friendly%29
"""

# import lxml
import os.path
import re
import shutil
import subprocess
import sys
import requests
#import HTMLParser

from altfuncs import config, getxml, dircheck, gethtml
from bs4 import BeautifulSoup
#from crunchyDec import CrunchyDec
from unidecode import unidecode
from hls import video_hls
from configparser import ConfigParser
from decode import decode
import json
import m3u8
# ----------

def ultimate(page_url='', seasonnum=0, epnum=0, sess_id_=''):
    #global url1, url2, filen, title, media_id, lang1, lang2, hardcoded, forceusa, page_url2, onlymainsub
    #global player_revision

    print('''
--------------------------
---- Start New Export ----
--------------------------

CrunchyRoll Downloader Toolkit DX v0.98b 

Crunchyroll hasn't changed anything.

If you don't have a premium account, go and sign up for one now. It's well worth it, and supports the animators.

----------
Booting up...
''')
    if page_url == '':
        #page_url = input('Please enter Crunchyroll video URL:\n')
        page_url = 'https://www.crunchyroll.com/the-rising-of-the-shield-hero/episode-11-catastrophe-returns-781158'
        #page_url = 'http://www.crunchyroll.com/military/episode-1-the-mission-begins-668503'
        #page_url = 'https://www.crunchyroll.com/mob-psycho-100/episode-11-guidance-psychic-sensor-780930'
	
    try:
        int(page_url)
        page_url = 'http://www.crunchyroll.com/media-' + page_url
    except ValueError:
        if not re.findall(r'https?://', page_url):
            page_url = 'http://' + page_url

        '''
        try:
            int(page_url[-6:])
        except ValueError:
            if bool(seasonnum) and bool(epnum):
                page_url = altfuncs.vidurl(page_url, seasonnum, epnum)
            elif bool(epnum):
                page_url = altfuncs.vidurl(page_url, 1, epnum)
            else:
                page_url = altfuncs.vidurl(page_url, False, False)
        '''

    # ----------

    lang1, lang2, forcesub, forceusa, localizecookies, vquality, onlymainsub, connection_n_, proxy_ = config()
    forcesub = False
    if sess_id_ == '':
        cookies_ = ConfigParser()
        cookies_.read('cookies')
        if forceusa:
            sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
        else:
            sess_id_ = cookies_.get('COOKIES', 'sess_id')
    media_id = re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)',page_url)[0]
    #htmlconfig = BeautifulSoup(gethtml(page_url), 'html')
    html_page_ = gethtml(page_url)
    #print(re.findall(r'vilos\.config\.media = ({.*})',html_page_))
    htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})',html_page_)[0])
    stream_url ={}
    for i in htmlconfig['streams']:
        stream_url.update({i['hardsub_lang']:i['url']})
    #for i in htmlconfig['subtitles']:
    #    print(i["language"], i["url"])
    #for i in stream_url:
    #    print(i, stream_url[i])
    media_info = getxml('RpcApiVideoPlayer_GetStandardConfig', media_id)
    #print(media_info)
    #print(media_info['file'])
    #print(media_info['media_metadata']['series_title'])
    #print(media_info['media_metadata']['episode_number'])
    #print(media_info['media_metadata']['episode_title'])
    title: str = '%s Episode %s - %s' % (media_info['media_metadata']['series_title'],media_info['media_metadata']['episode_number'], media_info['media_metadata']['episode_title'])
    #title: str = re.findall(r'var mediaMetadata = \{.*?name":"(.+?)",".+?\};',html_page_)[0]
    if len(os.path.join('export', title + '.flv')) > 255 or media_info['media_metadata']['episode_title'] is '':
        title: str = '%s Episode %s' % (media_info['media_metadata']['series_title'], media_info['media_metadata']['episode_number'])

    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - '}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    title = unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], title))
    Loc_lang = {u'Español (Espana)': 'esES', u'Français (France)': 'frFR', u'Português (Brasil)': 'ptBR',
            u'English': 'enUS', u'Español': 'esLA', u'Türkçe': 'trTR', u'Italiano': 'itIT',
            u'العربية': 'arME', u'Deutsch': 'deDE', u'Русский' : 'ruRU'}
    Loc_lang_1 = Loc_lang[lang1]
    Loc_lang_2 = Loc_lang[lang2]

    #print(Loc_lang_1,Loc_lang_2)
    if forcesub:
        try:
            hls_url = stream_url[Loc_lang_1]
        except:
            try:
                hls_url = stream_url[Loc_lang_2]
            except:
                hls_url = stream_url[None]
                forcesub = False
    else:
        hls_url = stream_url[None]

    #print(vquality)
    hls_url_m3u8 = m3u8.load(hls_url)
    hls_url_parse = {}
    for stream in hls_url_m3u8.playlists:
        hls_url_parse.update({stream.stream_info.resolution[1]: stream.absolute_uri})

    # for i in hls_url_parse:
    #    print(i,hls_url_parse[i])
    if vquality == '1080p':
        try:
            hls_url = hls_url_parse[1080]
        except:
            pass
    elif vquality == '720p':
        try:
            hls_url = hls_url_parse[720]
        except:
            pass
    elif vquality == '480p':
        try:
            hls_url = hls_url_parse[480]
        except:
            pass
    elif vquality == '360p':
        try:
            hls_url = hls_url_parse[360]
        except:
            pass
    elif vquality == '240p':
        try:
            #print(hls_url_parse)
            hls_url = hls_url_parse[240]
            #print(hls_url_parse[240])
        except:
            pass

    ### End stolen code ###

    # ----------
    #print(vquality,hls_url)
    print(format('Now Downloading - ' + title))
    #video_input = os.path.join("export", title + '.ts')
    video_input = dircheck([os.path.abspath('export') + '\\', media_info['media_metadata']['series_title'], ' Episode',
                          ' - ' + media_info['media_metadata']['episode_number'],
                          ' - ' + media_info['media_metadata']['episode_title'],'.ts'],
                         ['True', 'True', 'False', 'True', 1, 'True',], 240)
    video_hls(hls_url, video_input, connection_n_)
    decode(page_url)
    mkv_merge(video_input, vquality, 'eng')

def mkv_merge(video_input,pixl,defult_lang):
    print('Starting mkv merge')
    #print(os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe")))
    #print(os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe")))
    if os.path.exists(os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))
    elif os.path.exists(os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))
    #mkvmerge = os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))
    working_dir = os.path.dirname(video_input)
    working_name = os.path.splitext(os.path.basename(video_input))[0]
    filename_output = os.path.join(working_dir, working_name + '[' + pixl +'].mkv')
    cmd = [mkvmerge, "-o", os.path.abspath(filename_output), '--language', '0:jpn', '--language', '1:jpn',
           '-a', '1', '-d', '0', os.path.abspath(video_input), '--title', working_name]

    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".ass"):
            #print(os.path.abspath(os.path.join(working_dir,file)))
            cmd += ['--language', '0:' + re.findall(r'\[(.*)\]\[',file)[0],
                    '--sub-charset', '0:UTF-8',
                    '--default-track', '0:yes' if 1!=1 else '0:no',
                    '--forced-track', '0:yes',
                    '--track-name', '0:' + re.findall(r'\]\[(.*)\]',file)[0], '-s', '0',
                    os.path.abspath(os.path.join(working_dir,file))]

                #cmd.extend(['--language', '0:' + sublangc.replace('spa_spa','spa')])

                #if sublangc == sublang:
                #    cmd.extend(['--default-track', '0:yes'])
                #else:
                #    cmd.extend(['--default-track', '0:no'])
                #if forcesub:
                #    cmd.extend(['--forced-track', '0:yes'])
                #else:
                #    cmd.extend(['--forced-track', '0:no'])

                #cmd.extend(['--track-name', '0:' + sublangn])
                #cmd.extend(['-s', '0'])
                #cmd.append(filename_subtitle)
    #print(cmd)
    subprocess.call(cmd)
    #subprocess.Popen(cmd.encode('ascii', 'surrogateescape').decode('utf-8'))
    print('Merge process complete')
    print('Starting Final Cleanup')
    os.remove(os.path.abspath(video_input))
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".ass"):
            os.remove(os.path.abspath(os.path.join(working_dir,file)))
    

    

# ----------


if __name__ == '__main__':
    try:
        page_url = sys.argv[1]
    except IndexError:
        page_url = ''

    try:
        seasonnum, epnum = sys.argv[2:4]
    except ValueError:
        try:
            epnum = str(int(sys.argv[2]))
            seasonnum = ''
        except IndexError:
            # sys.exit('No season or episode numbers.')
            seasonnum, epnum = '', ''
            pass
    #ultimate(page_url, seasonnum, epnum)
    mkv_merge('..\\export\\The Rising of the Shield Hero - 1 - The Shield Hero.ts','480p','ara')
    input()
