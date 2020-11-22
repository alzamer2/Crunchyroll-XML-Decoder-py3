#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Crunchyroll Export Script DX - Last Updated 2014/07/16
Removes need for rtmpExplorer
ORIGINAL SOURCE:
  http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-%28noob-friendly%29
"""

import os.path
import re
import subprocess
import sys

from altfuncs import config, clean_text, dircheck, gethtml, vilos_subtitle
from unidecode import unidecode
from hls_ import video_hls
from Dash import dash_download
from configparser import ConfigParser
import json
import m3u8
import youtube_dl
# ----------

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def ultimate(page_url='', seasonnum=0, epnum=0, sess_id_=''):

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
        page_url = input('Please enter Crunchyroll video URL:\n')
        #page_url = 'https://www.crunchyroll.com/the-rising-of-the-shield-hero/episode-11-catastrophe-returns-781158'
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

    config_ = config()
    if not os.path.lexists(config_['download_dirctory']):
        os.makedirs(config_['download_dirctory'])
    forcesub = config_['forcesubtitle']
    if sess_id_ == '':
        cookies_ = ConfigParser()
        cookies_.read('cookies')
        if config_['forceusa']:
            sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
        else:
            sess_id_ = cookies_.get('COOKIES', 'sess_id')
    media_id = re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)',page_url)[0]
    html_page_ = gethtml(page_url)
    htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})',html_page_)[0])
    htmlconfig['metadata']['series_title'] = json.loads(re.findall(r'vilos\.config\.analytics = ({.*})',html_page_)[0])['media_reporting_parent']['title']
    stream_url ={}
    stream_url_dash = {}
    for i in htmlconfig['streams']:
        if i['format'] == 'adaptive_hls':
            stream_url.update({i['hardsub_lang']:i['url']})
        elif i['format'] == 'adaptive_dash':
            stream_url_dash.update({i['hardsub_lang']:i['url']})
    if htmlconfig['metadata']['episode_number'] != '':
        title = '%s Episode %s - %s' % (htmlconfig['metadata']['series_title'],htmlconfig['metadata']['episode_number'], htmlconfig['metadata']['title'])
        title = clean_text(title)
    else:
        title = '%s - %s' % (htmlconfig['metadata']['series_title'], htmlconfig['metadata']['title'])
        title = clean_text(title)
    Loc_lang = {'Espanol_Espana': 'esES',
                'Francais': 'frFR',
                'Portugues': 'ptBR',
                'English': 'enUS',
                'Espanol': 'esLA',
                'Turkce': 'trTR',
                'Italiano': 'itIT',
                'Arabic': 'arME',
                'Deutsch': 'deDE',
                'Russian' : 'ruRU'}
    Loc_lang_1 = Loc_lang[config_['language']]
    Loc_lang_2 = Loc_lang[config_['language2']]

    if forcesub:
        try:
            hls_url = stream_url[Loc_lang_1]
            dash_url = stream_url_dash[Loc_lang_1]
        except:
            try:
                hls_url = stream_url[Loc_lang_2]
                dash_url = stream_url_dash[Loc_lang_2]
            except:
                hls_url = stream_url[None]
                dash_url = stream_url_dash[None]
                forcesub = False
    else:
        try:
            hls_url = stream_url[None]
            dash_url = stream_url_dash[None]
        except:
            try:
                hls_url = stream_url['enUS']
                dash_url = stream_url_dash['enUS']
            except:
                hls_url = stream_url[list(stream_url)[0]]
                dash_url = stream_url_dash[list(stream_url_dash)[0]]

    hls_url_m3u8 = m3u8.load(hls_url)
    hls_url_parse = {}
    dash_id_parse = {}
    for stream in hls_url_m3u8.playlists:
        hls_url_parse.update({stream.stream_info.resolution[1]: stream.absolute_uri})
    if config_['video_quality'] == '1080p':
        try:
            hls_url = hls_url_parse[1080]
        except:
            pass
    elif config_['video_quality'] == '720p':
        try:
            hls_url = hls_url_parse[720]
        except:
            pass
    elif config_['video_quality'] == '480p':
        try:
            hls_url = hls_url_parse[480]
        except:
            pass
    elif config_['video_quality'] == '360p':
        try:
            hls_url = hls_url_parse[360]
        except:
            pass
    elif config_['video_quality'] == '240p':
        try:
            hls_url = hls_url_parse[240]
        except:
            pass


    ### End stolen code ###

    # ----------
    print(format('Now Downloading - ' + title))
    if htmlconfig['metadata']['episode_number'] != '':
        video_input = dircheck([os.path.join(os.path.abspath(config_['download_dirctory']),''),
                                 clean_text(htmlconfig['metadata']['series_title']),
                                 ' Episode',
                                 ' - ' + clean_text(htmlconfig['metadata']['episode_number']),
                                 ' - ' + clean_text(htmlconfig['metadata']['title']),
                                 '.ts'],
                                 ['True', 'True', 'False', 'True', 1, 'True',], 240)
    else:
        video_input = dircheck([os.path.join(os.path.abspath(config_['download_dirctory']),''),
                                 clean_text(htmlconfig['metadata']['series_title']),
                                 ' - ' + clean_text(htmlconfig['metadata']['title']),
                                 '.ts'],
                                 ['True', 'True', 1, 'True',], 240)

    download_subprocess_result = 0
    try:
        download_ = video_hls()
        download_subprocess_result = download_.video_hls(hls_url, video_input, config_['connection_n_'])
    except AssertionError:
        download_subprocess_result = 1

    if download_subprocess_result != 0:
        try:
            print('It seem there is problem in HLS stream, will use DASH stream instead')
            download_ = dash_download()
            download_subprocess_result = download_.download(dash_url, video_input, config_['connection_n_'], r=config_['video_quality'], abr='best')
        except:
            download_subprocess_result = 1

    if download_subprocess_result != 0:
        print('It seem there is problem in DASH stream, will use External Library YoutubeDL instead')
        with youtube_dl.YoutubeDL({'logger': MyLogger()}) as ydl:
            dash_info_dict = ydl.extract_info(dash_url, download=False)
        for stream in dash_info_dict['formats']:
            if not stream['height'] == None:
                dash_id_parse.update({stream['height']: stream['format_id']})
        if config_['video_quality'] == '1080p':
            try:
                dash_video_id = dash_id_parse[1080]
            except:
                pass
        elif config_['video_quality'] == '720p':
            try:
                dash_video_id = dash_id_parse[720]
            except:
                pass
        elif config_['video_quality'] == '480p':
            try:
                dash_video_id = dash_id_parse[480]
            except:
                pass
        elif config_['video_quality'] == '360p':
            try:
                dash_video_id = dash_id_parse[360]
            except:
                pass
        elif config_['video_quality'] == '240p':
            try:
                dash_video_id = dash_id_parse[240]
            except:
                pass
        def youtube_dl_proxy(*args, **kwargs):
            import sys
            if 'idlelib.run' in sys.modules:  # code to force this script to only run in console
                try:
                    import run_code_with_console
                    return run_code_with_console.run_code_with_console()
                except:
                    pass  # end of code to force this script to only run in console
            return youtube_dl.YoutubeDL(*args, **kwargs)
            pass

        if not 'idlelib.run' in sys.modules:
            with youtube_dl.YoutubeDL(
                    {'format': dash_video_id + ',bestaudio', 'outtmpl': video_input[:-3] + '.%(ext)s'}) as ydl:
                ydl.download([dash_url])
        else:
            youtube_dl_script='''\
import youtube_dl
with youtube_dl.YoutubeDL(
                {'format': \''''+dash_video_id+''',bestaudio', 'outtmpl': r\''''+video_input[:-3]+'''\' + '.%(ext)s'}) as ydl:
                ydl.download([\'\'\''''+dash_url+'''\'\'\'])
'''
            command = 'where'  # Windows
            if os.name != "nt":  # non-Windows
                command = 'which'
            python_path_ = os.path.normpath(
                os.path.join(os.path.split(subprocess.getoutput([command, 'pip3']))[0], '..', 'python.exe'))
            try:
                subprocess.call([python_path_, '-c', youtube_dl_script])
            except FileNotFoundError:  # fix for old version windows that dont have 'where' command
                reg_ = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Python\PythonCore')
                python_request_v = [3, 0]
                if len(python_request_v) > 0:
                    if len(python_request_v) < 2:
                        python_request_v += [0]
                    python_request_v = python_request_v[0] + python_request_v[1] / 10
                else:
                    python_request_v = 0.0
                for reg_i in range(0, winreg.QueryInfoKey(reg_)[0]):
                    reg_2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Python\PythonCore')
                    if float(winreg.EnumKey(reg_2, reg_i)) >= python_request_v and \
                       True if python_request_v == 0.0 else float(winreg.EnumKey(reg_2, reg_i)) < float(
                        round(python_request_v) + 1):
                        reg_2 = winreg.OpenKey(reg_2, winreg.EnumKey(reg_2, reg_i))
                        reg_2 = winreg.OpenKey(reg_2, r'PythonPath')
                        python_path_ = os.path.normpath(
                            os.path.join(winreg.EnumValue(reg_2, 0)[1].split(';')[0], '..', 'python.exe'))
                subprocess.call([python_path_, '-c', youtube_dl_script])



    vilos_subtitle(page_url)
    mkv_merge(video_input, config_['video_quality'], 'English')

def mkv_merge(video_input,pixl,defult_lang=None, keep_files=False):
    print('Starting mkv merge')
    config_ = config()
    if defult_lang is None:
        defult_lang = config_['onlymainsub']
    if os.path.lexists(os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))
    elif os.path.lexists(os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))
    working_dir = os.path.dirname(video_input)
    working_name = os.path.splitext(os.path.basename(video_input))[0]
    filename_output = os.path.join(working_dir, working_name + '[' + pixl +'].mkv')
    exists_counter = 1
    while os.path.lexists(filename_output):
        filename_output = filename_output[:-4] + '(' + str(exists_counter) + ')' + filename_output[-4:]
        exists_counter += 1
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".ts"):
            cmd = [mkvmerge, "-o", os.path.abspath(filename_output), '--language', '0:jpn', '--language', '1:jpn',
                          '-a', '1', '-d', '0', os.path.abspath(os.path.join(working_dir, file)), '--title', working_name]
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".mp4"):
            cmd = [mkvmerge, "-o", os.path.abspath(filename_output), '--language', '0:jpn', '--language', '1:jpn',
                          '-a', '1', '-d', '0', os.path.abspath(os.path.join(working_dir, file)), '--title', working_name]
    lang_iso = {'Espanol_Espana': u'Espa\xf1ol (Espa\xf1a)',
                'Francais': u'Fran\xe7ais (France)',
                'Portugues': u'Portugu\xeas (Brasil)',
                'English': 'English (US)',
                'Espanol' : u'Espa\xf1ol',
                'Turkce': 'Türkçe',
                'Italiano': 'Italiano',
                'Arabic': 'العربية',
                'Deutsch': 'Deutsch',
                'Russian': 'Русский'
                }
    defult_lang_sub = ''
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".ass"):
            if re.findall(r'\]\[(.*)\]',file)[0] == lang_iso[config_['language']]:
                defult_lang_sub = re.findall(r'\]\[(.*)\]',file)[0]
            if defult_lang_sub == '':
                if re.findall(r'\]\[(.*)\]', file)[0] == lang_iso[config_['language2']]:
                    defult_lang_sub = re.findall(r'\]\[(.*)\]', file)[0]
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and file.endswith(".m4a"):
            cmd += ['--language', '0:jpn',
                    '--default-track', '0:yes',
                    '--forced-track', '0:yes',
                    os.path.abspath(os.path.join(working_dir, file))]
        if file.startswith(working_name) and file.endswith(".ass"):
            cmd += ['--language', '0:' + re.findall(r'\[(.*)\]\[',file)[0],
                    '--sub-charset', '0:UTF-8',
                    '--default-track', '0:yes' if re.findall(r'\]\[(.*)\]',file)[0] == defult_lang_sub else '0:no',
                    '--forced-track', '0:yes',
                    '--track-name', '0:' + re.findall(r'\]\[(.*)\]',file)[0], '-s', '0',
                    os.path.abspath(os.path.join(working_dir,file))]

    cmd_exitcode = 2
    if os.name != 'nt':
        cmd = ['wine']+cmd
    cmd_exitcode = subprocess.call(cmd)
    if cmd_exitcode != 0:
        print('fixing TS file')
        for file in os.listdir(working_dir):
            if file.startswith(working_name) and file.endswith(".ts"):
                unix_pre = []
                if os.name != 'nt':
                    unix_pre += ['wine']
                subprocess.call(unix_pre + [mkvmerge.replace('mkvmerge', 'ffmpeg'), '-i', os.path.abspath(os.path.join(working_dir, file)), '-map', '0', '-c', 'copy',
                                 '-f', 'mpegts', os.path.abspath(os.path.join(working_dir, file)).replace('.ts','_fix.ts')])
                if os.name == 'nt':
                    cmd[11] = cmd[11].replace('.ts','_fix.ts')
                else:
                    cmd[12] = cmd[12].replace('.ts','_fix.ts')
                cmd_exitcode = subprocess.call(cmd)
                
    print('Merge process complete')
    print('Starting Final Cleanup')
    if not keep_files:
        for file in os.listdir(working_dir):
            if file.startswith(working_name) and (file.endswith(".ass") or file.endswith(".m4a") or file.endswith(".mp4") or file.endswith(".ts")):
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
    ultimate(page_url, seasonnum, epnum)
    #mkv_merge('..\\export\\The Rising of the Shield Hero - 1 - The Shield Hero.ts','480p','ara')
