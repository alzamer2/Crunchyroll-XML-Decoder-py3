#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#version 1.1
import sys
import re
import m3u8
import tempfile
import urllib
import os, shutil
import threading
import math
import time
import requests
import json
import ssl
import certifi
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pager import _windows_get_window_size as get_terminal_size
from colorama import Fore, Style, init
from urllib.parse import urljoin,urlparse
import codecs
init()

blocksize = 16384

class video_hls():
    
    def __init__(self):
        self.size = 0
        self.offset = 0
        self.part_size = {}
        self.part_offset = {}
        self.part_filename = {}
        self.progress_bar_print = ['']
        self.progress_bar_arg = ['']
        self.start_t = time.process_time()
        self.printing = True
        self.download_url_list = list()
        self.printing = True
        #print_funct = print
    
    #def print(*arg,**kwarg):
    #    if not self.disable_printing:
    #        print_funct(*arg,**kwarg)

    def compute_total_size_part(self, url, n):
        with self.session_size.head(url) as response:
            self.part_size[n] = int(response.headers['Content-Length'])

    def compute_total_size(self):
        with requests.session() as self.session_size:
            while len(self.compute_total_size_urls) > 0:
                finished_download_ = True
                for thread in threading.enumerate():
                    if 'download_thread_' in thread.name:
                        finished_download_ = finished_download_ and not thread.is_alive()
                if finished_download_:
                    break
                sequence, url = self.compute_total_size_urls.pop()
                if not str(sequence) in self.part_size:
                    self.compute_total_size_part(url, str(sequence))

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
                            self.part_offset[str(media_sequence)] += len(chunk)
                            part_offset += len(chunk)
                            self.part_offset[str(media_sequence)] += len(chunk)
                            total_size = 0

                            finished_calculating_ = True
                            for thread in threading.enumerate():
                                if thread.name == 'compute_total_size_thread_':
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
                            
                            #if not self.disable_printing:
                                #if not self.printing:
                                    #self.printing = True
                                    #print('\n'.join(self.progress_bar_print)+'\033[A'*len(self.progress_bar_print)+'\x0d')
                                    #self.printing = False
                            if chunk:
                                f_handle.write(decryptor.update(chunk))
                        decryptor.finalize()
                    return filename
                except:
                    #retry -= 1
                    retry = 0 
                      

    def save_progress(self, output):
        with open(os.path.join(output, 'progress_hls.log'), 'w') as progressfile:
            while True:
                progressfile.seek(0)
                progressdata = dict()
                progressdata['part_offset'] = dict()
                for filename_key, filename_value in self.part_filename.items():
                    if filename_key in self.part_offset and filename_key in self.part_size:
                        progressdata['part_offset'][filename_key] = (filename_value, self.part_offset[filename_key], self.part_size[filename_key])

                progressdata['part_size'] = self.part_size
                progressfile.write(json.dumps(progressdata,indent=4,sort_keys=True))
                still_downloading = False
                for task_ in self.tasks1:
                    still_downloading = still_downloading or task_.is_alive()
                if not still_downloading:
                    break
                time.sleep(0.1)
        

    def print_progress(self):
        if not self.printing:
            return
        total_start_time = time.process_time()
        while True:
            still_downloading = False
            for task_ in self.tasks1:
                still_downloading = still_downloading or task_.is_alive()
            if total_start_time != time.process_time():
                total_speed = str(size_adj(self.offset/(time.process_time()-total_start_time), 'internet'))
            else:
                total_speed = str(size_adj(0, 'internet'))

            finished_calculating_ = True
            for thread in threading.enumerate():
                if 'compute_total_size_thread_' in thread.name:
                    finished_calculating_ = finished_calculating_ and not thread.is_alive()

            if not finished_calculating_:
                print_kwargs = {'currect':self.offset,
                'target': self.offset+1,
                'text_center': size_adj(self.offset, 'harddisk'),
                'text_end': f'    @ {total_speed}',
                'text_end_lenght':19,
                'center_bgc': '',
                'defult_bgc': ''
                }
            else:
                total_size = sum(self.part_size.values())
                print_kwargs = {'currect':self.offset,
                'target': total_size,
                'text_center': f"{size_adj(self.offset, 'harddisk')}/{size_adj(total_size, 'harddisk')}",
                'text_end': f"%{round(self.offset * 100 / total_size)} @ {size_adj(self.offset/(time.process_time()-self.start_t), 'internet')}",
                'text_end_lenght':19
                }


            #print(progress_bar_(**print_kwargs))
            temp_progress_bar_print = [progress_bar_(**print_kwargs)] + self.progress_bar_print
            for print_line in temp_progress_bar_print:
                print(print_line)
            print('\033[A'*(len(temp_progress_bar_print)+1))
            #print(self.tasks1)
            if not still_downloading:
                print('\n'*(len(temp_progress_bar_print)+1))
                break
            time.sleep(0.1)


    def download_thread(self, output):
        #with requests.session() as self.session:
        #    for n, seg in enumerate(video):
        #        self.download_part(seg.absolute_uri, output, key, seg.media_sequence, self.tasks1)
        if hasattr(self.video, 'key'):
            key = self.video.key
        else:
            key = self.video.keys[0]
        backend = default_backend()
        decode_hex = codecs.getdecoder("hex_codec")
        while len(self.download_url_list) >0:
            sequence, url = self.download_url_list.pop(0)
            if str(sequence) in self.part_offset and str(sequence) in self.part_size:
                if self.part_offset[str(sequence)] == self.part_size[str(sequence)]:
                    continue
            filename = os.path.join(output,os.path.split(urlparse(url).path)[1])
            self.part_filename[str(sequence)] = filename
            self.part_offset[str(sequence)] = 0
            decryptor = None
            if key:
                if key.iv is not None:
                    iv = str(key.iv)[2:]
                else:
                    iv = "%032x" % sequence
                aes = Cipher(algorithms.AES(key.key_value), modes.CBC(decode_hex(iv)[0]), backend=backend)
                decryptor = aes.decryptor()
            with self.session.get(url, stream=True) as response:
                response.raise_for_status()
                self.part_size[str(sequence)] = int(response.headers['Content-Length'])
                with open(filename, 'ab') as f_handle:
                    self.part_offset[str(sequence)] = 0
                    part_start_time = time.process_time()
                    for chunk in response.iter_content(chunk_size=blocksize):
                        self.offset += len(chunk)
                        self.part_offset[str(sequence)] += len(chunk)
                        total_size = 0
                        if part_start_time != time.process_time():
                            part_speed = str(size_adj(self.offset/(time.process_time()-part_start_time), 'internet'))
                        else:
                            part_speed = str(size_adj(0, 'internet'))
                        index_thread_ = int(threading.current_thread().name.replace('download_thread_',''))
                        print_kwargs = {'currect':self.part_offset[str(sequence)],
                        'target': self.part_size[str(sequence)],
                        'text_center': f'Part#{sequence} [{size_adj(self.part_offset[str(sequence)], "harddisk")}/{size_adj(self.part_size[str(sequence)], "harddisk")}]',
                        'text_end': f'% {round(self.part_offset[str(sequence)] * 100 / int(self.part_size[str(sequence)]),2)} @ {part_speed}',
                        'text_end_lenght':19
                        }
                        self.progress_bar_print[index_thread_] = progress_bar_(**print_kwargs)
                        if chunk:
                            if decryptor:
                                f_handle.write(decryptor.update(chunk))
                            else:
                                f_handle.write(chunk)
                    if decryptor:
                        decryptor.finalize()
                    self.part_offset[str(sequence)] = self.part_size[str(sequence)]
                #return filename

    def look_for_old_parts(self, new_dir_):
        old_progress = {}
        old_progress_dir = ''
        for fname in os.listdir(os.path.split(self.output)[0]):
            if fname.startswith(os.path.split(self.output)[1]) and os.path.isdir(os.path.join(os.path.split(self.output)[0],fname)):
                if os.path.lexists(os.path.join(os.path.split(self.output)[0],fname,'progress_hls.log')):
                    old_progress_dir = os.path.join(os.path.split(self.output)[0],fname)
                    old_progress = json.load(open(os.path.join(old_progress_dir,'progress_hls.log')))

        if old_progress == {}:
            return
        for old_part_size_key, old_part_size_value in old_progress['part_size'].items():
            self.part_size[old_part_size_key] = old_part_size_value
        for old_part_offset_key, old_part_offset_value in old_progress['part_offset'].items():
            if old_part_offset_value[1] == old_part_offset_value[2]:
                shutil.move(old_part_offset_value[0], os.path.join(new_dir_,os.path.split(old_part_offset_value[0])[1]))
                self.part_filename[old_part_offset_key] = os.path.join(new_dir_,os.path.split(old_part_offset_value[0])[1])
                self.part_offset[old_part_offset_key] = old_part_offset_value[1]
                self.offset += self.part_offset[old_part_offset_key]

        

        shutil.rmtree(old_progress_dir)
        #input()




    def fetch_streams(self):
        self.tasks1 = []

        if len(self.video.segments)/self.connection_n <2:       #fix when m2u8 parts are few
            self.connection_n = len(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n)))

        for n, seg in enumerate(self.video.segments):
            seg.media_sequence = self.video.media_sequence+n
        self.progress_bar_print = ['']*(self.connection_n+1)
        self.download_url_list = list()

        with tempfile.TemporaryDirectory(dir=os.path.split(self.output)[0],prefix=os.path.split(self.output)[1]) as tempD_:
            self.look_for_old_parts(tempD_)
            with requests.session() as self.session:
                print_task = threading.Thread(target=self.print_progress,name='print_thread_')
                save_progres_task = threading.Thread(target=self.save_progress,name='save_progress_thread_', args=([tempD_]))
                for seg in self.video.segments:
                    self.download_url_list += [(seg.media_sequence, seg.absolute_uri)]
                vfiles = [os.path.split(urlparse(url_[1]).path)[1] for url_ in self.download_url_list]
                self.compute_total_size_urls = list(self.download_url_list)
                for n in range(0,self.connection_n):
                    task = threading.Thread(target=self.download_thread,name=f'download_thread_{n}', args=([tempD_]))
                    taskc = threading.Thread(target=self.compute_total_size,name=f'compute_total_size_thread_{n}')
                    self.tasks1.append(task)
                    self.tasks1.append(taskc)
                
                for x in self.tasks1:
                    x.start()

                print_task.start()
                save_progres_task.start()
                for x in self.tasks1:
                    x.join()
                print_task.join()
                save_progres_task.join()
                with open(self.output, 'wb') as outfile:
                    for fname in vfiles:
                                                                                                                                
                        with open(os.path.join(tempD_, fname), 'rb') as infile:
                            while True:
                                byte = infile.read(blocksize)
                                if not byte:
                                    break
                                outfile.write(byte)

        #for n, i in enumerate(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n))):
        #    self.progress_bar_print.append('')
        #    self.progress_bar_arg.append('')
        #    self.progress_bar_arg.append('')
        #    if hasattr(self.video, 'key'):
        #        task = threading.Thread(target=self.download_thread,name='download_thread_',args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)],
        #                                                             self.output+str(n), self.video.key))
        #    else:
        #        task = threading.Thread(target=self.download_thread,name='download_thread_',args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)],
        #                                                             self.output+str(n), self.video.keys[0]))
        #    self.tasks1.append(task)
        #for n, i in enumerate(range(0,len(self.video.segments),math.ceil(len(self.video.segments)/self.connection_n))):
        #    task = threading.Thread(target=self.compute_total_size,name='compute_total_size_thread_',
        #                            args=(self.video.segments[i:i+math.ceil(len(self.video.segments)/self.connection_n)]))
        #    self.tasks1.append(task)
        #for x in self.tasks1:
        #    x.start()
        #for x in self.tasks1:
        #    x.join()

        #print('\n'*len(self.progress_bar_print))
        #if not self.disable_printing:
        #    print('\n'*len(self.progress_bar_print))
        #if self.connection_n==1:
        #    os.rename(self.output+'0',self.output)


    def fetch_encryption_key(self, video):
        if hasattr(video, 'key'):
            assert video.key.method == 'AES-128'
            try:
                video.key.key_value = urllib.urlopen(url = video.key.uri).read()
            except:
                video.key.key_value = requests.get(video.keys[0].uri).text.encode('windows-1252')
        else:
            if video.keys[0]:
                assert video.keys[0].method == 'AES-128'
                try:
                    video.keys[0].key_value = urllib.urlopen(url = video.keys[0].uri).read()
                except:
                    video.keys[0].key_value = requests.get(video.keys[0].uri).text.encode('windows-1252')

    def find_best_video(self, uri, kwargs):
        try:
            playlist = m3u8.load(uri, http_client=RequestsClient())
        except urllib.error.URLError:
           m3u8._load_from_uri = CERTIFICATE_VERIFY_FAILED_monkeypatching
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
        self.video = self.find_best_video(self.url_, kwargs)
        self.fetch_encryption_key(self.video)
        self.fetch_streams()
        return 0
        

##########################################################################################:---      
##########################################################################################:---      Functions
##########################################################################################:---

def progress_bar_(currect,target,text_center='',text_end='%100',text_end_lenght=0,center_bgc='30;42',defult_bgc=''):
    currect = float(currect)
    target = float(target)
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
    marker_pos = round(currect * c_width_croped / target)
    progress_b = f'{text_center:^{c_width_croped}}|{text_end:<{text_end_lenght}}'
    progress_b = f'\033[{center_bgc}m{progress_b[:marker_pos]}\033[{defult_bgc}m{progress_b[marker_pos:]}'

    return progress_b

def size_adj(size_, x_):
    size_ = int(size_)  #make sure size_ is int
                                    
    size_out_ = size_
    size_adj_dict = {
        'harddisk': {'round': 0, 'base': 1024,
        'suf': [' bytes', 'KB', 'MB', 'GB']},
        'internet': {'round': 2, 'base': 1024,
        'suf': ['b/s', 'Kb/s', 'Mb/s', 'Gb/s']}
    }
    for pow in range(1,len(size_adj_dict[x_]['suf'])+1):
        if size_ /(size_adj_dict[x_]['base']**pow) <= 1:
            temp_size_out_ = size_ /(size_adj_dict[x_]['base']**(pow-1))
            temp_size_out_intlen = len(str(int(temp_size_out_)))
            if temp_size_out_intlen <= 2:
                size_adj_dict[x_]['round'] = 2
            elif temp_size_out_intlen == 3:
                size_adj_dict[x_]['round'] = 1
            else:
                size_adj_dict[x_]['round'] = 0
            size_out_ = f'{temp_size_out_:.{size_adj_dict[x_]["round"]}f}{size_adj_dict[x_]["suf"][pow-1]}'
            break
    return size_out_

class RequestsClient():
    def download(self, uri, timeout=None, headers={}, verify_ssl=True):
        o = requests.get(uri, timeout=timeout, headers=headers)
        base_url = os.path.split(o.url)[0]
        return o.text, base_url

def CERTIFICATE_VERIFY_FAILED_monkeypatching(uri, timeout=None, headers={}):
    request = m3u8.Request(uri, headers=headers)
    resource = m3u8.urlopen(request, timeout=timeout, context=ssl.create_default_context(cafile=certifi.where()))
    base_uri = m3u8._parsed_url(resource.geturl())
    if m3u8.PYTHON_MAJOR_VERSION < (3,):
        content = m3u8._read_python2x(resource)
    else:
        content = m3u8._read_python3x(resource)
    return m3u8.M3U8(content, base_uri=base_uri)


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
        
