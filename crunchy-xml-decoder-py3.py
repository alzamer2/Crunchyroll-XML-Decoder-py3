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
import subprocess


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

iquality = 'highest'
ilang1 = 'English'
ilang2 = 'English'
iforcesub = False
iforceusa = False
ilocalizecookies = False
ionlymainsub = False
idubfilter = True
iconnection_n_ = 1
iproxy_ = ''
def defaultsettings(vvquality, vlang1, vlang2, vforcesub, vforceusa, vlocalizecookies, onlymainsub, vconnection_n_,vproxy_,vdubfilter):
    dsettings='''[SETTINGS]
# Set this to the preferred quality. Possible values are: "240p" , "360p", "480p", "720p", "1080p", or "highest" for highest available.
# Note that any quality higher than 360p still requires premium, unless it's available that way for free (some first episodes).
# We're not miracle workers.
video_quality = '''+vvquality+'''
# Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option (below).
# Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch
language = '''+vlang1+'''
# If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default
language2 = '''+vlang2+'''
# Set this if you want to use --forced-track rather than --default-track for subtitle
forcesubtitle = '''+str(vforcesub)+'''
# Set this if you want to use a US session ID
forceusa = '''+str(vforceusa)+'''
# Set this if you want to Localize the cookies (this option is under testing and may generate some problem and it willnot work with -forceusa- option)
localizecookies = '''+str(vlocalizecookies)+'''
# Set this if you only want to mux one subtitle only (this so make easy for some devices like TVs to play subtitle)
onlymainsub='''+str(onlymainsub)+'''
# Set this if you autocatch dub links too
dubfilter='''+str(vdubfilter)+'''
# Set this option to increase the Number of the connection
connection_n_='''+str(vconnection_n_)+'''
# Set this option to use proxy, example: US
Proxy = '''+vproxy_+'''
'''
    open(os.path.join('.','settings.ini'), 'w', encoding='utf8').write(dsettings)

if not os.path.lexists(os.path.join('.','settings.ini')):
    defaultsettings(iquality, ilang1, ilang2, iforcesub, iforceusa, ilocalizecookies, ionlymainsub, iconnection_n_, iproxy_, idubfilter)

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
#'''
    userstatus = getuserstatus()
else:
    pass

    userstatus = getuserstatus()
    print(idle_cmd_txt_fix('User Name = ' + '\x1b[32m' + userstatus[1] + '\x1b[0m'))
    print(idle_cmd_txt_fix('Membership Type = ' + '\x1b[32m' +userstatus[0] + '\x1b[0m'))
#'''
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(Argument Parser)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
    
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(FUNCTION)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
def queueu(queuepath):
    if not os.path.lexists(queuepath):
        open(queuepath, 'w').write(u'#the any line that has hash before the link will be skiped\n')
        subprocess.call('notepad.exe '+queuepath)
    lines = open(queuepath).readlines()
    for line in lines:
        if line.rstrip('\n') ==''.join(line.rstrip('\n').split('#', 1)):
            #print ''.join(line.rstrip('\n').split('#', 1))
            ultimate(line.rstrip('\n'), '', '')
            for i in range(0, len(lines)):
                if lines[i]== line:
                    lines[i]='#'+lines[i]
                    new_line_2=''
                    for new_line_ in lines:
                        try:
                            new_line_2=new_line_2+new_line_
                        except:
                            new_line_2=new_line_
                    open(queuepath, 'w').write(new_line_2)

def Languages_(Varname_):
    while True:
        seleccion = 0
        if Varname_ == 'slang1':
            print(idle_cmd_txt_fix('''Set this to the desired subtitle language. If the subtitles aren\'t available in that language, it reverts to the Secondary language option'''))
        if Varname_ == 'slang2':
            print(idle_cmd_txt_fix('''If the Primary language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default'''))
        try:
            print(idle_cmd_txt_fix('''Available Languages:
0.- '''+'''\x1b[32m'''+'''English'''+'''\x1b[0m'''+'''
1.- '''+'''\x1b[32m'''+'''Espanol'''+'''\x1b[0m'''+'''
2.- '''+'''\x1b[32m'''+'''Espanol (Espana)'''+'''\x1b[0m'''+'''
3.- '''+'''\x1b[32m'''+'''Francais'''+'''\x1b[0m'''+'''
4.- '''+'''\x1b[32m'''+'''Portugues'''+'''\x1b[0m'''+'''
5.- '''+'''\x1b[32m'''+'''Turkce'''+'''\x1b[0m'''+'''
6.- '''+'''\x1b[32m'''+'''Italiano'''+'''\x1b[0m'''+'''
7.- '''+'''\x1b[32m'''+'''Arabic'''+'''\x1b[0m'''+'''
8.- '''+'''\x1b[32m'''+'''Deutsch'''+'''\x1b[0m'''+'''
9.- '''+'''\x1b[32m'''+'''Russian'''+'''\x1b[0m'''))
            seleccion = int(input('> '))
        except:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue
        if seleccion == 1 :
            return 'Espanol'
        elif seleccion == 2 :
            return 'Espanol_Espana'
        elif seleccion == 3 :
            return 'Francais'
        elif seleccion == 4 :
            return 'Portugues'
        elif seleccion == 5 :
            return 'Turkce'
        elif seleccion == 6 :
            return 'Italiano'
        elif seleccion == 7 :
            return 'Arabic'
        elif seleccion == 8 :
            return 'Deutsch'
        elif seleccion == 9 :
            return 'Russian'
        elif seleccion == 0 :
            return 'English'
        else:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue

def videoquality_():
    while True:
        vquality = config()['video_quality']
        seleccion = 5
        try:
            print(idle_cmd_txt_fix('''Set This To The Preferred Quality:
0.- '''+'''\x1b[32m'''+'''android (240p)'''+'''\x1b[0m'''+'''
1.- '''+'''\x1b[32m'''+'''360p'''+'''\x1b[0m'''+'''
2.- '''+'''\x1b[32m'''+'''480p'''+'''\x1b[0m'''+'''
3.- '''+'''\x1b[32m'''+'''720p'''+'''\x1b[0m'''+'''
4.- '''+'''\x1b[32m'''+'''1080p'''+'''\x1b[0m'''+'''
5.- '''+'''\x1b[32m'''+'''highest'''+'''\x1b[0m'''+'''
Note: Any Quality Higher Than 360p Still Requires Premium, Unless It's Available That Way For Free (Some First Episodes).
We're Not Miracle Workers.'''))
            seleccion = int(input('> '))
        except:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue
        if seleccion == 0 :
            return '240p'
        elif seleccion == 1 :
            return '360p'
        elif seleccion == 2 :
            return '480p'
        elif seleccion == 3 :
            return '720p'
        elif seleccion == 4 :
            return '1080p'
        elif seleccion == 5 :
            return 'highest'
        else:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue

def settings_():
    while True:
        #slang1, slang2, sforcesub, sforceusa, slocalizecookies, vquality, vonlymainsub, vconnection_n_,vproxy_ = config()
        config_ = config()
        slang1 = config_['language']
        slang2 = config_['language2']
        sforcesub = config_['forcesubtitle']
        sforceusa = config_['forceusa']
        slocalizecookies = config_['localizecookies']
        vquality = config_['video_quality']
        vonlymainsub = config_['onlymainsub']
        vconnection_n_ = config_['connection_n_']
        vproxy_ = config_['proxy']
        vdubfilter = config_['dubfilter']
        slang1 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
            u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
            u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang1]
        slang2 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
            u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
            u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang2]
        if slang1 == 'Espanol_Espana':
            slang1_ = 'Espanol (Espana)'
        else:
            slang1_ = slang1
        if slang2 == 'Espanol_Espana':
            slang2_ = 'Espanol (Espana)'
        else:
            slang2_ = slang2
        seleccion = 0
        try:
            print(idle_cmd_txt_fix('''Options:
0.- Exit
1.- Video Quality = \x1b[32m'''+vquality+'''\x1b[0m
2.- Primary Language = \x1b[32m'''+slang1_+'''\x1b[0m
3.- Secondary Language = \x1b[32m'''+slang2_+'''\x1b[0m
4.- Hard Subtitle = '''+('\x1b[32m'+str(sforcesub)+'\x1b[0m' if sforcesub else '\x1b[31m'+str(sforcesub)+'\x1b[0m')+'''		#The Video will have 1 hard subtitle
5.- USA Proxy = '''+('\x1b[32m'+str(sforceusa)+'\x1b[0m' if sforceusa else '\x1b[31m'+str(sforceusa)+'\x1b[0m')+'''			#use a US session ID
6.- Localize cookies = '''+('\x1b[32m'+str(slocalizecookies)+'\x1b[0m' if slocalizecookies else '\x1b[31m'+str(slocalizecookies)+'\x1b[0m')+'''		#Localize the cookies (Experiment)
7.- Only One Subtitle = '''+('\x1b[32m'+str(vonlymainsub)+'\x1b[0m' if vonlymainsub else '\x1b[31m'+str(vonlymainsub)+'\x1b[0m')+'''		#Only download Primary Language
8.- Dub Filter = '''+('\x1b[32m'+str(vdubfilter)+'\x1b[0m' if vdubfilter else '\x1b[31m'+str(vdubfilter)+'\x1b[0m')+'''		#Ignor dub links when autocatch
9.- Change the Number of The Download Connection = \x1b[32m'''+str(vconnection_n_)+'''\x1b[0m
10.- use proxy(it disable if left blank)  = \x1b[32m'''+vproxy_+''' \x1b[0m  #ex:US
11.- Restore Default Settings
> '''))
            seleccion = int(input('> '))
        except:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue
        if seleccion == 1 :
            vquality = videoquality_()
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 2 :
            slang1 = Languages_('slang1')
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 3 :
            slang2 = Languages_('slang2')
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 4 :
            if sforcesub:
                sforcesub = False
            else:
                sforcesub = True
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 5 :
            if sforceusa:
                sforceusa = False
            else:
                sforceusa = True
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 6 :
            if slocalizecookies:
                slocalizecookies = False
            else:
                slocalizecookies = True
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 7 :
            if vonlymainsub:
                vonlymainsub = False
            else:
                vonlymainsub = True
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 8 :
            if vdubfilter:
                vdubfilter = False
            else:
                vdubfilter = True
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 9 :
            vconnection_n_ = input(u'Please Input The Download Connection Nymber: ')
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            continue
        elif seleccion == 10 :
            vproxy_ = input(u'Please Input The Proxy: ')
            defaultsettings(vquality, slang1, slang2, sforcesub, sforceusa, slocalizecookies, vonlymainsub, vconnection_n_, vproxy_, vdubfilter)
            getuserstatus(True)
            continue
        elif seleccion == 11 :
            defaultsettings(iquality, ilang1, ilang2, iforcesub, iforceusa, ilocalizecookies, ionlymainsub, iconnection_n_, iproxy_, idubfilter)
            continue
        elif seleccion == 0 :
            break
        else:
            print(idle_cmd_txt_fix("\x1b[31m"+"ERROR: Invalid option."+"\x1b[0m"))
            continue

def make_choise():
    #seleccion = 0
    while True:
        print(idle_cmd_txt_fix('''Options:
1.- Download Anime 
2.- Download Subtitle only
3.- Login
4.- Login As Guest
5.- Download an entire Anime(Autocatch links)
6.- Run Queue
'''+('\n111.- '+'\x1b[31m'+'update'+ '\x1b[0m' if code_version[1] < code_version[0] else '\n')+'''
999.- Settings
000.- Exit'''))
        seleccion = input('> ')
        if seleccion == '':
            break
        elif not seleccion.isdigit():
            print(idle_cmd_txt_fix('\x1b[31m' + 'Invalid Input!' + '\x1b[0m'))
            continue
        elif int(seleccion) == 0:
            break
        elif int(seleccion) == 1:
            ultimate()
            #mkv_merge('.\export\\The Rising of the Shield Hero - 1 - The Shield Hero.ts','480p','ara')
            pass
        elif int(seleccion) == 2:
            #decode('http://www.crunchyroll.com/military/episode-1-the-mission-begins-668503')
            #decode(input('Please enter Crunchyroll video URL:\n'))
            vilos_subtitle(input('Please enter Crunchyroll video URL:\n'))
            pass
        elif int(seleccion) == 3:
            username = input(u'Username: ')
            password = getpass('Password(don\'t worry the password are typing but hidden:')
            login(username, password)
            continue
        elif int(seleccion) == 4:
            login('', '')
            continue
        elif int(seleccion) == 5:
            #pass
            autocatch()
            queueu(os.path.join('.','queue.txt'))
        elif int(seleccion) == 6:
            queueu(os.path.join('.','queue.txt'))
        elif int(seleccion) == 111:
            subprocess.call([sys.executable.replace('pythonw.exe', 'python.exe'),
                             os.path.join(".", "crunchy-xml-decoder", "updater.py")])
        elif int(seleccion) == 999:
            settings_()
        else:
            print(idle_cmd_txt_fix('\x1b[31m' + 'Invalid Input!' + '\x1b[0m'))
            continue



def debug(func, *args, **kwds):
    import trace ##debug
    # create a Trace object, telling it what to ignore, and whether to
    # do tracing or line-counting or both.
    tracer = trace.Trace(
        ignoredirs=[sys.prefix, sys.exec_prefix],
        trace=1,
        count=1)
    # run the new command using the given tracer
    tracer.runfunc(func, *args, **kwds)
    # make a report, placing output in the current directory
    r = tracer.results()
    r.write_results(show_missing=True, coverdir=".")

def test_():
    for i in [1,2,3]:
        print(i)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#(MAIN)#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
if __name__ == '__main__':
    make_choise()
    #debug(test_)
    #print('done?')
    #input()
