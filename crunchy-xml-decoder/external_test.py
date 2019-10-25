#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import re
import platform
import subprocess
import zipfile
import math

'''
try:
    from pip._internal import main as pip_main
except:
    from pip import main as pip_main
    pip_main(['install', '--quiet', '-U', 'pip', 'wheel', 'setuptools'])
    from pip._internal import main as pip_main
'''
try:
    from colorama import Fore, Style, init
    init()
except:
    pass
def testing_external_moudules_(code_version=''):
    if code_version == '':
        from updater import get_lastest_version
        code_version = get_lastest_version()
    try:
        python_bit_ = re.findall("[0-9][0-9] bit", sys.version).pop()
    except:
        if sys.maxsize > 2 ** 32:
            python_bit_ = "64 bit"
        else:
            python_bit_ = "32 bit"
    python_version_ = re.findall('\d\.\d\.?\d?',sys.version)[0]
    print(idle_cmd_txt_fix("python version=" + '\x1b[32m' + '.'.join([str(i) for i in sys.version_info[:3]]) + " " + python_bit_ + '\x1b[0m'))
    print(idle_cmd_txt_fix("OS Version=" + '\x1b[32m' + platform.platform().replace("-", " ") + '\x1b[0m'))
    #print(idle_cmd_txt_fix("System Type=" + '\x1b[32m' + os.environ['PROCESSOR_ARCHITECTURE'] + '\x1b[0m'))
    print(idle_cmd_txt_fix("System Type=" + '\x1b[32m' + platform.machine() + '\x1b[0m'))
    print(idle_cmd_txt_fix("Code Version=" + '\x1b[32m' + '.'.join(code_version[1][:2]) + ' rev.'+ str(code_version[1][2]) + '\x1b[0m'+
                           ('\x1b[32m' +' (Up-To-Date)'+ '\x1b[0m' if code_version[0] <= code_version[1] else '\x1b[31m' +' (Need to Update the Code)'+ '\x1b[0m')))



    pip_download_ = []

    try:
        from colorama import Fore, Style, init
        init()
        print(idle_cmd_txt_fix('Colorama : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        pip_download_.append('Colorama')
    try:
        from lxml import etree
        print(idle_cmd_txt_fix('lxml : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('lxml : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m' + ', Installing lxml...'))
        pip_download_.append('lxml')
    try:
        import wget
        print(idle_cmd_txt_fix('wget : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('wget : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m' + ', Installing wget...'))
        pip_download_.append('wget')
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher
        print(idle_cmd_txt_fix('Cryptography : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('Cryptography : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m' + ', Installing Cryptography...'))
        pip_download_.append('cryptography==2.4.2')
    try:
        from cfscrape import create_scraper
        print(idle_cmd_txt_fix('Cfscrape : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('Cfscrape : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+ ', Installing Cfscrape...'))
        pip_download_.append('cfscrape')
    try:
        import m3u8
        print(idle_cmd_txt_fix('m3u8 : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('m3u8 : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing m3u8...'))
        pip_download_.append('m3u8')
    try:
        import youtube_dl
        print(idle_cmd_txt_fix('youtube_dl : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('youtube_dl : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing m3u8...'))
        pip_download_.append('youtube_dl')
    try:
        from bs4 import BeautifulSoup
        print(idle_cmd_txt_fix('BeautifulSoup : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('BeautifulSoup : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing BeautifulSoup...'))
        pip_download_.append('beautifulsoup4')
    try:
        from pager import getwidth as get_terminal_size
        print(idle_cmd_txt_fix('pager : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('pager : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing pager...'))
        pip_download_.append('pager')
    try:
        from unidecode import unidecode
        print(idle_cmd_txt_fix('Unidecode : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('Unidecode : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing Unidecode...'))
        pip_download_.append('unidecode')
    try:
        import psutil
        print(idle_cmd_txt_fix('psutil : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    except ImportError:
        print(idle_cmd_txt_fix('psutil : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing psutil...'))
        pip_download_.append('psutil')
    python_version_c = re.findall('(\d)\.(\d\.?\d?)',sys.version)[0]
    #if int(python_version_c[0]) >= 3:
    #    if float(python_version_c[1]) >= 5.3:
    #        try:
    #             from proxybroker import Broker
    #             print(idle_cmd_txt_fix('proxybroker : ' + '\x1b[32m' + 'installed!' + '\x1b[0m'))
    #        except ImportError:
    #             print(idle_cmd_txt_fix('proxybroker : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing proxybroker...'))
    #             pip_download_.append('proxybroker')
    if not pip_download_ == []:
        '''
        if not 'idlelib.run' in sys.modules:
            pip_main(['install']+pip_download_)
        else:
            pip_main(['install', '--quiet']+pip_download_)
        '''
        try:
            subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe')
                            , '-m', 'pip', 'install'] + pip_download_)
        except EnvironmentError:
            subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe')
                                , '-m', 'pip','--user', 'install'] + pip_download_)
    if os.path.lexists(os.path.join('.', 'crunchy-xml-decoder-py3.py')):
        bin_dir__ = os.path.join(".", "video-engine")
    elif os.path.lexists(os.path.join('..', 'crunchy-xml-decoder-py3.py')):
        bin_dir__ = os.path.join("..", "video-engine")
    else:
        print(idle_cmd_txt_fix('\x1b[31m'+"Can't find the crunchy-xml-decoder-py3 Folder"+'\x1b[0m'))
    if not os.path.lexists(bin_dir__):
        os.makedirs(bin_dir__)
    if not os.path.lexists(os.path.join(bin_dir__,"mkvmerge.exe")):
        import wget
        print(idle_cmd_txt_fix('mkvmerge : ' + '\x1b[31m' + 'not Found!' + '\x1b[0m'+', Downloading mkvmerge...'))
        wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/mkvmerge.zip',bin_dir__)
        unzip_(os.path.join(bin_dir__,"mkvmerge.zip"), bin_dir__)
        os.remove(os.path.join(bin_dir__,"mkvmerge.zip"))
    ## at momment rtmpdump Deprecation wil remove in the future
    '''
    if not os.path.exists(bin_dir__+"\\rtmpdump.exe"):
        import wget
        print(idle_cmd_txt_fix('rtmpdump : ' + '\x1b[31m' + 'not Found!' + '\x1b[0m'+', Downloading rtmpdump...'))
        wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/rtmpdump.zip',bin_dir__)
        unzip_(bin_dir__ + "\\rtmpdump.zip", bin_dir__)
        os.remove(bin_dir__ + "\\rtmpdump.zip")
    '''



	
def idle_cmd_txt_fix(print_text):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    return print_text

def unzip_(filename_,out):
    zf = zipfile.ZipFile(filename_)
    uncompress_size = sum((file.file_size for file in zf.infolist()))
    extracted_size = 0
    for file in zf.infolist():
        extracted_size += file.file_size
        percentage = extracted_size * 100/uncompress_size
        avail_dots = 73
        shaded_dots = int(math.floor(float(extracted_size) / uncompress_size * avail_dots))
        sys.stdout.write("\r" + '[' + '*'*shaded_dots + '-'*(avail_dots-shaded_dots) + '] %'+str(percentage))
        zf.extract(file,out)
    sys.stdout.write('\n')


if __name__ == '__main__':
    testing_external_moudules_()
