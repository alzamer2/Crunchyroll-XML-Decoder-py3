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

from external_test import testing_external_moudules_
try:
    from updater import get_lastest_version
    code_version = get_lastest_version()
except:
    code_version = [('0', '0', '0'), ('0', '0', '0')]
testing_external_moudules_(code_version)
from login import login, getuserstatus
from altfuncs import config, autocatch,vilos_subtitle
from ultimate import ultimate, mkv_merge
#from consolemenu import *
#from consolemenu.items import *
from pretyconsole import pmenu
import debug3

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

# iquality = 'highest'
# ilang1 = 'English'
# ilang2 = 'English'
# iforcesub = False
# iforceusa = False
# ilocalizecookies = False
# ionlymainsub = False
# idubfilter = True
# iconnection_n_ = 1
# iproxy_ = ''
# def defaultsettings(vvquality, vlang1, vlang2, vforcesub, vforceusa, vlocalizecookies, onlymainsub, vconnection_n_,vproxy_,vdubfilter):
#     dsettings='''[SETTINGS]
# # Set this to the preferred quality. Possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
# # Note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).
# # We're not miracle workers.
# video_quality = '''+vvquality+'''
# # Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option (below).
# # Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch
# language = '''+vlang1+'''
# # If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default
# language2 = '''+vlang2+'''
# # Set this if you want to use --forced-track rather than --default-track for subtitle
# forcesubtitle = '''+str(vforcesub)+'''
# # Set this if you want to use a US session ID
# forceusa = '''+str(vforceusa)+'''
# # Set this if you want to Localize the cookies (this option is under testing and may generate some problem and it willnot work with -forceusa- option)
# localizecookies = '''+str(vlocalizecookies)+'''
# # Set this if you only want to mux one subtitle only (this so make easy for some devices like TVs to play subtitle)
# onlymainsub='''+str(onlymainsub)+'''
# # Set this if you autocatch dub links too
# dubfilter='''+str(vdubfilter)+'''
# # Set this option to increase the Number of the connection
# connection_n_='''+str(vconnection_n_)+'''
# # Set this option to use proxy, example: US
# Proxy = '''+vproxy_+'''
# '''
#     open(os.path.join('.','settings.ini'), 'w', encoding='utf8').write(dsettings)

if not os.path.lexists(os.path.join('.','settings.ini')):
    load_config()
    #defaultsettings(iquality, ilang1, ilang2, iforcesub, iforceusa, ilocalizecookies, ionlymainsub, iconnection_n_, iproxy_, idubfilter)

def idle_cmd_txt_fix(print_text):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    return print_text

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
    print(idle_cmd_txt_fix('User Name = ' + '\x1b[32m' + userstatus[1] + '\x1b[0m'))
    print(idle_cmd_txt_fix('Membership Type = ' + '\x1b[32m' +userstatus[0] + '\x1b[0m'))
#'''

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(Argument Parser)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(FUNCTION)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# def empty_function():
#     pass

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
                ultimate(line.strip(), '', '')
                queueu = [i,  '#'+line]
                line_was_excuted = True
        if line_was_excuted:
            old_lines = open(queuepath).readlines()
            updated_lines = old_lines[:queueu[0]]+[queueu[1]]+old_lines[queueu[0]+1:]
            open(queuepath, 'w').write(''.join(updated_lines))
            continue
        else:
            break

# def Languages_(Varname_):
#     while True:
#         seleccion = 0
#         if Varname_ == 'slang1':
#             print(idle_cmd_txt_fix('''Set this to the desired subtitle language. If the subtitles aren\'t available in that language, it reverts to the Secondary language option'''))
#         if Varname_ == 'slang2':
#             print(idle_cmd_txt_fix('''If the Primary language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default'''))
#         try:
#             print(idle_cmd_txt_fix('''Available Languages:
# 0.- '''+'''\x1b[32m'''+'''English'''+'''\x1b[0m'''+'''
# 1.- '''+'''\x1b[32m'''+'''Espanol'''+'''\x1b[0m'''+'''
# 2.- '''+'''\x1b[32m'''+'''Espanol (Espana)'''+'''\x1b[0m'''+'''
# 3.- '''+'''\x1b[32m'''+'''Francais'''+'''\x1b[0m'''+'''
# 4.- '''+'''\x1b[32m'''+'''Portugues'''+'''\x1b[0m'''+'''
# 5.- '''+'''\x1b[32m'''+'''Turkce'''+'''\x1b[0m'''+'''
# 6.- '''+'''\x1b[32m'''+'''Italiano'''+'''\x1b[0m'''+'''
# 7.- '''+'''\x1b[32m'''+'''Arabic'''+'''\x1b[0m'''+'''
# 8.- '''+'''\x1b[32m'''+'''Deutsch'''+'''\x1b[0m'''+'''
# 9.- '''+'''\x1b[32m'''+'''Russian'''+'''\x1b[0m'''))
#             seleccion = int(input('> '))
#         except:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue
#         if seleccion == 1 :
#             return 'Espanol'
#         elif seleccion == 2 :
#             return 'Espanol_Espana'
#         elif seleccion == 3 :
#             return 'Francais'
#         elif seleccion == 4 :
#             return 'Portugues'
#         elif seleccion == 5 :
#             return 'Turkce'
#         elif seleccion == 6 :
#             return 'Italiano'
#         elif seleccion == 7 :
#             return 'Arabic'
#         elif seleccion == 8 :
#             return 'Deutsch'
#         elif seleccion == 9 :
#             return 'Russian'
#         elif seleccion == 0 :
#             return 'English'
#         else:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue

# def videoquality_():
#     while True:
#         vquality = config()['video_quality']
#         seleccion = 5
#         try:
#             print(idle_cmd_txt_fix('''Set This To The Preferred Quality:
# 0.- '''+'''\x1b[32m'''+'''android (240p)'''+'''\x1b[0m'''+'''
# 1.- '''+'''\x1b[32m'''+'''360p'''+'''\x1b[0m'''+'''
# 2.- '''+'''\x1b[32m'''+'''480p'''+'''\x1b[0m'''+'''
# 3.- '''+'''\x1b[32m'''+'''720p'''+'''\x1b[0m'''+'''
# 4.- '''+'''\x1b[32m'''+'''1080p'''+'''\x1b[0m'''+'''
# 5.- '''+'''\x1b[32m'''+'''highest'''+'''\x1b[0m'''+'''
# Note: Any Quality Higher Than 360p Still Requires Premium, Unless It's Available That Way For Free (Some First Episodes).
# We're Not Miracle Workers.'''))
#             seleccion = int(input('> '))
#         except:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue
#         if seleccion == 0 :
#             return '240p'
#         elif seleccion == 1 :
#             return '360p'
#         elif seleccion == 2 :
#             return '480p'
#         elif seleccion == 3 :
#             return '720p'
#         elif seleccion == 4 :
#             return '1080p'
#         elif seleccion == 5 :
#             return 'highest'
#         else:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue

# def settings_():
#     while True:
#         #slang1, slang2, sforcesub, sforceusa, slocalizecookies, vquality, vonlymainsub, vconnection_n_,vproxy_ = config()
#         config_ = config()
#         slang1 = config_['language']
#         slang2 = config_['language2']
#         sforcesub = config_['forcesubtitle']
#         sforceusa = config_['forceusa']
#         slocalizecookies = config_['localizecookies']
#         vquality = config_['video_quality']
#         vonlymainsub = config_['onlymainsub']
#         vconnection_n_ = config_['connection_n_']
#         vproxy_ = config_['proxy']
#         vdubfilter = config_['dubfilter']
#         slang1 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
#             u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
#             u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang1]
#         slang2 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
#             u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
#             u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang2]
#         if slang1 == 'Espanol_Espana':
#             slang1_ = 'Espanol (Espana)'
#         else:
#             slang1_ = slang1
#         if slang2 == 'Espanol_Espana':
#             slang2_ = 'Espanol (Espana)'
#         else:
#             slang2_ = slang2
#         seleccion = 0
#         try:
#             print(idle_cmd_txt_fix('''Options:
# 0.- Exit
# 1.- Video Quality = \x1b[32m'''+vquality+'''\x1b[0m
# 2.- Primary Language = \x1b[32m'''+slang1_+'''\x1b[0m
# 3.- Secondary Language = \x1b[32m'''+slang2_+'''\x1b[0m
# 4.- Hard Subtitle = '''+('\x1b[32m'+str(sforcesub)+'\x1b[0m' if sforcesub else '\x1b[31m'+str(sforcesub)+'\x1b[0m')+'''		#The Video will have 1 hard subtitle
# 5.- USA Proxy = '''+('\x1b[32m'+str(sforceusa)+'\x1b[0m' if sforceusa else '\x1b[31m'+str(sforceusa)+'\x1b[0m')+'''			#use a US session ID
# 6.- Localize cookies = '''+('\x1b[32m'+str(slocalizecookies)+'\x1b[0m' if slocalizecookies else '\x1b[31m'+str(slocalizecookies)+'\x1b[0m')+'''		#Localize the cookies (Experiment)
# 7.- Only One Subtitle = '''+('\x1b[32m'+str(vonlymainsub)+'\x1b[0m' if vonlymainsub else '\x1b[31m'+str(vonlymainsub)+'\x1b[0m')+'''		#Only download Primary Language
# 8.- Dub Filter = '''+('\x1b[32m'+str(vdubfilter)+'\x1b[0m' if vdubfilter else '\x1b[31m'+str(vdubfilter)+'\x1b[0m')+'''		#Ignor dub links when autocatch
# 9.- Change the Number of The Download Connection = \x1b[32m'''+str(vconnection_n_)+'''\x1b[0m
# 10.- use proxy(it disable if left blank)  = \x1b[32m'''+vproxy_+''' \x1b[0m  #ex:US
# 11.- Restore Default Settings
# > '''))
#             seleccion = int(input('> '))
#         except:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue
#         if seleccion == 1 :
#             vquality = videoquality_()
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 2 :
#             slang1 = Languages_('slang1')
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 3 :
#             slang2 = Languages_('slang2')
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 4 :
#             if sforcesub:
#                 sforcesub = False
#             else:
#                 sforcesub = True
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 5 :
#             if sforceusa:
#                 sforceusa = False
#             else:
#                 sforceusa = True
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 6 :
#             if slocalizecookies:
#                 slocalizecookies = False
#             else:
#                 slocalizecookies = True
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 7 :
#             if vonlymainsub:
#                 vonlymainsub = False
#             else:
#                 vonlymainsub = True
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 8 :
#             if vdubfilter:
#                 vdubfilter = False
#             else:
#                 vdubfilter = True
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 9 :
#             vconnection_n_ = input(u'Please Input The Download Connection Nymber: ')
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             continue
#         elif seleccion == 10 :
#             vproxy_ = input(u'Please Input The Proxy: ')
#             defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
#             getuserstatus(True)
#             continue
#         elif seleccion == 11 :
#             defaultsettings(iquality, ilang1, ilang2, iforcesub, iforceusa, ilocalizecookies, ionlymainsub, iconnection_n_, iproxy_, idubfilter)
#             continue
#         elif seleccion == 0 :
#             break
#         else:
#             print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
#             continue
#
# def make_choise():
#     #seleccion = 0
#     while True:
#         print(idle_cmd_txt_fix('''Options:
# 1.- Download Anime
# 2.- Download Subtitle only
# 3.- Login
# 4.- Login As Guest
# 5.- Download an entire Anime(Autocatch links)
# 6.- Run Queue
# '''+('\n111.- '+'\x1b[31m'+'update'+ '\x1b[0m' if code_version[1] < code_version[0] else '\n')+'''
# 999.- Settings
# 000.- Exit'''))
#         seleccion = input('> ')
#         if seleccion == '':
#             break
#         elif not seleccion.isdigit():
#             print(idle_cmd_txt_fix('\x1b[31m' + 'Invalid Input!' + '\x1b[0m'))
#             continue
#         elif int(seleccion) == 0:
#             break
#         elif int(seleccion) == 1:
#             ultimate()
#             #mkv_merge('.\export\\The Rising of the Shield Hero - 1 - The Shield Hero.ts','480p','ara')
#             pass
#         elif int(seleccion) == 2:
#             #decode('http://www.crunchyroll.com/military/episode-1-the-mission-begins-668503')
#             #decode(input('Please enter Crunchyroll video URL:\n'))
#             vilos_subtitle(input('Please enter Crunchyroll video URL:\n'))
#             pass
#         elif int(seleccion) == 3:
#             username = input(u'Username: ')
#             password = getpass('Password(don\'t worry the password are typing but hidden:')
#             login(username, password)
#             continue
#         elif int(seleccion) == 4:
#             login('', '')
#             continue
#         elif int(seleccion) == 5:
#             #pass
#             autocatch()
#             queueu(os.path.join('.','queue.txt'))
#         elif int(seleccion) == 6:
#             queueu(os.path.join('.','queue.txt'))
#         elif int(seleccion) == 111:
#             subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe'),
#                              os.path.join(".", "crunchy-xml-decoder", "updater.py")])
#         elif int(seleccion) == 999:
#             settings_()
#         else:
#             print(idle_cmd_txt_fix('\x1b[31m' + 'Invalid Input!' + '\x1b[0m'))
#             continue
#
#
#
# def debug(func, *args, **kwds):
#     import trace ##debug
#     # create a Trace object, telling it what to ignore, and whether to
#     # do tracing or line-counting or both.
#     tracer = trace.Trace(
#         ignoredirs=[sys.prefix, sys.exec_prefix],
#         trace=1,
#         count=1)
#     # run the new command using the given tracer
#     tracer.runfunc(func, *args, **kwds)
#     # make a report, placing output in the current directory
#     r = tracer.results()
#     r.write_results(show_missing=True, coverdir=".")
#
# def test_():
#     for i in [1,2,3]:
#         print(i)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MENU)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MENU)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
menu_test = pmenu()
debug_ = debug3.debug()
def load_config(**kwargs):
    for key in kwargs:
        if type(kwargs[key]) == list:
            if kwargs[key][0] == input:
                kwargs[key] = menu_test.input_pc(kwargs[key][1])
    config_ = config(**kwargs)
    # print(config_)
    #if config_['language'] == 'Espanol_Espana':
        # config_['language'] = 'Espanol (Espana)'
    # if config_['language2'] == 'Espanol_Espana':
    #     config_['language2'] = 'Espanol (Espana)'
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
If you don't have a \x1b[32mpremium\x1b[0m account,
go and sign up for one now. It's well worth it, and supports the animators.'''
vquality_sub = '''\
set this to the preferred quality. possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).'''
lang1_sub='''Set this to the desired subtitle language.\
If the subtitles aren\'t available in that language, it reverts to the Secondary language option'''
lang2_sub='''If the Primary language isn't available, what language would you like as a backup?\
Only if then they aren't found, then it goes to English as default'''
quality_list_t = ['''\x1b[32m'''+'''android (240p)'''+'''\x1b[0m''','''\x1b[32m'''+'''360p'''+'''\x1b[0m''',
                '''\x1b[32m'''+'''480p'''+'''\x1b[0m''','''\x1b[32m'''+'''720p'''+'''\x1b[0m''',
                '''\x1b[32m'''+'''1080p'''+'''\x1b[0m''','''\x1b[32m'''+'''highest'''+'''\x1b[0m''']
quality_list_ = ['240p', '360p', '480p', '720p', '1080p', 'highest']
lang_list_t = ['''\x1b[32m'''+'''English'''+'''\x1b[0m''','''\x1b[32m'''+'''Español'''+'''\x1b[0m''',
                '''\x1b[32m'''+'''Español (Espana)'''+'''\x1b[0m''','''\x1b[32m'''+'''Français'''+'''\x1b[0m''',
               '''\x1b[32m'''+'''Português'''+'''\x1b[0m''','''\x1b[32m'''+'''Türkçe'''+'''\x1b[0m''',
               '''\x1b[32m'''+'''Italiano'''+'''\x1b[0m''','''\x1b[32m'''+u'''Arabic'''+'''\x1b[0m''',
               '''\x1b[32m'''+'''Deutsch'''+'''\x1b[0m''','''\x1b[32m'''+'''Русский'''+'''\x1b[0m''']
lang_list_ = [ u'English', u'Español',u'Español (Espana)', u'Français (France)',u'Português (Brasil)',u'Türkçe',
               u'Italiano',u'العربية', u'Deutsch',u'Русский']


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
        menu_test.print_pc(idle_cmd_txt_fix(b'\x0d'.decode()+b'\033[A'.decode()+print_space*(menu_test.get_width_()-6)+b'\x0d'.decode()))
        username = menu_test.input_pc(u'Username: ')
        menu_test.print_pc(b'\x0d'.decode()+b'\033[A'.decode()*2+'Password(don\'t worry the password are typing but hidden:',end='')
        password = getpass('')
    menu_test.print_pc(idle_cmd_txt_fix(b'\x0d'.decode()+b'\033[A'.decode()+print_space*(menu_test.get_width_()-6))+b'\x0d'.decode(),end='')

    #print('Login as ' + '\x1b[32m' + username + '\x1b[0m' + ' successfully.', password)
    userstatus = login(username, password)
    if username != '' and userstatus[0] == 'Guest':
        menu_test.print_commit = '\x1b[31m' + 'Login failed.' + '\x1b[0m'
    # sys.exit()
    else:
        menu_test.print_commit = 'Login as ' + '\x1b[32m' + userstatus[1] + '\x1b[0m' + ' successfully.'

    #menu_test.print_commit = 'Login as ' + '\x1b[32m' + username + '\x1b[0m' + ' successfully.'
    if not 'idlelib.run' in sys.modules:
        print('\n'*newline_print,end='')
    else:
        menu_test.print_commit=''

def autocatch_t():
    autocatch()
    queueu(os.path.join('.','queue.txt'))

def debug_t():
    # sys.settrace(debug3.traceit)
    debug_.debug_start()
    menu_test.print_msg = '\x1b[31m'+'Debug is on'+ '\x1b[0m'+'>'



menu_test.main_menu_(Title,Subtitle,exit_option_call_text_='000|0|')
menu_test.add_menu_('setting', 'Settings:', exit_option_text='Back', parent_='Main')
menu_test.add_multiselection_menue_('vquality', 'Video Quality:',vquality_sub, quality_list_t,parent_='setting')
menu_test.add_multiselection_menue_('language1', 'Language:', lang1_sub, lang_list_t,parent_='setting')
menu_test.add_multiselection_menue_('language2', 'Language:', lang2_sub, lang_list_t,parent_='setting')

menu_test.add_function('Main','Download Anime',ultimate)
menu_test.add_function('Main','Download Subtitle only',vilos_subtitle)
menu_test.add_function('Main','Login',login_t,reposition=True)
menu_test.add_function('Main','Login As Guest',login_t,['',''],reposition=True)
menu_test.add_function('Main','Download an entire Anime(Autocatch links)',autocatch_t)
menu_test.add_function('Main','Run Queue',queueu,[os.path.join('.','queue.txt')])
menu_test.add_space('Main')
if code_version[1] < code_version[0]:
    menu_test.add_function('Main','\x1b[31m'+'update'+ '\x1b[0m',subprocess.call,[[sys.executable.replace('pythonw.exe', 'python.exe'),
                                                                                   os.path.join(".", "crunchy-xml-decoder", "updater.py")]],
                           call_text_='111')
else:
    menu_test.add_space('Main')

menu_test.add_function('Main','Settings',menu_test.run_menu,['setting'],call_text_='999',reposition=True)
menu_test.add_function('Main','DEBUG',debug_t,call_text_='debug',reposition=True,hidden=True)
# menu_test.add_function('Main','DEBUG',debug_.debug_start,call_text_='debug',reposition=True,hidden=True)

menu_test.add_function('setting',
                        ['''Video Quality = \x1b[32m''',(menu_test.varible_pool_,'video_quality'),'''\x1b[0m'''],
                       multiitem_config_q_,[quality_list_t,quality_list_],reposition=True)
menu_test.add_function('setting',
                        ['''Primary Language = \x1b[32m''',(menu_test.varible_pool_,'language'),'''\x1b[0m'''],
                       multiitem_config_l1,[lang_list_t,lang_list_],reposition=True)
menu_test.add_function('setting',
                        ['''Secondary Language = \x1b[32m''',(menu_test.varible_pool_,'language2'),'''\x1b[0m'''],
                       multiitem_config_l2,[lang_list_t,lang_list_],reposition=True)
menu_test.add_function('setting',
                        ['''Hard Subtitle = ''',(menu_test.varible_pool_,'forcesubtitle'),''' #The Video will have 1 hard subtitle'''],
                       load_config,[],{'forcesubtitle':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['''USA Proxy = ''',(menu_test.varible_pool_,'forceusa'),''' #use a US session ID'''],
                       load_config,[],{'forceusa':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['''Localize cookies = ''',(menu_test.varible_pool_,'localizecookies'),''' #Localize the cookies (Experiment)'''],
                       load_config,[],{'localizecookies':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['''Only One Subtitle = ''',(menu_test.varible_pool_,'onlymainsub'),''' #Only download Primary Language'''],
                       load_config,[],{'onlymainsub':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['''Dub Filter = ''',(menu_test.varible_pool_,'dubfilter'),''' #Ignor dub links when autocatch'''],
                       load_config,[],{'dubfilter':'toggle'},reposition=True)
menu_test.add_function('setting',
                        ['''Change the Number of The Download Connection = \x1b[32m''',(menu_test.varible_pool_,'connection_n_'),'''\x1b[0m'''],
                       load_config,[],{'connection_n_':[input,'Enter New Number of The Download Connection>>']},reposition=True)
menu_test.add_function('setting',
                        ['''use proxy(it disable if left blank)  = \x1b[32m''',(menu_test.varible_pool_,'proxy'),'''\x1b[0m  #ex:US'''],
                       load_config,[],{'proxy':[input,'Enter New proxy>>']},reposition=True)

menu_test.add_function('setting','Restore Default Settings',load_config,[],{'defult':True},reposition=True)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(argparse)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(argparse)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
parser = argparse.ArgumentParser(description=textwrap.dedent('''\
If you don't have a \x1b[32mpremium\x1b[0m account,
go and sign up for one now. It's well worth it, and supports the animators.'''),epilog='version: '+__version__)
parser.add_argument("-d","--download", type=str, nargs = 1, metavar='URL', help="Download Crunchyroll Anime Link")
parser.add_argument("-s","--subtitle", type=str, nargs = 1, metavar='URL', help="Download Crunchyroll Anime Subtitles only")
parser.add_argument("-l","--Login", type=str, nargs = 2, metavar=('usename', 'password'), help="Login with your Crunchyroll Account")
parser.add_argument("-g","--guest", action='store_true', help="Login As Guest")
parser.add_argument("-a","--autocatch", type=str, nargs = 1, metavar='URL', help="Download an entire Anime")
parser.add_argument("-q","--queue", type=str, nargs = '?', metavar='Queue Directory', const='.\\queue.txt', help="Run List of Crunchyroll Anime Link in queue file")
parser.add_argument("-D","--default", action='store_true', help="Restore Default Settings")
parser.add_argument("--debug", action='store_true', help="Run Code in Debug Mode")
arg = parser.parse_args()
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MAIN)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MAIN)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if __name__ == '__main__':
    ''' link for debug
https://www.crunchyroll.com/military/episode-1-the-mission-begins-668503
    '''
    #print(arg)
    if arg.download:
        ultimate(arg.download[0])
    elif arg.subtitle:
        vilos_subtitle(arg.subtitle[0])
    elif arg.Login:
        login(arg.Login[0], arg.Login[1])
    elif arg.guest:
        login('', '')
    elif arg.autocatch:
        autocatch(arg.autocatch[0])
        queueu(os.path.join('.', 'queue.txt'))
    elif arg.queue:
        queueu(os.path.join('.', arg.queue))
    elif arg.default:
        config(defult=True)
    elif arg.debug:
        debug_.debug_start()
        menu_test.print_msg = '\x1b[31m' + 'Debug is on' + '\x1b[0m' + '>'
        menu_test.start_()
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
