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

from altfuncs import config, getxml, dircheck, gethtml, vilos_subtitle
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

    #lang1, lang2, forcesub, forceusa, localizecookies, vquality, onlymainsub, connection_n_, proxy_ = config()
    config_ = config()
    #print(config_)
    forcesub = config_['forcesubtitle']
    if sess_id_ == '':
        cookies_ = ConfigParser()
        cookies_.read('cookies')
        if config_['forceusa']:
            sess_id_ = cookies_.get('COOKIES', 'sess_id_usa')
        else:
            sess_id_ = cookies_.get('COOKIES', 'sess_id')
    media_id = re.findall(r'https?://www\.crunchyroll\.com/.+/.+-(\d*)',page_url)[0]
    #htmlconfig = BeautifulSoup(gethtml(page_url), 'html')
    html_page_ = gethtml(page_url)
    #print(re.findall(r'vilos\.config\.media = ({.*})',html_page_))
    htmlconfig = json.loads(re.findall(r'vilos\.config\.media = ({.*})',html_page_)[0])
    htmlconfig['metadata']['series_title'] = json.loads(re.findall(r'vilos\.config\.analytics = ({.*})',html_page_)[0])['media_reporting_parent']['title']
    stream_url ={}
    stream_url_dash = {}
    for i in htmlconfig['streams']:
        if i['format'] == 'adaptive_hls':
            stream_url.update({i['hardsub_lang']:i['url']})
        elif i['format'] == 'adaptive_dash':
            stream_url_dash.update({i['hardsub_lang']:i['url']})
        #stream_url.update({i['hardsub_lang']: i['url']})
    #for i in htmlconfig['subtitles']:
    #    print(i["language"], i["url"])
    #for i in stream_url:
    #    print(i, stream_url[i])
    #media_info = getxml('RpcApiVideoPlayer_GetStandardConfig', media_id)
    #print(media_info)
    #print(media_info['file'])
    #print(media_info['media_metadata']['series_title'])
    #print(media_info['media_metadata']['episode_number'])
    #print(media_info['media_metadata']['episode_title'])
    if not htmlconfig['metadata']['episode_number'] is '':
        title = clean_text('%s Episode %s - %s' % (htmlconfig['metadata']['series_title'],htmlconfig['metadata']['episode_number'], htmlconfig['metadata']['title']))
    else:
        title = clean_text('%s - %s' % (htmlconfig['metadata']['series_title'], htmlconfig['metadata']['title']))
    #title: str = re.findall(r'var mediaMetadata = \{.*?name":"(.+?)",".+?\};',html_page_)[0]
    #if len(os.path.join('export', title + '.flv')) > 255 or media_info['media_metadata']['episode_title'] is '':
    #    title = clean_text('%s Episode %s' % (media_info['media_metadata']['series_title'], media_info['media_metadata']['episode_number']))
    Loc_lang = {u'Español (Espana)': 'esES', u'Français (France)': 'frFR', u'Português (Brasil)': 'ptBR',
            u'English': 'enUS', u'Español': 'esLA', u'Türkçe': 'trTR', u'Italiano': 'itIT',
            u'العربية': 'arME', u'Deutsch': 'deDE', u'Русский' : 'ruRU'}
    Loc_lang_1 = Loc_lang[config_['language']]
    Loc_lang_2 = Loc_lang[config_['language2']]

    #print(Loc_lang_1,Loc_lang_2,stream_url)
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

    #print(dash_url)
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
    #print(vquality,hls_url)
    print(format('Now Downloading - ' + title))
    #video_input = os.path.join("export", title + '.ts')
    if not htmlconfig['metadata']['episode_number'] is '':
        video_input = dircheck([os.path.join(os.path.abspath('export'),''),
                                 clean_text(htmlconfig['metadata']['series_title']),
                                 ' Episode',
                                 ' - ' + clean_text(htmlconfig['metadata']['episode_number']),
                                 ' - ' + clean_text(htmlconfig['metadata']['title']),
                                 '.ts'],
                                 ['True', 'True', 'False', 'True', 1, 'True',], 240)
    else:
        video_input = dircheck([os.path.join(os.path.abspath('export'),''),
                                 clean_text(htmlconfig['metadata']['series_title']),
                                 ' - ' + clean_text(htmlconfig['metadata']['title']),
                                 '.ts'],
                                 ['True', 'True', 1, 'True',], 240)

    download_subprocess_result = 0
    try:
        # assert 1==2
        download_ = video_hls()
        download_subprocess_result = download_.video_hls(hls_url, video_input, config_['connection_n_'])
    except AssertionError:
        download_subprocess_result = 1

    if download_subprocess_result != 0:
        try:
            print('It seem there is problem in HLS stream, will use DASH stream instead')
            # assert 1==2
            download_ = dash_download()
            # print(config_['connection_n_'],config_['video_quality'])
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
        # for i in dash_info_dict['formats']:
        #    print(i['format_id'], i['ext'], i['height'], i['tbr'], i['asr'], i['language'], i['format_note'], i['filesize'],
        #          i['vcodec'], i['acodec'], i['format'])
        # for i in hls_url_parse:
        #    print(i,hls_url_parse[i])
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

        # youtube_dl_proxy({'format': dash_video_id + ',bestaudio',
        #                    'outtmpl': video_input[:-3] + '.%(ext)s'}).download([dash_url])

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
            #print(youtube_dl_script)
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


    """
    if not 'idlelib.run' in sys.modules:
        #video_hls(hls_url, video_input, config_['connection_n_'])
        try:
            #assert 1==2
            download_ = video_hls()
            download_.video_hls(hls_url, video_input, config_['connection_n_'])
        except AssertionError:
            try:
                print('It seem there is problem in HLS stream, will use DASH stream instead')
                #assert 1==2
                download_ = dash_download()
                # print(config_['connection_n_'],config_['video_quality'])
                download_.download(dash_url, video_input, config_['connection_n_'], r=config_['video_quality'], abr='best')
            except:
                print('It seem there is problem in DASH stream, will use External Library YoutubeDL instead')
                with youtube_dl.YoutubeDL({'logger': MyLogger()}) as ydl:
                    dash_info_dict = ydl.extract_info(dash_url, download=False)
                for stream in dash_info_dict['formats']:
                    if not stream['height'] == None:
                        dash_id_parse.update({stream['height']: stream['format_id']})
                # for i in dash_info_dict['formats']:
                #    print(i['format_id'], i['ext'], i['height'], i['tbr'], i['asr'], i['language'], i['format_note'], i['filesize'],
                #          i['vcodec'], i['acodec'], i['format'])
                # for i in hls_url_parse:
                #    print(i,hls_url_parse[i])
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
                with youtube_dl.YoutubeDL(
                        {'format': dash_video_id + ',bestaudio', 'outtmpl': video_input[:-3] + '.%(ext)s'}) as ydl:
                    ydl.download([dash_url])

    else:
        if os.path.lexists(os.path.abspath(os.path.join(".", "crunchy-xml-decoder", "hls.py"))):
            hls_s_path = os.path.abspath(os.path.join(".", "crunchy-xml-decoder"))
        elif os.path.lexists(os.path.abspath(os.path.join("..", "crunchy-xml-decoder", "hls.py"))):
            hls_s_path = os.path.abspath(os.path.join("..", "crunchy-xml-decoder"))
        else:
            print('hls script not found')
        hls_script = '''\
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
sys.path.append(r"''' + hls_s_path + '''")
from hls_ import video_hls

download_ = video_hls()
download_.video_hls("''' + hls_url + '''", r"''' + video_input + '''", ''' + str(config_['connection_n_']) + ''')
#video_hls("''' + hls_url + '''", r"''' + video_input + '''", ''' + str(config_['connection_n_']) + ''')'''
        # print(hls_script)
        open(os.path.join(".", "export", "hls_script_temp.py"), "w", encoding='utf-8').write(hls_script)
        hls_subprocess_result = subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe'),
                                             os.path.join(".", "export", "hls_script_temp.py")])
        if not hls_subprocess_result == 0:
            print('It seem there is problem in HLS stream, will use DASH stream instead')
            subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe'),
                             '-m','youtube_dl',
                             '-f', dash_video_id+',bestaudio',
                             '-o', video_input[:-3]+'.%(ext)s',
                             dash_url
                             ])



        os.remove(os.path.join(".", "export", "hls_script_temp.py"))
    """
    #decode(page_url)
    vilos_subtitle(page_url)
    mkv_merge(video_input, config_['video_quality'], 'English')

def mkv_merge(video_input,pixl,defult_lang=None):
    print('Starting mkv merge')
    #lang1, lang2, forcesub, forceusa, localizecookies, vquality, onlymainsub, connection_n_, proxy_ = config()
    config_ = config()
    if defult_lang is None:
        defult_lang = config_['onlymainsub']
    #print(os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe")))
    #print(os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe")))
    if os.path.lexists(os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join(".","video-engine", "mkvmerge.exe"))
    elif os.path.lexists(os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))):
        mkvmerge = os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))
    #mkvmerge = os.path.abspath(os.path.join("..","video-engine", "mkvmerge.exe"))
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
    #cmd = [mkvmerge, "-o", os.path.abspath(filename_output), '--language', '0:jpn', '--language', '1:jpn',
    #       '-a', '1', '-d', '0', os.path.abspath(video_input), '--title', working_name]
    lang_iso = {'English': 'English (US)', u'Español' : u'Espa\xf1ol', u'Español (Espana)': u'Espa\xf1ol (Espa\xf1a)',
                u'Français (France)': u'Fran\xe7ais (France)', u'Português (Brasil)': u'Portugu\xeas (Brasil)',
                u'Italiano': 'Italiano', u'Deutsch': 'Deutsch', u'العربية': 'العربية', u'Русский': 'Русский',
                u'Türkçe': 'uTürkçe'}
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
            #print(os.path.abspath(os.path.join(working_dir,file)))
            cmd += ['--language', '0:' + re.findall(r'\[(.*)\]\[',file)[0],
                    '--sub-charset', '0:UTF-8',
                    '--default-track', '0:yes' if re.findall(r'\]\[(.*)\]',file)[0] == defult_lang_sub else '0:no',
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
    if os.name == 'nt':
        subprocess.call(cmd)
    else:
        subprocess.call(['wine']+cmd)
    #subprocess.Popen(cmd.encode('ascii', 'surrogateescape').decode('utf-8'))
    print('Merge process complete')
    print('Starting Final Cleanup')
    #os.remove(os.path.abspath(video_input))
    for file in os.listdir(working_dir):
        if file.startswith(working_name) and (file.endswith(".ass") or file.endswith(".m4a") or file.endswith(".mp4") or file.endswith(".ts")):
            os.remove(os.path.abspath(os.path.join(working_dir,file)))
    
def clean_text(text_):
    ### Taken from http://stackoverflow.com/questions/6116978/python-replace-multiple-strings and improved to include the backslash###
    rep = {' / ': ' - ', '/': ' - ', ':': '-', '?': '.', '"': "''", '|': '-', '&quot;': "''", 'a*G': 'a G', '*': '#',
           r'\u2026': '...', r' \ ': ' - ', u'”': "''"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    return unidecode(pattern.sub(lambda m: rep[re.escape(m.group(0))], text_))

    

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
    input()
