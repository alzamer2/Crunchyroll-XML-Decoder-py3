#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
import m3u8
import urllib
import os
import threading
import math
import time
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pager import _windows_get_window_size as get_terminal_size
from colorama import Fore, Style, init
from urllib.parse import urljoin,urlparse
import codecs
init()

blocksize = 16384

class video_hls():
    
    ef __init__(self):
        self.size = 0
        self.offset = 0
        self.part_size = {}
        self.part_offset = {}
        self.progress_bar_print = ['']
        self.progress_bar_arg = ['']
        self.start_t = time.process_time()
        self.printing = False
        self.disable_printing = False
        #print_funct = print
    
    #def print(*arg,**kwarg):
    #    if not self.disable_printing:
    #        print_funct(*arg,**kwarg)

    def compute_total_size_part(self, url, n):
        with self.session_size.head(url) as response:
            self.part_size[n] = response.headers['Content-Length']

    def compute_total_size(self, *video):
        with requests.session() as self.session_size:
            for n in range(len(video)-1,-1,-1):
                finished_download_ = True
                for i in threading.enumerate():
                    if i.name == 'download_thread_':
                        finished_download_ = finished_download_ and not i.is_alive()
                if finished_download_:
                    break
                if not str(video[n].media_sequence) in self.part_size:
                    self.compute_total_size_part(video[n].absolute_uri, str(video[n].media_sequence))

    def download_part(self, url, output, key, media_sequence, tasks):
        if key.iv is not None:
            iv = str(key.iv)[2:]
        else:
            iv = "%032x" % media_sequence
        backend = default_backend()
        decode_hex = codecs.getdecoder("hex_codec")
        aes = Cipher(algorithms.AES(key.key_value), modes.CBC(decode_hex(iv)[0]), backend=backend)
        decryptor = aes.decryptor()
        self.part_offset[str(media_sequence)] = 0
        filename = output
        with open(filename, 'ab+') as f_handle:
            #part_start_pos = f_handle.tell()
            retry = 5
            part_offset = 0
            while retry > 0:
                
                try:
                    header = {"Range": "bytes={}-".format(part_offset)}
                    with self.session.get(url,headers = header, stream=True) as response:
                        response.raise_for_status()
                        if not str(media_sequence) in self.part_size:
                            self.part_size[str(media_sequence)] = response.headers['Content-Length']
                        for chunk in response.iter_content(chunk_size=blocksize):
                            self.offset += len(chunk)
                            part_offset += len(chunk)
                            self.part_offset[str(media_sequence)] += len(chunk)
                            total_size = 0

                            finished_calculating_ = True
                            for i in threading.enumerate():
                                if i.name == 'compute_total_size_thread_':
                                    finished_calculating_ = finished_calculating_ and not i.is_alive()
                            if not finished_calculating_:
                                self.progress_bar_arg[0] = [self.offset, self.offset+1, size_adj(self.offset, 'harddisk'),
                                                            '     @{:>8}'.format(size_adj(self.offset/(time.process_time()-self.start_t), 'internet'))]
                                self.progress_bar_print[0] = progress_bar_(*self.progress_bar_arg[0],text_end_lenght=17, center_bgc='', defult_bgc='')
                            else:
                                for part_size in self.part_size.values():
                                    total_size += int(part_size)
                                self.progress_bar_arg[0] = [self.offset, total_size, '{}/{}'.format(size_adj(self.offset, 'harddisk'),size_adj(total_size, 'harddisk')),
                                                            '%{:<5.1f}@{:>8}'.format(round(self.offset * 100 / total_size),size_adj(self.offset/(time.process_time()-self.start_t), 'internet'))]
                                self.progress_bar_print[0] = progress_bar_(*self.progress_bar_arg[0],text_end_lenght=17)
                            self.progress_bar_arg[self.tasks1.index(threading.currentThread())+1] = [self.part_offset[str(media_sequence)], int(response.headers['Content-Length']),'Part#{}'.format(media_sequence),
                                                                                                     '%{} '.format(round(self.part_offset[str(media_sequence)] * 100 / int(response.headers['Content-Length']),2))]
                            self.progress_bar_print[self.tasks1.index(threading.currentThread())+1] = progress_bar_(*self.progress_bar_arg[self.tasks1.index(threading.currentThread())+1], text_end_lenght=17)
                            if not self.disable_printing:
                                if not self.printing:
                                    self.printing = True
                                    print('\n'.join(self.progress_bar_print)+'\033[A'*len(self.progress_bar_print)+'\x0d')
                                    self.printing = False
                            if chunk:
                                f_handle.write(decryptor.update(chunk))
                        decryptor.finalize()
                    return filename
                except:
                    retry -= 1
                      

    def download_thread(self, video, output, key):
        with requests.session() as self.session:
            for n, seg in enumerate(video):
                self.download_part(seg.absolute_uri, output, key, seg.media_sequence, self.tasks1)

    def fetch_streams(self):
        self.tasks1 = []

        if len(self.video.segments)/self.connection_n <2:       #fix when m2u8 parts are few
            self.connection_n = len(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n)))

        for n, seg in enumerate(self.video.segments):
            seg.media_sequence=self.video.media_sequence+n

        for n, i in enumerate(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n))):
            self.progress_bar_print.append('')
            self.progress_bar_arg.append('')
            self.progress_bar_arg.append('')
            if hasattr(self.video, 'key'):
                task = threading.Thread(target=self.download_thread,name='download_thread_',args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)],
                                                                     self.output+str(n), self.video.key))
            else:
                task = threading.Thread(target=self.download_thread,name='download_thread_',args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)],
                                                                     self.output+str(n), self.video.keys[0]))
            self.tasks1.append(task)
        for n, i in enumerate(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n))):
            task = threading.Thread(target=self.compute_total_size,name='compute_total_size_thread_',
                                    args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)]))
            self.tasks1.append(task)
        for x in self.tasks1:
            x.start()
        for x in self.tasks1:
            x.join()

        #print('\n'*len(self.progress_bar_print))
        if not self.disable_printing:
            print('\n'*len(self.progress_bar_print))
        if self.connection_n==1:
            os.rename(self.output+'0',self.output)
        else:
            with open(self.output, 'ab') as outfile:
                for fname in os.listdir(os.path.split(self.output)[0]):
                    if fname.startswith(os.path.split(self.output)[1]) and not fname.endswith(os.path.splitext(self.output)[1]):
                        with open(os.path.join(os.path.split(self.output)[0],fname), 'rb') as infile:
                            while True:
                                byte = infile.read(blocksize)
                                if not byte:
                                    break
                                outfile.write(byte)
                        os.remove(os.path.join(os.path.split(self.output)[0],fname))

    def fetch_encryption_key(self, video):
        if hasattr(video, 'key'):
            assert video.key.method == 'AES-128'
            try:
                video.key.key_value = urllib.urlopen(url = video.key.uri).read()
            except:
                video.key.key_value = requests.get(video.keys[0].uri).text.encode('windows-1252')
        else:
            assert video.keys[0].method == 'AES-128'
            try:
                video.keys[0].key_value = urllib.urlopen(url = video.keys[0].uri).read()
            except:
                video.keys[0].key_value = requests.get(video.keys[0].uri).text.encode('windows-1252')

    def find_best_video(self, uri, kwargs):
        playlist = m3u8.load(uri)
        if not playlist.is_variant:
            if urlparse(playlist.segments[0].uri).netloc == '':
                for n, seg in enumerate(playlist.segments):
                    seg.uri = seg.absolute_uri
            return playlist

        '''Parse kwargs'''
        parsed_kwargs = dict()
	## suported key: resolution, r, size, s, width, height, w, h, bandwidth
        suported_key = {'resolution' : 'r', 'r' : 'r', 'size' : 'r', 's' : 'r',
	                        'width' : 'w', 'w' : 'w', 'height' : 'h', 'h' : 'h',
	                        'bandwidth' : 'vbr', 'vbr' : 'vbr=',}
	## suported value: MAX, best, high, highest, low, lowest, worst, 0
        suported_value = {'MAX' : 'MAX','best': 'MAX','high': 'MAX','highest': 'MAX',
	                          'low' : 0, 'lowest' : 0, 'worst' : 0}
        def parse_value_r(value):
            if value in list(k.lower() for k in suported_value):
                return dict((k.lower(), suported_value[k]) for k in suported_value)[value]
            else:
                return int(re.fullmatch(r'(^\d+)(?:[pP]$|[Xx]\d+|$)',str(value)).group(1))
        def parse_value_w(value):
            if value in list(k.lower() for k in suported_value):
                return dict((k.lower(), suported_value[k]) for k in suported_value)[value]
            else:
                return int(re.fullmatch(r'(?:\d+[xX])?(\d+)[Pp]?$',str(value)).group(1))
        for key_ in kwargs:
            if key_ in list(k.lower() for k in suported_key):
                if suported_key[key_] == 'r':
                    value_ = parse_value_r(kwargs[key_])
                elif suported_key[key_] == 'h':
                    value_ = parse_value_r(kwargs[key_])
                elif suported_key[key_] == 'w':
                    value_ = parse_value_w(kwargs[key_])
                elif suported_key[key_] == 'vbr':
                    value_ = int(kwargs[key_])

                if not suported_key[key_] in parsed_kwargs:
                    parsed_kwargs[suported_key[key_]]= value_
                else:
                    if not parsed_kwargs[suported_key[key_]] == 'MAX':
                        if value_ == 'MAX':
                            parsed_kwargs[suported_key[key_]] = value_
                        elif value_ > parsed_kwargs[suported_key[key_]]:
                            parsed_kwargs[suported_key[key_]] = value_
        if kwargs == {}:
            parsed_kwargs = {'r':'MAX'}

        def st_best_streem(value_, compare='resolution'):
            seperated_playlists = list(playlist.playlists)
            ordered_playlists = list()
            while len(seperated_playlists) >1:
                best_stream = seperated_playlists[0]
                for stream in seperated_playlists:
                    if compare == 'resolution':
                        if stream.stream_info.resolution[0] > best_stream.stream_info.resolution[0]:
                            best_stream = stream
                    elif compare == 'width':
                        if stream.stream_info.resolution[1] > best_stream.stream_info.resolution[1]:
                            best_stream = stream
                    elif compare == 'bandwidth':
                        if stream.stream_info.bandwidth > best_stream.stream_info.bandwidth:
                            best_stream = stream
                ordered_playlists += [seperated_playlists.pop(seperated_playlists.index(best_stream))]
            best_stream = ordered_playlists[0]
            for stream in ordered_playlists:
                if compare == 'resolution':
                    if str(value_).lower() == 'MAX'.lower():
                        value_c = best_stream.stream_info.resolution[0]
                    else:
                        value_c = value_
                    if stream.stream_info.resolution[0] > value_c:
                        best_stream = stream
                elif compare == 'width':
                    if str(value_).lower() == 'MAX'.lower():
                        value_c = best_stream.stream_info.resolution[1]
                    else:
                        value_c = value_
                    if stream.stream_info.resolution[1] > value_c:
                        best_stream = stream
                elif compare == 'bandwidth':
                    if str(value_).lower() == 'MAX'.lower():
                        value_c = best_stream.stream_info.bandwidth
                    else:
                        value_c = value_
                    if stream.stream_info.bandwidth > value_c:
                        best_stream = stream
            return best_stream

        kwargs_streams = list()
        for key_ in parsed_kwargs:
            if key_ == 'r' or key_ == 'h':
                kwargs_streams +=[st_best_streem(parsed_kwargs[key_])]
            elif key_ == 'w':
                kwargs_streams +=[st_best_streem(parsed_kwargs[key_],'width')]
            elif key_ == 'vbr':
                kwargs_streams +=[st_best_streem(parsed_kwargs[key_],'bandwidth')]

        best_stream = kwargs_streams[0]
        for stream in kwargs_streams:
            if stream.stream_info.bandwidth == 'max' or stream.stream_info.bandwidth > best_stream.stream_info.bandwidth:
                best_stream = stream
        return self.find_best_video(best_stream.absolute_uri, kwargs)
    

    def video_hls(self, url = None, output = None, connection_n = 1, **kwargs):
        if 'idlelib.run' in sys.modules: #code to force this script to only run in console
            try:
                import run_code_with_console
                return run_code_with_console.run_code_with_console()
            except:
                pass                     #end of code to force this script to only run in console
        if url is None:
            url = input('HLS link>>')
        self.url_ = url
        if output is not None:
            self.output = os.path.abspath(output)
        else:
            self.output = os.path.abspath('download.mp4')
        self.connection_n = connection_n
        self.video = self.find_best_video(uri, kwargs)
        self.fetch_encryption_key(self.video)
        self.fetch_streams()
        return 0
        

##########################################################################################:---      
##########################################################################################:---      Functions
##########################################################################################:---

def progress_bar_(currect,target,text_center='',text_end='%100',text_end_lenght=0,center_bgc='30;42',defult_bgc=''):
    try:
        c_width = get_terminal_size()[0]
        if c_width ==0:
            c_width = 60
    except:
        c_width = 60
    if text_end_lenght == 0 :
        text_end_lenght = len(text_end)
    if text_end == '%100':
        text_end = '%{:.1f}'.format(currect*100/target)
        text_end_lenght = len('%100')
    c_width_croped = c_width - text_end_lenght - 3
    progress_b = '{text_center:^{padding}}\033[{d_bgc}m|{text_end:<{end_padding}}'.format(text_center= text_center, text_end= text_end,
                                                                                          padding= c_width_croped, d_bgc= defult_bgc, end_padding= text_end_lenght)
    marker_pos = round(currect * c_width_croped / target)
    progress_b = '\033[{c_bgc}m{}\033[{d_bgc}m{}{}'.format(progress_b[:marker_pos], progress_b[marker_pos:marker_pos+1],progress_b[marker_pos+1:],
                                                           c_bgc = center_bgc, d_bgc= defult_bgc)
    return progress_b

def size_adj(size_, x_):
    if x_ == 'harddisk':
        if size_/1024/1024/1024 > 1:
            size_out_ = '{:.{prec}f}GB'.format(size_/1024/1024/1024,
                                               prec=0 if len(str(int(size_/1024/1024/1024))) >=3 else 3-len(str(int(size_/1024/1024/1024))))
        elif size_/1024/1024 > 1:
            size_out_ = '{:.{prec}f}MB'.format(size_/1024/1024,
                                               prec=0 if len(str(int(size_/1024/1024))) >=3 else 3-len(str(int(size_/1024/1024))))
        elif size_/1024 > 1:
            size_out_ = '{:.{prec}f}KB'.format(size_/1024,
                                               prec=0 if len(str(int(size_/1024))) >=3 else 3-len(str(int(size_/1024))))
        else:
            size_out_ = '{}bytes'.format(size_)
    if x_ == 'internet':
        if size_/1024/1024/1024 > 1:
            size_out_ = '{:.{prec}f}Gb/s'.format(size_/1024/1024/1024,
                                                 prec=0 if len(str(int(size_/1024/1024/1024))) >=3 else 3-len(str(int(size_/1024/1024/1024))))
        elif size_/1024/1024 > 1:
            size_out_ = '{:.{prec}f}Mb/s'.format(size_/1024/1024,
                                                 prec=0 if len(str(int(size_/1024/1024))) >=3 else 3-len(str(int(size_/1024/1024))))
        elif size_/1024 > 1:
            size_out_ = '{:.{prec}f}Kb/s'.format(size_/1024,
                                                 prec=0 if len(str(int(size_/1024))) >=3 else 3-len(str(int(size_/1024))))
        else:
            size_out_ = '{}b/s'.format(size_)
    return size_out_

##########################################################################################:---      
##########################################################################################:---      Main
##########################################################################################:---
    
if __name__ == '__main__':
    connection_n = 1
    output = "download.ts"
    try:
        uri = sys.argv[1]
        #uri = 'https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2132995.mp4,2133011.mp4,2132979.mp4,2132963.mp4,1038945.mp4,.urlset/master.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMjk5NS5tcDQsMjEzMzAxMS5tcDQsMjEzMjk3OS5tcDQsMjEzMjk2My5tcDQsMTAzODk0NS5tcDQsLnVybHNldC9tYXN0ZXIubTN1OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU1ODY4MzI1Nn19fV19&Signature=pNFL3u8YuKwyK3glAI2jLfvHk981ieKDWRgMPw6elxJXzvYeDt6z-~uuh7lCBpTfYAASO2gvktDhAkyEjkBTRzPnCovyoYRIdOe6iriFRZ4kNP1TcuEKnNF3JTJ1IPll748eIVxjKwHw4QS2GXhozF0DQ89s2cOcELTQa572SZCiAJczm0shOWkq0hyI8sysBSVkmv1LYWdk0ZS1bNUmOf0p5zpoKlu807KecQJH9v2LLop1CFl99ryB~37Lgp7~9tJY9imVJ23COoRJue-Dgs752Ei2ytep4yiw4dQdUmx8SOGaXzMEv~J-fXQTe9Lz8NWBHMj0dQF0ALp3MaUgyw__&Key-Pair-Id=DLVR'
    except:
        raise Exception('invalid url')
    argv_cut = 2
    if len(sys.argv) >=3:
        if sys.argv[2].isdigit():
            connection_n = int(sys.argv[2])
            argv_cut = 3
        elif not '=' in sys.argv[2]:
            output = sys.argv[2]
            argv_cut = 3
    if len(sys.argv) >=4:
        if sys.argv[3].isdigit():
            connection_n = int(sys.argv[3])
            argv_cut = 4
        elif not '=' in sys.argv[3]:
            output = sys.argv[3]
            argv_cut = 4
    download_ = video_hls()
    #download_.disable_printing = True
    download_.video_hls(uri, output, connection_n,
                        **dict(arg.split('=') for arg in sys.argv[argv_cut:]))
    print(download_.progress_bar_arg)
        
