#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import re
import platform

try:
    from pip._internal import main as pip_main
except:
    from pip import main as pip_main
    pip_main(['install', '--quiet', '-U', 'pip', 'wheel', 'setuptools'])
    from pip._internal import main as pip_main
try:
    from colorama import Fore, Style, init
    init()
except:
    pass
def testing_external_moudules_():
    try:
        python_bit_ = re.findall("[0-9][0-9] bit", sys.version).pop()
    except:
        if sys.maxsize > 2 ** 32:
            python_bit_ = "64 bit"
        else:
            python_bit_ = "32 bit"
    python_version_ = re.findall('\d\.\d\.?\d?',sys.version)[0]
    printidle("python version=" + '\x1b[32m' + re.findall("[0-9]\.[0-9]\.[0-9]", sys.version).pop() + " " + python_bit_ + '\x1b[0m')
    printidle("OS Version=" + '\x1b[32m' + platform.platform().replace("-", " ") + '\x1b[0m')
    #printidle("System Type=" + '\x1b[32m' + os.environ['PROCESSOR_ARCHITECTURE'] + '\x1b[0m')
    printidle("System Type=" + '\x1b[32m' + platform.machine() + '\x1b[0m')

    if os.path.exists(".\\video-engine\\rtmpdump.exe"):
        bin_dir__ = "."
    elif os.path.exists("..\\video-engine\\rtmpdump.exe"):
        bin_dir__ = ".."
    else:
        printidle("Can't find the Binary Folder")
    pip_download_ = []

    try:
        from colorama import Fore, Style, init
        init()
        printidle('Colorama : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        pip_download_.append('Colorama')
    try:
        from lxml import etree
        printidle('lxml : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('lxml : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m' + ', Installing lxml...')
        pip_download_.append('lxml')
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher
        printidle('Cryptography : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('Cryptography : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m' + ', Installing Cryptography...')
        pip_download_.append('cryptography==2.4.2')
    try:
        from cfscrape import create_scraper
        printidle('Cfscrape : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('Cfscrape : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+ ', Installing Cfscrape...')
        pip_download_.append('cfscrape')
    try:
        import m3u8
        printidle('m3u8 : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('m3u8 : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing m3u8...')
        pip_download_.append('m3u8')
    try:
        from bs4 import BeautifulSoup
        printidle('BeautifulSoup : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('BeautifulSoup : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing BeautifulSoup...')
        pip_download_.append('beautifulsoup4')
    try:
        from backports.shutil_get_terminal_size import get_terminal_size
        printidle('backports.shutil_get_terminal_size : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('backports.shutil_get_terminal_size : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing backports.shutil_get_terminal_size...')
        pip_download_.append('backports.shutil_get_terminal_size')
    try:
        from unidecode import unidecode
        printidle('Unidecode : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
    except ImportError:
        printidle('Unidecode : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing Unidecode...')
        pip_download_.append('unidecode')
    python_version_c = re.findall('(\d)\.(\d\.?\d?)',sys.version)[0]
    if int(python_version_c[0]) >= 3:
        if float(python_version_c[1]) >= 5.3:
            try:
                 from proxybroker import Broker
                 printidle('proxybroker : ' + '\x1b[32m' + 'installed!' + '\x1b[0m')
            except ImportError:
                 printidle('proxybroker : ' + '\x1b[31m' + 'not installed!' + '\x1b[0m'+', Installing proxybroker...')
                 pip_download_.append('proxybroker')
    if not pip_download_ == []:
        if not 'idlelib.run' in sys.modules:
            pip_main(['install']+pip_download_)
        else:
            pip_main(['install', '--quiet']+pip_download_)

	
def printidle(print_text, *args, **kwds):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    print(print_text, *args, **kwds)
    

if __name__ == '__main__':
    testing_external_moudules_()
