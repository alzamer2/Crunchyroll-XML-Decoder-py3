#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
this is unlclean version of this script
its Deprecation and only for refreance
it will not update and may be deleted in future
'''

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

#print_counter = 0
#def print_pc(*arg,**kwargs):
#    global print_counter
#    print_counter +=1
#    #print(print_counter,end='')
#    print(*arg,**kwargs)

def idle_cmd_txt_fix(print_text):
    if 'idlelib.run' in sys.modules:
        print_text = re.sub('\\x1b.*?\[\d*\w','',print_text)
    return print_text

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

    def print_pc(self, *arg, **kwargs):
        self.print_counter += 1
        #print('0'*(4-len(str(self.print_counter)))+str(self.print_counter),
        #      '0'*(4-len(str(self.save_print_counter)))+str(self.save_print_counter),
        #      end='')
        print(*arg,**kwargs)

    def test_function(self):
        #print(self.warptext(val_,1))
        text_list = [tuple(('title','title')),tuple(('sub','''\
If you don't have a \x1b[31mpremium\x1b[0m account,
go and sign up for one now. It's well worth it, and supports the animators.''')),tuple(('lv2','item'))]
        text_list_ = self.createw_(self.parse_text(text_list))
        for line_ in text_list_:
                print(line_)
    def empty_function(self):
        pass
    
    def input_pc(self,prompt=''):
        self.print_pc(idle_cmd_txt_fix(b'\x0d'.decode()+b'\033[A'.decode()+prompt),end='')
        input_t = input('')
        if not 'idlelib.run' in sys.modules:
            self.print_pc(idle_cmd_txt_fix(b'\x0d'.decode()+' '*(self.get_width_()-6)))
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
                            fun_value = '\x1b[32m' + fun_value + '\x1b[0m'
                        elif fun_value == str(False):
                            fun_value = '\x1b[31m' + fun_value + '\x1b[0m'
                        temp_texts_ += fun_value
                    elif type(item_[0]) == dict:
                        fun_value = str(item_[0][item_[1]])
                        if fun_value == str(True):
                            fun_value = '\x1b[32m' + fun_value + '\x1b[0m'
                        elif fun_value == str(False):
                            fun_value = '\x1b[31m' + fun_value + '\x1b[0m'
                        temp_texts_ += fun_value
                    else:
                        temp_texts_ += ''.join(item_)
                        
                elif type(item_) == types.FunctionType:
                    fun_value = str(item_())
                    if fun_value == str(True):
                        fun_value = '\x1b[32m' + fun_value + '\x1b[0m'
                    elif fun_value == str(False):
                        fun_value = '\x1b[31m' + fun_value + '\x1b[0m'
                    temp_texts_ += fun_value
                elif type(item_) == bool:
                    if item_:
                        temp_texts_ += '\x1b[32m' + str(item_) + '\x1b[0m'
                    else:
                        temp_texts_ += '\x1b[31m' + str(item_) + '\x1b[0m'
                else:
                    temp_texts_ += str(item_)
            return temp_texts_
        else:
            return str(texts_)
                    
            
    def start_(self):
        print()
        ##print('self.menus_')
        ##print(self.menus_)
        ##print(self.menus_functions_ )
        ##print(self.menus_functions_internal_ )
        ##print(self.menue_parrent_)
        #text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_['Main']))
        #self.menus_frames_.update({'Main':text_list_})
        #for line_ in self.menus_frames_['Main']:
        #    print(line_)
        #input_ = input('>>')
        frames_len = []
        for value_ in self.menus_frames_.values():
            frames_len += [len(value_)]
        #print(frames_len)
        #print(max(frames_len))
        for frame in self.menus_frames_:
            if len(self.menus_frames_[frame]) < max(frames_len):
                for i in range(len(self.menus_frames_[frame]),max(frames_len)):
                    self.add_space(frame)
        frames_len = []
        for value_ in self.menus_frames_.values():
            frames_len += [len(value_)]
        #print(frames_len)
        #print(max(frames_len))
        #print(self.menus_frames_.keys())
        self.run_menu('Main')

    def run_menu(self, menu_name_):
        self.menue_running_[menu_name_] = True
        #firstnotprint = False
        print_commit = ''
        do_reposition = True
        while self.menue_running_[menu_name_]:
            #if not 'idlelib.run' in sys.modules:
            #    #print(self.menue_parrent_[menu_name_])
            #    
            #    if not self.menue_parrent_[menu_name_] is None:
            #        #print(firstnotprint,len(self.menus_frames_['Main']))
            #        #for i in range(1,len(self.menus_frames_['Main'])):
            #        #    print(b'\033[A'.decode())
            #        #print()
            #        print(b'\x0d'.decode()+b'\033[A'.decode()*(len(self.menus_frames_['Main'])+2))
            #        pass
            menus_functions_internal_temp = {}
            for dict_item_ in self.menus_functions_internal_[menu_name_]:
                for dict_item_v in self.menus_functions_internal_[menu_name_][dict_item_]:
                    menus_functions_internal_temp.update({dict_item_v:dict_item_})
            #print(self.menus_functions_)
            #print(menus_functions_internal_temp)
            #print(self.menus_functions_internal_)
            #print(self.menue_reposition_)
            #if not self.save_print_counter == self.print_counter:
            if do_reposition:
                self.repositionfunction(self.print_counter-self.save_print_counter+2)

            do_reposition = True
            self.save_print_counter = self.print_counter+1
            for line_ in self.menus_frames_[menu_name_]:
                self.print_pc(line_)
            #print(self.varible_pool_)
            if not 'idlelib.run' in sys.modules:
                console_space = ' '
            else:
                console_space = ''
            self.print_pc(idle_cmd_txt_fix(b'\x0d'.decode()+console_space*(self.get_width_()-6)+b'\x0d'.decode()+print_commit+'>>'),end='')
            #self.print_pc(self.menus_functions_internal_)
            print_commit = ''
            input_ = str(input())
            if input_ in self.menus_functions_[menu_name_].keys():
                function_ = self.menus_functions_[menu_name_][input_]
                #print(input_, menu_name_, self.menue_reposition_[menu_name_][input_])
                #input()
                #print(function_,function_[2].values(),input in function_[2].values())
                #if self.menue_reposition_[menu_name_][input_] and not function_ == input:
                #    pass#self.save_print_counter = self.print_counter
                #    self.repositionfunction(self.print_counter-self.save_print_counter+2)
                output_ = function_[0](*function_[1], **function_[2])
                #self.print_pc(self.print_counter,self.save_print_counter)
                #pass#self.repositionfunction(self.print_counter-self.save_print_counter+2)
                #if self.menue_reposition_[menu_name_][input_]:
                #    pass#self.save_print_counter = self.print_counter
                #    self.repositionfunction(self.print_counter-self.save_print_counter+2)
                do_reposition = self.menue_reposition_[menu_name_][input_]
                if not output_ is None:
                    return output_
            elif input_ in menus_functions_internal_temp.keys():
                function_ = self.menus_functions_[menu_name_][menus_functions_internal_temp[input_]]
                #print(input_)
                #print(menus_functions_internal_temp[input_])
                #print(function_)
                output_ = function_[0](*function_[1], **function_[2])
                if not output_ is None:
                    return output_
            else:
                print_commit = '\x1b[31m' + 'Invalid Input!' + '\x1b[0m'
                #self.repositionfunction(self.print_counter-self.save_print_counter+2)
                #self.repositionfunction()
            #firstnotprint = True

    def main_menu_(self, title_='', subtitle_='',exit_option_text='Exit', exit_option_call_text_='[EXIT]'):
        self.add_menu_('Main', title_, subtitle_, exit_option_text, exit_option_call_text_)

    def exit_function(self,menu_name_):
        if self.menue_parrent_[menu_name_] == None:
            exit()
        else:
            self.menue_running_[menu_name_] = False
            #self.repositionfunction()

    def add_exit(self, menu_name_, exit_option_text='Exit', call_text_='[EXIT]'):
        #self.add_function(menu_name_,exit_option_text,self.exit_function,[],call_text_=call_text_)
        self.menus_[menu_name_] += [tuple(('[EXIT]'+'|'+call_text_,exit_option_text))]
        self.menus_functions_[menu_name_].update({'[EXIT]':[self.exit_function, [menu_name_], {}]})
        #text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
        #self.menus_frames_.update({menu_name_:text_list_})
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
        #add_menu_(self, menu_name_, title_='', subtitle_='',exit_option_text='Exit',exit_option_call_text_='[EXIT]',parent_=None)
        pass
    ##add_menu_(self, menu_name_, title_='', subtitle_='',exit_option_text='Exit',exit_option_call_text_='[EXIT]',parent_=None)
    ##menu_test.add_menu_('vquality', 'Video Quality:', exit_option_text='Back', parent_='setting')

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
        #text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
        #self.menus_frames_.update({menu_name_:text_list_})
        self.redraw(menu_name_)
        self.add_exit(menu_name_,exit_option_text,exit_option_call_text_)

    def repositionfunction(self,reposition_value=None):
        if not 'idlelib.run' in sys.modules:
            if reposition_value is None:
                reposition_value = len(self.menus_frames_['Main']) + 2
            #print(b'\033[A'.decode()+b'\x0d'.decode()+' '*10+b'\x0d'.decode()+b'\033[A'.decode()*reposition_value)
            print(b'\x0d'.decode()+b'\033[A'.decode()*reposition_value)
            #print(self.menue_parrent_[menu_name_])
                
            #if not self.menue_parrent_[menu_name_] is None:
                #print(firstnotprint,len(self.menus_frames_['Main']))
                #for i in range(1,len(self.menus_frames_['Main'])):
                #    print(b'\033[A'.decode())
                #print()
            #    print(b'\x0d'.decode()+b'\033[A'.decode()*(len(self.menus_frames_['Main'])+2))
            #    pass

    def add_function(self, menu_name_, text_, function_, args=[], kwargs={}, call_text_=None, reposition=False):
        auto_index = 1
        if call_text_ is None:
            while True:
                #print(self.menus_functions_[menu_name_])
                if not str(auto_index) in self.menus_functions_[menu_name_]:
                    call_text_ = str(auto_index)
                    break
                auto_index += 1

        #print(text_)
        self.menus_[menu_name_] += [tuple(('lv2'+'|'+call_text_,text_))]
        self.menus_functions_[menu_name_].update({call_text_:[function_, args, kwargs]})
        self.menue_reposition_[menu_name_].update({call_text_:reposition})
        #text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
        #self.menus_frames_.update({menu_name_:text_list_})
        self.redraw(menu_name_)

    def redraw(self,menu_name_=None):
        #print(self.menus_)
        if not menu_name_:
            for menu_name_ in self.menus_frames_:
                text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
                self.menus_frames_.update({menu_name_:text_list_})
        else:
            text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
            self.menus_frames_.update({menu_name_:text_list_})

    def add_space(self, menu_name_):
        self.menus_[menu_name_] += [tuple(('space',''))]
        #text_list_ = self.createw_(self.parse_text(menu_name_,self.menus_[menu_name_]))
        #self.menus_frames_.update({menu_name_:text_list_})
        self.redraw(menu_name_)

    def parse_text(self, menu_name_, texts_):
        
        new_texts_ = []
        #unclean_texts_ = []
        #for item_ in texts_:
        #    unclean_texts_ += [item_[1]]
        #for i, item_ in enumerate(texts_):
        #     texts_[i] = tuple((item_[0],re.sub('\\x1b.*?\[\d*\w','',item_[1])))
        keys_texts_ = {}
        auto_index = 1
        #for item_ in texts_:
        #    if item_[0] != 'title' and item_[0] != 'sub':
        #        if re.findall('lv\d{1,3}\|(.*)',item_[0])[0] != '':
        #            keys_texts_.update(dict({re.findall('lv\d{1,3}\|(.*)',item_[0])[0] : item_[1]}))
        #        else:
        #            keys_texts_.update(dict({auto_index : item_[1]}))
        #            for key_ in keys_texts_:
        #                if type(key_) is int:
        #                    auto_index +=1
                #non_int_key = 0
                #keys_texts_.update(dict({re.findall('lv\d{1,3}\|(.*)',item_[0])[0] : item_[1]}))
                #for key_ in keys_texts_:
                #    if type(key_) is str:
                #        non_int_key += 1
                    
                
        #print(texts_)
        #texts_keys = []
        #exit_in_texts_keys = False
        texts_exit = None
        for item_ in texts_:
            if re.match('\[EXIT\]\|',item_[0]) != None:
                texts_exit = tuple((item_[0],item_[1]))
        #print(texts_exit)
            #texts_keys += [item_[0]]
            #if not exit_in_texts_keys:
            #    exit_in_texts_keys = re.match('\[EXIT\]\|',item_[0]) != None
        #try:
        #    print(texts_.count(tuple(('lv2|[EXIT]', 'Exit'))))
        #except:
        #    pass
        #print(auto_index)
        #if texts_.count(tuple(('lv2|[EXIT]', 'Exit'))) != 0:
        #    call_list_ = []
        #    for item_ in texts_:
        #        if item_[0] != 'title' and item_[0] != 'sub' and item_[0] != 'space' and re.findall('lv\d{1,3}\|(.*)',item_[0])[0] != '[EXIT]':
        #            call_list_ += [re.findall('lv\d{1,3}\|(.*)',item_[0])[0]]
        #    exit_index=texts_.index(tuple(('lv2|[EXIT]', 'Exit')))
        #    if exit_index+1 != len(texts_):
        #        texts_ = texts_[0:exit_index]+texts_[exit_index+1:]+[tuple(texts_[exit_index])]
        #    print(call_list_)
        if texts_exit:
            call_list_ = []
            for item_ in texts_:
                if item_[0] != 'title' and item_[0] != 'sub' and item_[0] != 'space' and re.findall('\|(.*)',item_[0]) != ['[EXIT]']:
                    call_list_ += [re.findall('\|(.*)',item_[0])[0]]
            exit_index = texts_.index(texts_exit)
            if exit_index+1 != len(texts_):
                texts_ = texts_[0:exit_index]+texts_[exit_index+1:]+[tuple(texts_[exit_index])]
                
        #print(texts_)
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
                #if re.findall('lv\d{1,3}\|(.*)',item_[0])[0] == '[EXIT]':
                #    pre_ = 'ex'
                #    auto_index = 1
                #    while True:
                #        if not str(auto_index) in call_list_:
                #            pre_ = str(auto_index)
                #            break
                #        auto_index += 1
                #    
                #else:
                #    pre_ = re.findall('lv\d{1,3}\|(.*)',item_[0])[0]
                pre_ = re.findall('lv\d{1,3}\|(.*)',item_[0])[0]
                #if re.findall('lv\d{1,3}\|(.*)',item_[0])[0] != '':
                #    pre_ = re.findall('lv\d{1,3}\|(.*)',item_[0])[0]
                #    keys_texts_.update(dict({re.findall('lv\d{1,3}\|(.*)',item_[0])[0] : self.join_(item_[1])}))
                #else:
                #    keys_texts_.update(dict({auto_index : self.join_(item_[1])}))
                #    pre_ = str(auto_index)
                #    for key_ in keys_texts_:
                #        if type(key_) is int:
                #            auto_index +=1
                    
                new_texts_ += self.warptext(pre_ + ' - ' + self.join_(item_[1]),int(re.findall('lv(\d{1,3})',item_[0])[0]))
        #print(unclean_texts_)
        #print(new_texts_)
        return new_texts_

    def get_width_(self):
        if get_terminal_size()[0] != 0:
            return get_terminal_size()[0]
        else:
            return 70
            #return 50        

    def warptext(self, text_, lv=0):
        #if get_terminal_size()[0] != 0:
        #    width_ = get_terminal_size()[0]-10
        #else:
        #    width_ = 70
        #    #width_ = 50
        width_ = self.get_width_()
        text_to_clean_ = re.findall('\\x1b.*?\[(\d*\w)(.*)\\x1b.*?\[\d*\w',text_)
        for item_ in text_to_clean_:
            #print(item_[0],item_[1])
            #print(text_)
            #text_.replace(item_[0],item_[1])
            text_= re.sub('\\x1b.*?\[\d*\w','',text_)
            #print(text_)
        if text_ != '':
            ptext = textwrap.wrap(text_, width=width_-6,initial_indent=" "*2*lv,subsequent_indent=" "*(2*lv+4))
        else:
            ptext = [' ']
        #print(ptext)
        #for line_ in ptext:
        #    print(line_)
        #self.printw_(ptext)
        if not 'idlelib.run' in sys.modules:
            for i, item_ in enumerate(ptext):
                for replacement_ in text_to_clean_:
                    ptext[i] = item_.replace(replacement_[1],'\x1b['+replacement_[0]+replacement_[1]+'\x1b[0m')
                
        return ptext

    def createw_(self, text_list_):
        #if get_terminal_size()[0] != 0:
        #    width_ = get_terminal_size()[0]-10
        #else:
        #    width_ = 70
        #    #width_ = 50
        width_ = self.get_width_()
        for i, line_ in enumerate(text_list_):
            text_list_[i] = " "*self.indent_+self.frame_[0]+text_list_[i]+' '*(width_-len(re.sub('\\x1b.*?\[\d*\w','',line_))-6)+self.frame_[0]
        text_list_.insert(0," "*self.indent_+self.frame_[2]+self.frame_[1]*(width_-6)+self.frame_[3])
        text_list_.insert(1," "*self.indent_+self.frame_[0]+' '*(width_-6)+self.frame_[0])
        #text_list_.insert(-1," "*self.indent_+self.frame_[4]+self.frame_[1]*(width_-3)+self.frame_[5])
        text_list_ +=[" "*self.indent_+self.frame_[0]+' '*(width_-6)+self.frame_[0]]
        text_list_ +=[" "*self.indent_+self.frame_[4]+self.frame_[1]*(width_-6)+self.frame_[5]]
        #print(text_list_)
        #for line_ in text_list_:
        #    print(line_)
        return text_list_

        
        
                          
    def printw(self, text_):
        #if get_terminal_size()[0] != 0:
        #    width_ = get_terminal_size()[0]-10
        #else:
        #    width_ = 70
        #    #width_ = 50
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
    #config_ = config()
    #print(config_)
    #print(config(forceusa=True))
    #exit()
    #slang1 = ''
    #def load_config(**kwargs):
    #    config_ = config(**kwargs)
    #    slang1 = config_['language']
    #    slang2 = config_['language2']
    #    sforcesub = config_['forcesubtitle']
    #    sforceusa = config_['forceusa']
    #    slocalizecookies = config_['localizecookies']
    #    vquality = config_['video_quality']
    #    vonlymainsub = config_['onlymainsub']
    #    vconnection_n_ = config_['connection_n_']
    #    vproxy_ = config_['proxy']
    #    vdubfilter = config_['dubfilter']
    #    slang1 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
    #        u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
    #        u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang1]
    #    slang2 = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais', u'Português (Brasil)' : 'Portugues',
    #        u'English' : 'English', u'Español' : 'Espanol', u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano',
    #        u'العربية' : 'Arabic', u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[slang2]
    #    if slang1 == 'Espanol_Espana':
    #        slang1_ = 'Espanol (Espana)'
    #    else:
    #        slang1_ = slang1
    #    if slang2 == 'Espanol_Espana':
    #        slang2_ = 'Espanol (Espana)'
    #    else:
    #        slang2_ = slang2
    #load_config()
    #print(slang1)
    #exit()
    menu_test = pmenu()
    def load_config(**kwargs):
        for key in kwargs:
            if type(kwargs[key]) == list:
                if kwargs[key][0] == input:
                    kwargs[key] = menu_test.input_pc(kwargs[key][1])
        #print(kwargs)
        config_ = config(**kwargs)
        #print(config_)
        #print(config_['language'])
        
        #config_['language'] = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais',
        #                       u'Português (Brasil)' : 'Portugues', u'English' : 'English', u'Español' : 'Espanol',
        #                       u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano', u'العربية' : 'Arabic',
        #                       u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[config_['language']]
        #config_['language2'] = {u'Español (Espana)' : 'Espanol_Espana', u'Français (France)' : 'Francais',
        #                       u'Português (Brasil)' : 'Portugues', u'English' : 'English', u'Español' : 'Espanol',
        #                       u'Türkçe' : 'Turkce', u'Italiano' : 'Italiano', u'العربية' : 'Arabic',
        #                       u'Deutsch' : 'Deutsch', u'Русский' : 'Russian'}[config_['language2']]
        if config_['language'] == 'Espanol_Espana':
            config_['language'] = 'Espanol (Espana)'
        if config_['language2'] == 'Espanol_Espana':
            config_['language2'] = 'Espanol (Espana)'
        #print(config_)
        menu_test.varible_pool_.update(config_)
        menu_test.redraw()

    def multiitem_config_q_old(list_t=[],return_list_t=[],item__=None):
        #print(list_t)
        #print(return_list_t)
        #print(item__)
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
    lang_list_t = ['''\x1b[32m'''+'''English'''+'''\x1b[0m''','''\x1b[32m'''+'''Espanol'''+'''\x1b[0m''',
                   '''\x1b[32m'''+'''Espanol (Espana)'''+'''\x1b[0m''','''\x1b[32m'''+'''Francais'''+'''\x1b[0m''',
                   '''\x1b[32m'''+'''Portugues'''+'''\x1b[0m''','''\x1b[32m'''+'''Turkce'''+'''\x1b[0m''',
                   '''\x1b[32m'''+'''Italiano'''+'''\x1b[0m''','''\x1b[32m'''+'''Arabic'''+'''\x1b[0m''',
                   '''\x1b[32m'''+'''Deutsch'''+'''\x1b[0m''','''\x1b[32m'''+'''Russian'''+'''\x1b[0m''']
    lang_list_ = ['English','Espanol','Espanol_Espana','Francais','Portugues','Turkce','Italiano','Arabic','Deutsch','Russian']

    def multiitem_config_q_(list_t=[],return_list_t=[],item__=None):
        #item__ = menu_test.multiselection_menue_('vquality', 'Video Quality:',vquality_sub, list_t,parent_='setting')
        item__ = menu_test.run_menu('vquality')
        if not item__ is None:
            #return_list_t[list_t.index(item__)]
            #print(return_list_t[list_t.index(item__)])
            if not return_list_t == [] and len(list_t) == len(return_list_t):
                load_config(video_quality=return_list_t[list_t.index(item__)])
            else:
                load_config(video_quality=item__)
            
    def multiitem_config_l1(list_t=[],return_list_t=[],item__=None):
        #item__ = menu_test.multiselection_menue_('language1', 'Language:', lang1_sub, list_t,parent_='setting')
        item__ = menu_test.run_menu('language1')
        if not item__ is None:
            if not return_list_t == [] and len(list_t) == len(return_list_t):
                load_config(language=return_list_t[list_t.index(item__)])
            else:
                load_config(language=item__)

    def multiitem_config_l2(list_t=[],return_list_t=[],item__=None):
        #item__ = menu_test.multiselection_menue_('language2', 'Language:', lang2_sub, list_t,parent_='setting')
        item__ = menu_test.run_menu('language2')
        if not item__ is None:
            if not return_list_t == [] and len(list_t) == len(return_list_t):
                load_config(language2=return_list_t[list_t.index(item__)])
            else:
                load_config(language2=item__)


        
    #menu_test.frame_ =['*','*','*','*','*','*']
    menu_test.main_menu_(Title,Subtitle,exit_option_call_text_='000|0|')
    #menu_test.menus_functions_internal_.update(
    #menu_test.main_menu_(Title,Subtitle)
    menu_test.add_menu_('setting', 'Settings:', exit_option_text='Back', parent_='Main')
    #menu_test.add_menu_('vquality', 'Video Quality:', exit_option_text='Back', parent_='setting')
    #menu_test.add_multiselection_menue_('vquality', 'Video Quality:',vquality_sub, quality_list_t, quality_list_,multiitem_config_q, parent_='setting')
    #menu_test.add_menu_('language1', 'Language:', lang1_sub, exit_option_text='Back', parent_='setting')
    #menu_test.add_multiselection_menue_('language1', 'Language:', lang1_sub, lang_list_t, lang_list_,multiitem_config_l1, parent_='setting')
    #menu_test.add_multiselection_menue_('language2', 'Language:', lang2_sub, lang_list_t, lang_list_,multiitem_config_l2, parent_='setting')
    #menu_test.add_menu_('language2', 'Language:', lang2_sub, exit_option_text='Back', parent_='setting')
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
    menu_test.add_function('Main','\x1b[31m'+'update'+ '\x1b[0m',print,['lol2'],call_text_='111')
    menu_test.add_function('Main','Settings',menu_test.run_menu,['setting'],call_text_='999',reposition=True)

    #menu_test.add_function('setting','''Video Quality = \x1b[32m'''+menu_test.varible_pool_['video_quality']+'''\x1b[0m''',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting',
    #                       ['''Video Quality = \x1b[32m''',(menu_test.varible_pool_,'video_quality'),'''\x1b[0m'''],
    #                       menu_test.run_menu,['vquality'])
    menu_test.add_function('setting',
                           ['''Video Quality = \x1b[32m''',(menu_test.varible_pool_,'video_quality'),'''\x1b[0m'''],
                           multiitem_config_q_,[quality_list_t,quality_list_],reposition=True)
    #menu_test.add_function('setting','Primary Language',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting',
    #                       ['''Primary Language = \x1b[32m''',(menu_test.varible_pool_,'language'),'''\x1b[0m'''],
    #                       menu_test.run_menu,['language1'])
    menu_test.add_function('setting',
                           ['''Primary Language = \x1b[32m''',(menu_test.varible_pool_,'language'),'''\x1b[0m'''],
                           multiitem_config_l1,[lang_list_t,lang_list_],reposition=True)
    #menu_test.add_function('setting','Secondary Language',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting',
    #                       ['''Secondary Language = \x1b[32m''',(menu_test.varible_pool_,'language2'),'''\x1b[0m'''],
    #                       menu_test.run_menu,['language2'])
    menu_test.add_function('setting',
                           ['''Primary Language = \x1b[32m''',(menu_test.varible_pool_,'language2'),'''\x1b[0m'''],
                           multiitem_config_l2,[lang_list_t,lang_list_],reposition=True)
    #menu_test.add_function('setting',
    #                       ['''Hard Subtitle = ''',('\x1b[32m'+str(menu_test.varible_pool_['forcesubtitle'])+'\x1b[0m' if menu_test.varible_pool_['forcesubtitle'] else '\x1b[31m'+str(menu_test.varible_pool_['forcesubtitle'])+'\x1b[0m'),''' #The Video will have 1 hard subtitle'''],
    #                       load_config,[],{'forcesubtitle':'toggle'})
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
    
    #menu_test.add_function('setting','Only One Subtitle',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting','Dub Filter',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting','Change the Number of The Download Connection',menu_test.run_menu,['vquality'])
    #menu_test.add_function('setting','use proxy(it disable if left blank',menu_test.run_menu,['vquality'])
    menu_test.add_function('setting','Restore Default Settings',load_config,[],{'defult':True},reposition=True)
    #menu_test.menus_functions_internal_['Main']['[EXIT]'] = ['000','0','']

    

    
    menu_test.start_()


    #multiitem_config_q_(quality_list_t,quality_list_)
