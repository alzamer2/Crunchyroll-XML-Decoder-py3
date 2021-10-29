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
import winreg
# ----------

class MyLogger(object):
    
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class Cloudflare(Exception):
    #print('Cloudflare was detected')
    #raise when Cloudflare returend
    pass

class ultimate():

    def __init__(self):
        self.intro()
        self.page_url = ''
        self.sess_id_ = ''
        self.media_id = int()
        self.config_dict = config()
        self.htmlconfig = dict()
        self.stream_url_hls = dict()
        self.stream_url_dash = dict()
        self.title = ''
        self.Loc_lang_1 = None
        self.Loc_lang_2 = None
        self.video_output = ''
        self.retries = 5

        if not os.path.lexists(self.config_dict['download_dirctory']):
            os.makedirs(self.config_dict['download_dirctory'])

    def intro(self):
        lines = ['--------------------------',
                 '---- Start New Export ----',
                 '--------------------------',
                 'CrunchyRoll Downloader Toolkit DX v0.98b',
                 "Crunchyroll hasn't changed anything.",
                 '',
                 "If you don't have a premium account, go and sign up for one now. It's well worth it, and supports the animators.",
                 '',
                 '----------',
                 'Booting up...']
        for i in lines:
            print(i)

    def download_episode(self):
        html_page_resp = gethtml(self.page_url, return_form = 'respond')

        if (html_page_resp.status_code in (403, 503, 429)  #check if Cloudflare was bypassed
        and html_page_resp.headers.get("Server", "").startswith("cloudflare")
        and (b"jschl_vc" in html_page_resp.content or b"jschl_answer" in html_page_resp.content or b"/cdn-cgi/l/chk_captcha" in html_page_resp.content)):
            raise Cloudflare('Attention Required! | Cloudflare')

        html_page_ = html_page_resp.text

        self.htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})',html_page_)[0])
        self.htmlconfig['metadata']['series_title'] = json.loads(re.findall(r'vilos\.config\.analytics = ({.*})',html_page_)[0])['media_reporting_parent']['title']

        for i in self.htmlconfig['streams']:
            if i['format'] == 'adaptive_hls' or i['format'] == 'trailer_hls':
                self.stream_url_hls.update({i['hardsub_lang']:i['url']})
            elif i['format'] == 'adaptive_dash' or i['format'] == 'trailer_dash':
                self.stream_url_dash.update({i['hardsub_lang']:i['url']})

        if self.htmlconfig['metadata']['episode_number'] != '':
            self.title = '{s_title} Episode {ep} - {ep_title}'.format(s_title=self.htmlconfig['metadata']['series_title'],
                                                                 ep=self.htmlconfig['metadata']['episode_number'],
                                                                 ep_title=self.htmlconfig['metadata']['title'])
        else:
            self.title = '{s_title} - {ep_title}'.format(s_title=self.htmlconfig['metadata']['series_title'],
                                                    ep_title=self.htmlconfig['metadata']['title'])
        self.title = clean_text(self.title)

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
        self.Loc_lang_1 = Loc_lang[self.config_dict['language']]
        self.Loc_lang_2 = Loc_lang[self.config_dict['language2']]

        if self.htmlconfig['metadata']['episode_number'] != '':
            self.video_output = dircheck([os.path.join(os.path.abspath(self.config_dict['download_dirctory']),''),
                                    clean_text(self.htmlconfig['metadata']['series_title']),
                                    ' Episode',
                                    ' - ' + clean_text(self.htmlconfig['metadata']['episode_number']),
                                    ' - ' + clean_text(self.htmlconfig['metadata']['title']),
                                    '.ts'],
                                    ['True', 'True', 'False', 'True', 1, 'True',], 240)
        else:
            self.video_output = dircheck([os.path.join(os.path.abspath(self.config_dict['download_dirctory']),''),
                                    clean_text(self.htmlconfig['metadata']['series_title']),
                                    ' - ' + clean_text(self.htmlconfig['metadata']['title']),
                                    '.ts'],
                                    ['True', 'True', 1, 'True',], 240)

        download_method = [(self.hls_download, 'HLS stream'), (self.dash_download_, 'DASH stream'), (self.youtube_dl_, 'External Library YoutubeDL')]

        #print(self.stream_url_hls)

        for download_method_run in download_method:
            download_method_run[0]()
            try:
                print(f'Now Downloading - {self.title} [{download_method_run[1]}]\n')
                download_method_run[0]()
                break
            except:
                error_line = f'It seem there is problem in {download_method_run[1]}'
                if download_method.index(download_method_run) < len(download_method)-1:
                    error_line += f', will use {download_method[download_method.index(download_method_run)+1][1]} instead'
                print(error_line)
                continue




    def hls_download(self):
        if self.config_dict['forcesubtitle']:
            if self.Loc_lang_1 in self.stream_url_hls:
                hls_url = self.stream_url_hls[self.Loc_lang_1]
            elif self.Loc_lang_2 in self.stream_url_hls:
                hls_url = self.stream_url_hls[self.Loc_lang_2]
            else:
                hls_url = self.stream_url_hls[None]
                self.config_dict['forcesubtitle'] = False
        else:
            if None in self.stream_url_hls:
                hls_url = self.stream_url_hls[None]
            elif 'enUS' in self.stream_url_hls:
                hls_url = self.stream_url_hls['enUS']
            else:
                hls_url = self.stream_url_hls[list(self.stream_url_hls)[0]]
        
        hls_url_m3u8 = m3u8.load(hls_url)
        hls_url_parse = {}
        
        for stream in hls_url_m3u8.playlists:
            hls_url_parse.update({stream.stream_info.resolution[1]: stream.absolute_uri})
        #print(self.config_dict['video_quality'])
        if re.match('\d+',self.config_dict['video_quality']):
            if int(re.match('\d+',self.config_dict['video_quality']).group(0)) in hls_url_parse:
                hls_url = hls_url_parse[int(re.match('\d+',self.config_dict['video_quality']).group(0))]
        elif self.config_dict['video_quality'].lower() in ['low', 'lowest', 'worst']:
            hls_url = hls_url_parse[min(hls_url_parse)]
        elif self.config_dict['video_quality'].lower() in ['high', '"highest" ', 'best']:
            hls_url = hls_url_parse[max(hls_url_parse)]
            

        
        download_subprocess_result = 1
        cur_retry = 1
        while cur_retry < self.retries + 1:
            #download_ = video_hls()
            #download_subprocess_result = download_.video_hls(hls_url, self.video_output, self.config_dict['connection_n_'])
            try:
                download_ = video_hls()
                download_subprocess_result = download_.video_hls(hls_url, self.video_output, self.config_dict['connection_n_'])
                #print(download_subprocess_result)
                #input()
                if download_subprocess_result == 0:
                    cur_retry = self.retries + 1
            except:
                print(f'error while downloading.......retry #{cur_retry}')
                cur_retry += 1
        

    def dash_download_(self):
        if self.config_dict['forcesubtitle']:
            if self.Loc_lang_1 in self.stream_url_dash:
                dash_url = self.stream_url_dash[self.Loc_lang_1]
            elif self.Loc_lang_2 in self.stream_url_dash:
                dash_url = self.stream_url_dash[self.Loc_lang_2]
            else:
                dash_url = self.stream_url_dash[None]
                self.config_dict['forcesubtitle'] = False
        else:
            if None in self.stream_url_dash:
                dash_url = self.stream_url_dash[None]
            elif 'enUS' in self.stream_url_dash:
                dash_url = self.stream_url_dash['enUS']
            else:
                dash_url = self.stream_url_dash[list(self.stream_url_dash)[0]]

        download_subprocess_result = 1
        cur_retry = 1
        while cur_retry < self.retries + 1:
            try:
                download_ = dash_download()
                download_subprocess_result = download_.download(dash_url, self.video_output, self.config_dict['connection_n_'], r=self.config_dict['video_quality'], abr='best')
                if download_subprocess_result == 0:
                    cur_retry = self.retries + 1
            except:
                print(f'error while downloading.......retry #{cur_retry}')
                cur_retry += 1


    def youtube_dl_(self):
        dash_id_parse = {}
        if self.config_dict['forcesubtitle']:
            if self.Loc_lang_1 in self.stream_url_dash:
                dash_url = self.stream_url_dash[self.Loc_lang_1]
            elif self.Loc_lang_2 in self.stream_url_dash:
                dash_url = self.stream_url_dash[self.Loc_lang_2]
            else:
                dash_url = self.stream_url_dash[None]
                self.config_dict['forcesubtitle'] = False
        else:
            if None in self.stream_url_dash:
                dash_url = self.stream_url_dash[None]
            elif 'enUS' in self.stream_url_dash:
                dash_url = self.stream_url_dash['enUS']
            else:
                dash_url = self.stream_url_dash[list(self.stream_url_dash)[0]]

        with youtube_dl.YoutubeDL({'logger': MyLogger()}) as ydl:
            dash_info_dict = ydl.extract_info(dash_url, download=False)
        for stream in dash_info_dict['formats']:
            if not stream['height'] == None:
                dash_id_parse.update({stream['height']: stream['format_id']})
        
        if int(re.match('\d+',self.config_dict['video_quality']).group(0)) in dash_id_parse:
            dash_video_id = dash_id_parse[int(re.match('\d+',self.config_dict['video_quality']).group(0))]

        if not 'idlelib.run' in sys.modules:
            with youtube_dl.YoutubeDL(
                    {'format': f'{dash_video_id},bestaudio', 'outtmpl': rf'{os.path.splitext(self.video_output)[0]}.%(ext)s'}) as ydl:
                ydl.download([dash_url])
        else:
            youtube_dl_script=f'''\
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import youtube_dl
with youtube_dl.YoutubeDL(
                {{'format': \'{dash_video_id},bestaudio', 'outtmpl': r\'{os.path.splitext(self.video_output)[0]}.%(ext)s'}}) as ydl:
                ydl.download([\'\'\'{dash_url}\'\'\'])
'''

            subprocess.call(['py', '-c', youtube_dl_script])
            

        



    def download(self, page_url='', sess_id_=''):
        if self.page_url == '':
            if page_url != '':
                self.page_url = page_url
            else:
                self.page_url = input('Please enter Crunchyroll video URL:>\n')

        if self.sess_id_ == '':
            if sess_id_ != '':
                self.sess_id_ = sess_id_
            else:
                cookies_ = ConfigParser()
                cookies_.read('cookies')
                if self.config_dict['forceusa']:
                    self.sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
                else:
                    self.sess_id_ = cookies_.get('COOKIES', 'sess_id')

        check_page_url = re.match(r'https?://www.crunchyroll.com/.+?/.+?-(\d+?)$',self.page_url)

        if check_page_url:
            #this is episode
            self.media_id = check_page_url[1]
            self.page_url = f'http://www.crunchyroll.com/media-{self.media_id}'
            self.download_episode()

        else:
            #this is series
            pass
        #print(self.page_url)

        vilos_subtitle(self.page_url)
        mkv_merge(self.video_output, self.config_dict['video_quality'], 'English')
        



def mkv_merge(video_input,pixl,defult_lang=None):
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
    filename_output = os.path.join(working_dir, f'{working_name}[{pixl}].mkv')
    exists_counter = 1
    while os.path.lexists(filename_output):
        filename_output = f'{os.path.splitext(filename_output)[0]}({exists_counter}){os.path.splitext(filename_output)[1]}'
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
            #print(re.findall(r'\]\[(.*)\]',file)[0], lang_iso[lang1], lang_iso[lang2], defult_lang_sub)
            if re.findall(r'\]\[(.*)\]',file)[0] == lang_iso[config_['language']]:
                defult_lang_sub = re.findall(r'\]\[(.*)\]',file)[0]
            if defult_lang_sub == '':
                if re.findall(r'\]\[(.*)\]', file)[0] == lang_iso[config_['language2']]:
                    defult_lang_sub = re.findall(r'\]\[(.*)\]', file)[0]
    #print(defult_lang_sub)
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

    #print(cmd)
    cmd_exitcode = 2
    non_windows_os_pre = []
    if os.name != 'nt':
        non_windows_os_pre = ['wine']
    cmd_exitcode = subprocess.call(non_windows_os_pre+cmd)
    if cmd_exitcode !=0:
        print('fixing TS file')
        ts_fix_cmd = [mkvmerge.replace('mkvmerge', 'ffmpeg'), '-i', cmd[11], '-map', '0', '-c', 'copy',
	                                 '-f', 'mpegts', cmd[11].replace('.ts','_fix.ts')]
        subprocess.call(non_windows_os_pre + ts_fix_cmd)
        cmd[11] = cmd[11].replace('.ts','_fix.ts')
        cmd_exitcode = subprocess.call(non_windows_os_pre+cmd)
        
    #subprocess.Popen(cmd.encode('ascii', 'surrogateescape').decode('utf-8'))
    print('Merge process complete')
    print('Starting Final Cleanup')
    #input()
    #os.remove(os.path.abspath(video_input))
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and (file.endswith(".ass") or file.endswith(".m4a") or file.endswith(".mp4") or file.endswith(".ts")):
            os.remove(os.path.abspath(os.path.join(working_dir,file)))
    

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
    input()
