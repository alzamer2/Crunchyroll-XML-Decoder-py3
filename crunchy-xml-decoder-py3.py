#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = ["Alzamer2"] #people that write and fix
__copyright__ = ""
__credits__ = __author__ + [] #__author__ + beta tester and people that repot bugs
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = ["Alzamer2"]
__email__ = "via Github"
__status__ = "Development" #Status should typically be one of "Prototype", "Development", or "Production"

'''

'''
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(IMPORTING)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
import os
import sys
from getpass import getpass
import re
import argparse
import subprocess
import textwrap


sys.path.append('crunchy-xml-decoder')

from login import login, getuserstatus
#from altfuncs import config, autocatch,vilos_subtitle
from ultimate import ultimate, mkv_merge
from pretyconsole import pmenu
import altfuncs
import debug3

try:
    from updater import get_lastest_version
    code_version = get_lastest_version()
except:
    code_version = [('0', '0', '0'), ('0', '0', '0')]
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(updating-version)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
__version__ = '%s.%s.%s' % get_lastest_version()[1]
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(CHECKING)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

if not os.path.lexists(os.path.join(".","export")):
    os.makedirs(os.path.join(".","export"))

'''
try:
    from pip._internal import main as pip_main
except:
    import pip
    pip.main(['install', '--quiet', '-U', 'pip', 'wheel', 'setuptools'])
    from pip._internal import main as pip_main
'''


from colorama import Fore, Style, init
init()

if not os.path.lexists(os.path.join('.','settings.ini')):
    altfuncs.config(defult=True)

####### customs print
org_print = print
Green_c = '\x1b[32m'
Red_c = '\x1b[31m'
Default_c = '\x1b[0m'

def print_idle_cmd_txt_fix(value='', *args, **kwargs):
    if isinstance(value, str):
        if 'idlelib.run' in sys.modules:
            value = re.sub(r'\x1b.*?\[\d*(?:;\d*)?\w','',value)
    org_print(value, *args, **kwargs)

print = print_idle_cmd_txt_fix
#################
crunchyxmldecoder_print_coding = False

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(Argument Parser)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(FUNCTION)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# def empty_function():
#     pass

def check_external_test():
    from external_test import testing_external_moudules_

    testing_external_moudules_(code_version)




def check_cookies():
    if not os.path.lexists(os.path.join('.','cookies')):
        if input(u'Do you have an account [Y/N]?').lower() == 'y':
            username = input(u'Username: ')
            password = getpass(u'Password(don\'t worry the password are typing but hidden:')
            login(username, password)
        else:
            login('', '')
# '''
        userstatus = getuserstatus()
    else:
        userstatus = getuserstatus()
        print(f'User Name = {Green_c}{userstatus[1]}{Default_c}')
        print(f'Membership Type = {Green_c}{userstatus[0]}{Default_c}')
#'''
        
def queueu(queuepath):
    if not os.path.lexists(queuepath):
        open(queuepath, 'w').write(u'#the any line that has\
                                   hash before the link will be skiped\n')
        subprocess.call(['notepad.exe',queuepath])
    queueu_running = True
    while queueu_running:
        lines = open(queuepath).readlines()
        queueu = []
        line_was_excuted = False
        for i, line in enumerate(lines):
            if line[0] != '#' and not line_was_excuted:
                #print(line.strip())
                #ultimate(line.strip(), '', '')
                ultimate_(line.strip())
                queueu = [i,  '#'+line]
                line_was_excuted = True
        if line_was_excuted:
            old_lines = open(queuepath).readlines()
            updated_lines = old_lines[:queueu[0]]+[queueu[1]]+old_lines[queueu[0]+1:]
            open(queuepath, 'w').write(''.join(updated_lines))
            continue
        else:
            break
def ultimate_(*arg,**kwarg):
    ultimate_class = ultimate()
    ultimate_class.download(*arg,**kwarg)

def coding_debug(coding_var='001111111'):
    # this is function for debuging while codine
    # it will controll which part of the code will work or not
    # 1-enable/disable external_check
    # 2-enable/disable login
    # 3-print in "crunchy-xml-decoder-py3" file
    # 4-print in "altfuncs" file
    # 5-print in "login" file
    # 6-print in "hls/dash" file
    # 7-print in "pretyconsole" file
    # 8-print in "ultimate" file
    # 9-print in "" file
    
    coding_list = list()
    for i in coding_var:
        coding_list += [int(i)]
    print(coding_list)
    if coding_list[1-1]:
        check_external_test()
    if coding_list[2-1]:
        check_cookies()
    if coding_list[3-1]:
        print('printing in crunchy-xml-decoder-py3 Enabled')
        crunchyxmldecoder_print_coding = True
    if coding_list[4-1]:
        print('printing in altfuncs Enabled')
        altfuncs.altfuncs_print_coding = True
    #altfuncs.autocatch()
    print(altfuncs.altfuncs_print_coding)
    #exit()
    menu_test.start_()

    


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MENU)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MENU)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
menu_test = pmenu()
debug_ = debug3.debug()
def load_config(**kwargs):
    for key in kwargs:
        if type(kwargs[key]) == list:
            if kwargs[key][0] == input:
                kwargs[key] = menu_test.input_pc(kwargs[key][1])
    config_ = altfuncs.config(**kwargs)
    if config_['language'] == 'العربية':
        config_['language'] = 'Arabic'
    if config_['language2'] == 'العربية':
        config_['language2'] = 'Arabic'

    menu_test.varible_pool_.update(config_)
    menu_test.redraw()

def multiitem_config_q_old(list_t=[],return_list_t=[],item__=None):
    load_config(**{'video_quality' :return_list_t[list_t.index(item__)]})
    menu_test.exit_function('vquality')


def multiitem_config_l1old(list_t=[],return_list_t=[],item__=None):
    load_config(**{'language' :return_list_t[list_t.index(item__)]})
    menu_test.exit_function('language1')

def multiitem_config_l2old(list_t=[],return_list_t=[],item__=None):
    load_config(**{'language2' :return_list_t[list_t.index(item__)]})
    menu_test.exit_function('language2')



load_config()
Title = 'CrunchyRoll Downloader Toolkit'
Subtitle = '''\
If you don't have a {Green_c}premium{Default_c} account,
go and sign up for one now. It's well worth it, and supports the animators.'''
vquality_sub = '''\
set this to the preferred quality. possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).'''
lang1_sub='''Set this to the desired subtitle language.\
If the subtitles aren\'t available in that language, it reverts to the Secondary language option'''
lang2_sub='''If the Primary language isn't available, what language would you like as a backup?\
Only if then they aren't found, then it goes to English as default'''
quality_list_ = ['240p', '360p', '480p', '720p', '1080p', 'highest']
quality_list_t = [f'{Green_c}{quality_v.replace("240p","android (240p)")}{Default_c}' for quality_v in quality_list_]

#lang_list_t = ['''\x1b[32m'''+'''English'''+'''\x1b[0m''','''\x1b[32m'''+'''Español'''+'''\x1b[0m''',
#                '''\x1b[32m'''+'''Español (Espana)'''+'''\x1b[0m''','''\x1b[32m'''+'''Français'''+'''\x1b[0m''',
#               '''\x1b[32m'''+'''Português'''+'''\x1b[0m''','''\x1b[32m'''+'''Türkçe'''+'''\x1b[0m''',
#               '''\x1b[32m'''+'''Italiano'''+'''\x1b[0m''','''\x1b[32m'''+u'''Arabic'''+'''\x1b[0m''',
#               '''\x1b[32m'''+'''Deutsch'''+'''\x1b[0m''','''\x1b[32m'''+'''Русский'''+'''\x1b[0m''']
lang_list_ = [ u'English', u'Español',u'Español (Espana)', u'Français (France)',u'Português (Brasil)',u'Türkçe',
               u'Italiano',u'العربية', u'Deutsch',u'Русский']
lang_list_t = [f'{Green_c}{lang_v.replace(u"العربية",u"العربية (Arabic)")}{Default_c}' for lang_v in lang_list_]


def multiitem_config_q_(list_t=[],return_list_t=[],item__=None):
    item__ = menu_test.run_menu('vquality')
    if not item__ is None:
        if not return_list_t == [] and len(list_t) == len(return_list_t):
            load_config(video_quality=return_list_t[list_t.index(item__)])
        else:
            load_config(video_quality=item__)

def multiitem_config_l1(list_t=[],return_list_t=[],item__=None):
    item__ = menu_test.run_menu('language1')
    if not item__ is None:
        if not return_list_t == [] and len(list_t) == len(return_list_t):
            load_config(language=return_list_t[list_t.index(item__)])
        else:
            load_config(language=item__)

def multiitem_config_l2(list_t=[],return_list_t=[],item__=None):
    item__ = menu_test.run_menu('language2')
    if not item__ is None:
        if not return_list_t == [] and len(list_t) == len(return_list_t):
            load_config(language2=return_list_t[list_t.index(item__)])
        else:
            load_config(language2=item__)

def login_t(username=None,password=None):
    newline_print=1
    print_space = ''
    if not 'idlelib.run' in sys.modules:
        print_space = ' '
    if username is None or password is None:
        newline_print=4
        menu_test.print_pc(b'\x0d'.decode()+b'\033[A'.decode()+print_space*(menu_test.get_width_()-6)+b'\x0d'.decode())
        username = menu_test.input_pc(u'Username: ')
        menu_test.print_pc(b'\x0d'.decode()+b'\033[A'.decode()*2+'Password(don\'t worry the password are typing but hidden:',end='')
        password = getpass('')
    menu_test.print_pc(b'\x0d'.decode()+b'\033[A'.decode()+print_space*(menu_test.get_width_()-6)+b'\x0d'.decode(),end='')

    #print('Login as ' + '\x1b[32m' + username + '\x1b[0m' + ' successfully.', password)
    userstatus = login(username, password)
    if username != '' and userstatus[0] == 'Guest':
        menu_test.print_commit = f'{Red_c}Login failed.{Default_c}'
    # sys.exit()
    else:
        menu_test.print_commit = f'Login as {Green_c}{userstatus[1]}{Default_c}' + ' successfully.'

    #menu_test.print_commit = 'Login as ' + '\x1b[32m' + username + '\x1b[0m' + ' successfully.'
    if not 'idlelib.run' in sys.modules:
        print('\n'*newline_print,end='')
    else:
        menu_test.print_commit=''

def autocatch_t():
    altfuncs.autocatch()
    queueu(os.path.join('.','queue.txt'))

def debug_t():
    # sys.settrace(debug3.traceit)
    debug_.debug_start()
    menu_test.print_msg = f'{Red_c}Debug is on{Default_c}>'



menu_test.main_menu_(Title,Subtitle,exit_option_call_text_='000|0|')
menu_test.add_menu_('setting', 'Settings:', exit_option_text='Back', parent_='Main')
menu_test.add_multiselection_menue_('vquality', 'Video Quality:',vquality_sub, quality_list_t,parent_='setting')
menu_test.add_multiselection_menue_('language1', 'Language:', lang1_sub, lang_list_t,parent_='setting')
menu_test.add_multiselection_menue_('language2', 'Language:', lang2_sub, lang_list_t,parent_='setting')

menu_test.add_function('Main','Download Anime',ultimate_)
menu_test.add_function('Main','Download Subtitle only',altfuncs.vilos_subtitle)
menu_test.add_function('Main','Login',login_t,reposition=True)
menu_test.add_function('Main','Login As Guest',login_t,['',''],reposition=True)
menu_test.add_function('Main','Download an entire Anime(Autocatch links)',autocatch_t)
menu_test.add_function('Main','Run Queue',queueu,[os.path.join('.','queue.txt')])
menu_test.add_space('Main')
if code_version[1] < code_version[0]:
    menu_test.add_function('Main',f'{Red_c}update{Default_c}',subprocess.call,[[sys.executable.replace('pythonw.exe', 'python.exe'),
                                                                                   os.path.join(".", "crunchy-xml-decoder", "updater.py")]],
                           call_text_='111')
else:
    menu_test.add_space('Main')

menu_test.add_function('Main','Settings',menu_test.run_menu,['setting'],call_text_='999',reposition=True)
menu_test.add_function('Main','DEBUG',debug_t,call_text_='debug',reposition=True,hidden=True)
# menu_test.add_function('Main','DEBUG',debug_.debug_start,call_text_='debug',reposition=True,hidden=True)

menu_test.add_function('setting',
                        [f'Video Quality = {Green_c}',(menu_test.varible_pool_,'video_quality'),f'{Default_c}'],
                       multiitem_config_q_,[quality_list_t,quality_list_],reposition=True)
menu_test.add_function('setting',
                        [f'Primary Language = {Green_c}',(menu_test.varible_pool_,'language'),f'{Default_c}'],
                       multiitem_config_l1,[lang_list_t,lang_list_],reposition=True)
menu_test.add_function('setting',
                        [f'Secondary Language = {Green_c}',(menu_test.varible_pool_,'language2'),f'{Default_c}'],
                       multiitem_config_l2,[lang_list_t,lang_list_],reposition=True)
menu_test.add_function('setting',
                        ['Hard Subtitle = ',(menu_test.varible_pool_,'forcesubtitle'),''' #The Video will have 1 hard subtitle'''],
                       load_config,[],{'forcesubtitle':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['USA Proxy = ',(menu_test.varible_pool_,'forceusa'),''' #use a US session ID'''],
                       load_config,[],{'forceusa':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['Localize cookies = ',(menu_test.varible_pool_,'localizecookies'),''' #Localize the cookies (Experiment)'''],
                       load_config,[],{'localizecookies':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['Only One Subtitle = ',(menu_test.varible_pool_,'onlymainsub'),''' #Only download Primary Language'''],
                       load_config,[],{'onlymainsub':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['Dub Filter = ',(menu_test.varible_pool_,'dubfilter'),''' #Ignor dub links when autocatch'''],
                       load_config,[],{'dubfilter':'toggle'},reposition=True)
menu_test.add_function('setting',
                        [f'Change the Number of The Download Connection = {Green_c}',(menu_test.varible_pool_,'connection_n_'),f'{Default_c}'],
                       load_config,[],{'connection_n_':[input,'Enter New Number of The Download Connection>>']},reposition=True)
menu_test.add_function('setting',
                        [f'use proxy(it disable if left blank)  = {Green_c}',(menu_test.varible_pool_,'proxy'),f'{Default_c}  #ex:US'],
                       load_config,[],{'proxy':[input,'Enter New proxy>>']},reposition=True)
menu_test.add_function('setting',
                        [f'Export Directory  = {Green_c}',(menu_test.varible_pool_,'download_dirctory'),f'{Default_c}'],
                       load_config,[],{'download_dirctory':[input,'Enter New Export Directory>>']},reposition=True)

menu_test.add_function('setting','Restore Default Settings',load_config,[],{'defult':True},reposition=True)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(argparse)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(argparse)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
parser = argparse.ArgumentParser(description=textwrap.dedent(f'''\
If you don't have a {Green_c}premium{Default_c} account,
go and sign up for one now. It's well worth it, and supports the animators.'''),epilog='version: '+__version__)
parser.add_argument("-d","--download", type=str, nargs = 1, metavar='URL', help="Download Crunchyroll Anime Link")
parser.add_argument("-s","--subtitle", type=str, nargs = 1, metavar='URL', help="Download Crunchyroll Anime Subtitles only")
parser.add_argument("-l","--Login", type=str, nargs = 2, metavar=('usename', 'password'), help="Login with your Crunchyroll Account")
parser.add_argument("-g","--guest", action='store_true', help="Login As Guest")
parser.add_argument("-a","--autocatch", type=str, nargs = 1, metavar='URL', help="Download an entire Anime")
parser.add_argument("-q","--queue", type=str, nargs = '?', metavar='Queue Directory', const='.\\queue.txt', help="Run List of Crunchyroll Anime Link in queue file")
parser.add_argument("-D","--default", action='store_true', help="Restore Default Settings")
parser.add_argument("--debug", action='store_true', help="Run Code in Debug Mode")
parser.add_argument("--coding", nargs='?', const='001111111', help=argparse.SUPPRESS)
arg = parser.parse_args()
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MAIN)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MAIN)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if __name__ == '__main__':
    ''' link for debug
https://www.crunchyroll.com/military/episode-1-the-mission-begins-668503
    '''
    altfuncs_print_coding = False
    #print(arg)
    if not arg.coding:
        check_external_test()
        check_cookies()
        
    
    if arg.download:
        ultimate(arg.download[0])
    elif arg.subtitle:
        altfuncs.vilos_subtitle(arg.subtitle[0])
    elif arg.Login:
        login(arg.Login[0], arg.Login[1])
    elif arg.guest:
        login('', '')
    elif arg.autocatch:
        altfuncs.autocatch(arg.autocatch[0])
        queueu(os.path.join('.', 'queue.txt'))
    elif arg.queue:
        queueu(os.path.join('.', arg.queue))
    elif arg.default:
        altfuncs.config(defult=True)
    elif arg.debug:
        debug_.debug_start()
        menu_test.print_msg = f'{Red_c}Debug is on{Default_c}>'
        menu_test.start_()
    elif arg.coding:
        coding_debug(arg.coding)
    else:
        pass#make_choise()
        menu_test.start_()
    #debug(test_)
    #print('done?')
    #input()
    # if hasattr(debug3,'debugfile'):
    #     sys.settrace(None)
    #     debug3.debugfile.close()
    debug_.debug_end()
