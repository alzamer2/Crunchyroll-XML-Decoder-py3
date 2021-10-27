#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import textwrap
import re
import types

from colorama import Fore, Style, init
from pager import _windows_get_window_size as get_terminal_size

if sys.version_info < (3, 0, 0):
    input = raw_input
else:
    pass

init()

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

class pmenu():
    def __init__(self):
        self.indent_ = 2
        self.frame_ = ['│','─','┌','┐','└','┘']
        self.menus_ = {}
        self.menus_functions_ ={}
        self.menus_frames_ = {}
        self.menus_functions_internal_ = {}
        self.menue_parrent_ = {}
        self.menue_running_ = {}
        self.varible_pool_ = {}
        self.menue_reposition_ = {}
        self.print_counter = 0
        self.save_print_counter = 0
        self.print_commit = ''
        self.print_msg = ''

    def print_pc(self, *arg, **kwargs):
        self.print_counter += 1
        print(*arg,**kwargs)

    def test_function(self):
        text_list = [tuple(('title','title')),tuple(('sub',f'''\
If you don't have a {Red_c}premium{Green_c} account,
go and sign up for one now. It's well worth it, and supports the animators.''')),tuple(('lv2','item'))]
        text_list_ = self.createw_(self.parse_text(text_list))
        for line_ in text_list_:
                print(line_)
    def empty_function(self):
        pass
    
    def input_pc(self,prompt=''):
        self.print_pc(b'\x0d'.decode()+b'\033[A'.decode()+prompt,end='')
        input_t = input('')
        if not 'idlelib.run' in sys.modules:
            self.print_pc(b'\x0d'.decode()+' '*(self.get_width_()-6))
        self.print_counter -= 1
        return input_t
    
    def join_(self,texts_):
        if type(texts_) == str:
            return texts_
        elif type(texts_) == list:
            temp_texts_ = ''
            for item_ in texts_:
                if type(item_) == tuple:
                    if type(item_[0]) == types.FunctionType:
                        fun_value = str(item_[0](item_[1]))
                        if fun_value == str(True):
                            fun_value = f'{Green_c}{fun_value}{Default_c}'
                        elif fun_value == str(False):
                            fun_value = f'{Red_c}{fun_value}{Default_c}'
                        temp_texts_ += fun_value
                    elif type(item_[0]) == dict:
                        fun_value = str(item_[0][item_[1]])
                        if fun_value == str(True):
                            fun_value = f'{Green_c}{fun_value}{Default_c}'
                        elif fun_value == str(False):
                            fun_value = f'{Red_c}{fun_value}{Default_c}'
                        temp_texts_ += fun_value
                    else:
                        temp_texts_ += ''.join(item_)
                        
                elif type(item_) == types.FunctionType:
                    fun_value = str(item_())
                    if fun_value == str(True):
                        fun_value = f'{Green_c}{fun_value}{Default_c}'
                    elif fun_value == str(False):
                        fun_value = f'{Red_c}{fun_value}{Default_c}'
                    temp_texts_ += fun_value
                elif type(item_) == bool:
                    if item_:
                        temp_texts_ += f'{Green_c}{item_}{Default_c}'
                    else:
                        temp_texts_ += f'{Red_c}{item_}{Default_c}'
                else:
                    temp_texts_ += str(item_)
            return temp_texts_
        else:
            return str(texts_)
                    
            
    def start_(self):
        print()
        frames_len = []
        for value_ in self.menus_frames_.values():
            frames_len += [len(value_)]
        for frame in self.menus_frames_:
            if len(self.menus_frames_[frame]) < max(frames_len):
                for i in range(len(self.menus_frames_[frame]),max(frames_len)):
                    self.add_space(frame)
        frames_len = []
        for value_ in self.menus_frames_.values():
            frames_len += [len(value_)]
        self.run_menu('Main')

    def run_menu(self, menu_name_):
        self.menue_running_[menu_name_] = True
        #self.print_commit = ''
        do_reposition = True
        while self.menue_running_[menu_name_]:
            menus_functions_internal_temp = {}
            for dict_item_ in self.menus_functions_internal_[menu_name_]:
                for dict_item_v in self.menus_functions_internal_[menu_name_][dict_item_]:
                    menus_functions_internal_temp.update({dict_item_v:dict_item_})
            if do_reposition:
                self.repositionfunction(self.print_counter-self.save_print_counter+2)

            do_reposition = True
            self.save_print_counter = self.print_counter+1
            for line_ in self.menus_frames_[menu_name_]:
                self.print_pc(line_)
            if not 'idlelib.run' in sys.modules:
                console_space = ' '
            else:
                console_space = ''
            self.print_pc(b'\x0d'.decode()+console_space*(self.get_width_()-6)+b'\x0d'.decode()+self.print_msg+self.print_commit+'>>',end='')
            self.print_commit = ''
            input_ = str(input())
            if input_ in self.menus_functions_[menu_name_].keys():
                function_ = self.menus_functions_[menu_name_][input_]
                output_ = function_[0](*function_[1], **function_[2])
                do_reposition = self.menue_reposition_[menu_name_][input_]
                if not output_ is None:
                    return output_
            elif input_ in menus_functions_internal_temp.keys():
                function_ = self.menus_functions_[menu_name_][menus_functions_internal_temp[input_]]
                output_ = function_[0](*function_[1], **function_[2])
                if not output_ is None:
                    return output_
            else:
                self.print_commit = f'{Red_c}Invalid Input!{Default_c}'

    def main_menu_(self, title_='', subtitle_='',exit_option_text='Exit', exit_option_call_text_='[EXIT]'):
        self.add_menu_('Main', title_, subtitle_, exit_option_text, exit_option_call_text_)

    def exit_function(self,menu_name_):
        self.menue_running_[menu_name_] = False
        # if self.menue_parrent_[menu_name_] == None:
        #     exit()
        # else:
        #     self.menue_running_[menu_name_] = False

    def add_exit(self, menu_name_, exit_option_text='Exit', call_text_='[EXIT]'):
        self.menus_[menu_name_] += [tuple(('[EXIT]'+'|'+call_text_,exit_option_text))]
        self.menus_functions_[menu_name_].update({'[EXIT]':[self.exit_function, [menu_name_], {}]})
        self.redraw(menu_name_)

    def add_multiselection_menue_old(self, menu_name_, title_='', subtitle_='', list_=[], return_list = [], function_=None,
                                  exit_option_text='Back', exit_option_call_text_='[EXIT]', parent_=None):
        if return_list == []:
            return_list = list_
        self.add_menu_(menu_name_, title_, subtitle_, exit_option_text, exit_option_call_text_, parent_)
        def returnfunction(list_t=[],return_list_t=[],item__=None):
            return return_list_t[list_t.index(item__)]

        if function_ == None:
            function_ = returnfunction
        for i,item in enumerate(list_):
            self.add_function(menu_name_, item, function_,[list_, return_list, item],{})
        pass

    def multiselection_menue_(self, menu_name_, title_='', subtitle_='', list_=[],
                                  exit_option_text='Back', exit_option_call_text_='[EXIT]', parent_=None):
        self.add_menu_(menu_name_, title_, subtitle_, exit_option_text, exit_option_call_text_, parent_)
        def returnfunction(item__=None):
            return item__
        for i,item in enumerate(list_):
            self.add_function(menu_name_, item, returnfunction,[item],{}, reposition=True)
        output_ =  self.run_menu(menu_name_)
        if not output_ is None:
            return output_

    def add_multiselection_menue_(self, menu_name_, title_='', subtitle_='', list_=[],
                                  exit_option_text='Back', exit_option_call_text_='[EXIT]', parent_=None):
        self.add_menu_(menu_name_, title_, subtitle_, exit_option_text, exit_option_call_text_, parent_)
        def returnfunction(item__=None):
            return item__
        for i,item in enumerate(list_):
            self.add_function(menu_name_, item, returnfunction,[item],{}, reposition=True)
        

    def add_menu_(self, menu_name_, title_='', subtitle_='',exit_option_text='Exit',exit_option_call_text_='[EXIT]',parent_=None):
        self.menus_.update({menu_name_:[]})
        self.menus_functions_.update({menu_name_:{}})
        self.menus_functions_internal_.update({menu_name_:{'[EXIT]':'exit'}})
        self.menue_parrent_.update({menu_name_:parent_})
        self.menue_running_.update({menu_name_:False})
        self.menue_reposition_.update({menu_name_:{}})
        if title_!='':
            self.menus_[menu_name_] += [tuple(('title',title_))]
        if subtitle_!='':
            self.menus_[menu_name_] += [tuple(('sub',subtitle_))]
        self.redraw(menu_name_)
        self.add_exit(menu_name_,exit_option_text,exit_option_call_text_)

    def repositionfunction(self,reposition_value=None):
        if not 'idlelib.run' in sys.modules:
            if reposition_value is None:
                reposition_value = len(self.menus_frames_['Main']) + 2
            print(b'\x0d'.decode()+b'\033[A'.decode()*reposition_value)
                

    def add_function(self, menu_name_, text_, function_, args=[], kwargs={},
                     call_text_=None, reposition=False, hidden=False):
        auto_index = 1
        if call_text_ is None:
            while True:
                if not str(auto_index) in self.menus_functions_[menu_name_]:
                    call_text_ = str(auto_index)
                    break
                auto_index += 1

        if not hidden:
            self.menus_[menu_name_] += [tuple(('lv2'+'|'+call_text_,text_))]
        self.menus_functions_[menu_name_].update({call_text_:[function_, args, kwargs]})
        self.menue_reposition_[menu_name_].update({call_text_:reposition})
        self.redraw(menu_name_)

    def redraw(self,menu_name_=None):
        if not menu_name_:
            for menu_name_ in self.menus_frames_:
                text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
                self.menus_frames_.update({menu_name_:text_list_})
        else:
            text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
            self.menus_frames_.update({menu_name_:text_list_})

    def add_space(self, menu_name_):
        self.menus_[menu_name_] += [tuple(('space',''))]
        self.redraw(menu_name_)

    def parse_text(self, menu_name_, texts_):
        
        new_texts_ = []
        keys_texts_ = {}
        auto_index = 1
                    
                
        texts_exit = None
        for item_ in texts_:
            if re.match('\[EXIT\]\|',item_[0]) != None:
                texts_exit = tuple((item_[0],item_[1]))
        if texts_exit:
            call_list_ = []
            for item_ in texts_:
                if item_[0] != 'title' and item_[0] != 'sub' and item_[0] != 'space' and re.findall('\|(.*)',item_[0]) != ['[EXIT]']:
                    call_list_ += [re.findall('\|(.*)',item_[0])[0]]
            exit_index = texts_.index(texts_exit)
            if exit_index+1 != len(texts_):
                texts_ = texts_[0:exit_index]+texts_[exit_index+1:]+[tuple(texts_[exit_index])]
                
        for item_ in texts_:
            if item_[0] == 'title' or item_[0] == 'sub':
                new_texts_ += self.warptext(self.join_(item_[1]),1)
                new_texts_ += self.warptext('')
            elif item_[0] == 'space':
                new_texts_ += ' '
            elif re.match('\[EXIT\]\|',item_[0]):
                if re.search('\|\[EXIT\]',item_[0]):
                    pre_ = ['ex']
                    auto_index = 1
                    while True:
                        if not str(auto_index) in call_list_:
                            pre_ = [str(auto_index)]
                            break
                        auto_index += 1
                    
                else:
                    pre_ = re.findall('\[EXIT\]\|(.*)',item_[0])[0]
                    pre_= re.findall('(.*?)\|',pre_+'|')
                self.menus_functions_internal_[menu_name_]['[EXIT]'] = pre_
                new_texts_ += self.warptext(pre_[0] + ' - ' + self.join_(item_[1]),2)
            elif re.match('lv\d{1,3}',item_[0]) != None:
                pre_ = re.findall('lv\d{1,3}\|(.*)',item_[0])[0]
                    
                new_texts_ += self.warptext(pre_ + ' - ' + self.join_(item_[1]),int(re.findall('lv(\d{1,3})',item_[0])[0]))
        return new_texts_

    def get_width_(self):
        try:
            if get_terminal_size()[0] != 0:
                return get_terminal_size()[0]
            else:
                return 70
        except:
            return 70

    def warptext(self, text_, lv=0):
        width_ = self.get_width_()
        text_to_clean_ = re.findall('\\x1b.*?\[(\d*\w)(.*)\\x1b.*?\[\d*\w',text_)
        for item_ in text_to_clean_:
            text_= re.sub(r'\x1b.*?\[\d*(?:;\d*)?\w','',text_)
        if text_ != '':
            ptext = textwrap.wrap(text_, width=width_-6,initial_indent=" "*2*lv,subsequent_indent=" "*(2*lv+4))
        else:
            ptext = [' ']
        if not 'idlelib.run' in sys.modules:
            for i, item_ in enumerate(ptext):
                for replacement_ in text_to_clean_:
                    ptext[i] = item_.replace(replacement_[1],'\x1b['+replacement_[0]+replacement_[1]+f'{Default_c}')
                
        return ptext

    def createw_(self, text_list_):
        width_ = self.get_width_()
        for i, line_ in enumerate(text_list_):
            text_list_[i] = " "*self.indent_+self.frame_[0]+text_list_[i]+' '*(width_-len(re.sub(r'\x1b.*?\[\d*(?:;\d*)?\w','',line_))-6)+self.frame_[0]
        text_list_.insert(0," "*self.indent_+self.frame_[2]+self.frame_[1]*(width_-6)+self.frame_[3])
        text_list_.insert(1," "*self.indent_+self.frame_[0]+' '*(width_-6)+self.frame_[0])
        text_list_ +=[" "*self.indent_+self.frame_[0]+' '*(width_-6)+self.frame_[0]]
        text_list_ +=[" "*self.indent_+self.frame_[4]+self.frame_[1]*(width_-6)+self.frame_[5]]
        return text_list_

        
        
                          
    def printw(self, text_):
        width_ = self.get_width_()
        no_line=text_.count('\n')+1
        ptext = textwrap.wrap(text_, width=width_,initial_indent=" "*self.indent_+self.frame_[0],
                              subsequent_indent=" "*self.indent_+self.frame_[0],
                              )
        self.print_pc(" "*self.indent_+self.frame_[2]+self.frame_[1]*(width_-3)+self.frame_[3])
        for line_ in ptext:
            self.print_pc(line_+' '*(width_-len(line_))+self.frame_[0])
        self.print_pc(" "*self.indent_+self.frame_[4]+self.frame_[1]*(width_-3)+self.frame_[5])

if __name__ == '__main__':
    from altfuncs import config
    menu_test = pmenu()
    def load_config(**kwargs):
        for key in kwargs:
            if type(kwargs[key]) == list:
                if kwargs[key][0] == input:
                    kwargs[key] = menu_test.input_pc(kwargs[key][1])
        config_ = config(**kwargs)
        
        if config_['language'] == 'Espanol_Espana':
            config_['language'] = 'Espanol (Espana)'
        if config_['language2'] == 'Espanol_Espana':
            config_['language2'] = 'Espanol (Espana)'
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
    Subtitle = f'''\
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
    lang_list_ = ['English','Espanol','Espanol_Espana','Francais','Portugues','Turkce','Italiano','Arabic','Deutsch','Russian']
    lang_list_t = [f'{Green_c}{lang_v.replace("Espanol_Espana","Espanol (Espana)")}{Default_c}' for lang_v in lang_list_]
    
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


        
    menu_test.main_menu_(Title,Subtitle,exit_option_call_text_='000|0|')
    menu_test.add_menu_('setting', 'Settings:', exit_option_text='Back', parent_='Main')
    menu_test.add_multiselection_menue_('vquality', 'Video Quality:',vquality_sub, quality_list_t,parent_='setting')
    menu_test.add_multiselection_menue_('language1', 'Language:', lang1_sub, lang_list_t,parent_='setting')
    menu_test.add_multiselection_menue_('language2', 'Language:', lang2_sub, lang_list_t,parent_='setting')
    
    menu_test.add_function('Main','Download Anime',print,['hi'])
    menu_test.add_function('Main','Download Subtitle only',print,['lol'])
    menu_test.add_function('Main','Login',print,['lol2'])
    menu_test.add_function('Main','Login As Guest',print,['lol2'])
    menu_test.add_function('Main','Download an entire Anime(Autocatch links)',print,['lol2'])
    menu_test.add_function('Main','Run Queue',print,['lol2'])
    menu_test.add_space('Main')
    menu_test.add_function('Main',f'{Red_c}update{Default_c}',print,['lol2'],call_text_='111')
    menu_test.add_function('Main','Settings',menu_test.run_menu,['setting'],call_text_='999',reposition=True)
    menu_test.add_function('Main','DEBUG',print,['hi'],call_text_='debug',reposition=False,hidden=True)

    menu_test.add_function('setting',
                           [f'Video Quality = {Green_c}',(menu_test.varible_pool_,'video_quality'),f'{Default_c}'],
                           multiitem_config_q_,[quality_list_t,quality_list_],reposition=True)
    menu_test.add_function('setting',
                           [f'Primary Language = {Green_c}',(menu_test.varible_pool_,'language'),f'{Default_c}'],
                           multiitem_config_l1,[lang_list_t,lang_list_],reposition=True)
    menu_test.add_function('setting',
                           [f'Primary Language = {Green_c}',(menu_test.varible_pool_,'language2'),f'{Default_c}'],
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
                           [f'Change the Number of The Download Connection = {Green_c}',(menu_test.varible_pool_,'connection_n_'),f'{Default_c}'],
                           load_config,[],{'connection_n_':[input,'Enter New Number of The Download Connection>>']},reposition=True)
    menu_test.add_function('setting',
                           [f'use proxy(it disable if left blank)  = {Green_c}',(menu_test.varible_pool_,'proxy'),f'{Default_c}  #ex:US'],
                           load_config,[],{'proxy':[input,'Enter New proxy>>']},reposition=True)
    
    menu_test.add_function('setting','Restore Default Settings',load_config,[],{'defult':True},reposition=True)

    

    
    menu_test.start_()
    #menu_test.print_pc(Subtitle)


