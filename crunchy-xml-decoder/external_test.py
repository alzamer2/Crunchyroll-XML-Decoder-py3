#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import re
import platform
import subprocess
import zipfile
import math
import importlib

try:
    from colorama import Fore, Style, init
    init()
except:
    pass

####### customs print
org_print = print
Green_c = '\x1b[32m'
Red_c = '\x1b[31m'
Default_c = '\x1b[0m'

def print_idle_cmd_txt_fix(value='', *args, **kwargs):
    if isinstance(value, str):
        if 'idlelib.run' in sys.modules:
            value = re.sub('\\x1b.*?\[\d*\w','',value)
    org_print(value, *args, **kwargs)

print = print_idle_cmd_txt_fix
#################
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
            
    information_dict = {'Python Version': [re.findall('\d\.\d\.?\d?',sys.version)[0], python_bit_],
                        'OS Version': [platform.platform().replace("-", " ")],
                        'System Type': [platform.machine()],
                        'Code Version': ['.'.join([str(i) for i in code_version[1][:2]]), str(code_version[1][2]), '(Up-To-Date)' if code_version[0] <= code_version[1] else '(Need to Update the Code)']
                        }
    for info, value in information_dict.items():
        if info == 'Code Version':
            if value[2] == '(Up-To-Date)':
                print(f'{info}={Green_c}{value[0]} rev.{value[1]}{Default_c} {value[2]}')
        else:
            print(f'{info}={Green_c}{" ".join(str(i) for i in value)}{Default_c}')
    modules_dict = {'colorama': ['Fore', 'Style', 'init'],
                    'lxml': ['etree'],
                    'wget': [None],
                    'cryptography.hazmat.primitives.ciphers': ['Cipher'],
                    'cloudscraper': [None],
                    'm3u8': [None],
                    'youtube_dl': [None],
                    'bs4': ['BeautifulSoup'],
                    'pager': ['getwidth'],
                    'unidecode': ['unidecode'],
                    'socks': [None],
                    'psutil': [None],
                    'browser_cookie3': [None],
                    }
    modules_pip_names = {'colorama': 'Colorama',
                         'cryptography.hazmat.primitives.ciphers': 'cryptography',
                         'bs4': 'beautifulsoup4',
                         'socks': 'requests[socks]'
                         }

    pip_download_ = []

    for module_name, function_names in modules_dict.items():
        try:
            module_temp = importlib.import_module(module_name)
            
            if function_names != [None]:
                for function_name in function_names:
                    if not hasattr(module_temp,function_name):
                        importlib.import_module(f'{module_name}.{function_name}')

            print(f'{module_name} : {Green_c}installed!{Default_c}')
        except ImportError:
            print(f'{module_name} : {Red_c}not installed!{Default_c}, Installing {module_name}...')
            pip_download_.append(modules_pip_names[module_name] if module_name in modules_pip_names else module_name)

    python_version_c = re.findall('(\d)\.(\d\.?\d?)',sys.version)[0]
    if pip_download_ != []:
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
        print(f"{Red_c}Can't find the crunchy-xml-decoder-py3 Folder{Default_c}")
    
    if not os.path.lexists(bin_dir__):
        os.makedirs(bin_dir__)
    exe_dict = {"mkvmerge.exe":{'32': 'https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/mkvmerge_win32.zip',
                                '64': 'https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/mkvmerge_win64.zip'},
                "ffmpeg.exe":{'32': 'https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/ffmpeg.zip',
                              '64': 'https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/ffmpeg.zip'}
                }
    for EXE in exe_dict:
        if os.path.lexists(os.path.join(bin_dir__,EXE)):
            print(f'{EXE.upper()} : {Green_c}Found!{Default_c}')
        else:
            if not 'wget' in locals():
                import wget
            print(f'{EXE.upper()} : {Red_c}not Found!{Default_c}, Downloading {EXE.upper()}...')
            if platform.machine().endswith('64'):       #64bit
                exe_url = exe_dict[EXE]['64']
            else:                                       #32bit
                exe_url = exe_dict[EXE]['32']
            wget.download(exe_url,bin_dir__)
            unzip_(os.path.join(bin_dir__,os.path.split(exe_url)[1]), bin_dir__)
            os.remove(os.path.join(bin_dir__,os.path.split(exe_url)[1]))

    #if not os.path.lexists(os.path.join(bin_dir__,"mkvmerge.exe")):
    #    if not 'wget' in locals():
    #        import wget
    #    print('{EXE} : {Red}not Found!{Default}, Downloading {EXE}...'.format(EXE = 'MKVMerge',
    #        Green = '\x1b[32m', Red = '\x1b[31m', Default = '\x1b[0m'))
    #    if platform.machine().endswith('64'):
    #        wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/mkvmerge_win64.zip',bin_dir__)
    #        unzip_(os.path.join(bin_dir__,"mkvmerge_win64.zip"), bin_dir__)
    #        os.remove(os.path.join(bin_dir__,"mkvmerge_win64.zip"))
    #    else:
    #        wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/mkvmerge_win32.zip',bin_dir__)
    #        unzip_(os.path.join(bin_dir__,"mkvmerge_win32.zip"), bin_dir__)
    #        os.remove(os.path.join(bin_dir__,"mkvmerge_win32.zip"))
    #if not os.path.lexists(os.path.join(bin_dir__,"ffmpeg.exe")):
    #    if not 'wget' in locals():
    #        import wget
    #    print('{EXE} : {Red}not Found!{Default}, Downloading {EXE}...'.format(EXE = 'FFmpeg',
    #        Green = '\x1b[32m', Red = '\x1b[31m', Default = '\x1b[0m'))
    #    wget.download('https://github.com/alzamer2/Crunchyroll-XML-Decoder-py3/releases/download/v0.0/ffmpeg.zip',bin_dir__)
    #    unzip_(os.path.join(bin_dir__,"ffmpeg.zip"), bin_dir__)
    #    os.remove(os.path.join(bin_dir__,"ffmpeg.zip"))
            

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
