#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
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
    
    def __init__(self):
        self.size = 0
        self.offset = 0
        self.part_size = {}
        self.part_offset = {}
        self.progress_bar_print = ['']
        self.start_t = time.process_time()
        self.printing = False

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
        with self.session.get(url, stream=True) as response:
            response.raise_for_status()
            filename = output
            self.part_size[str(media_sequence)] = response.headers['Content-Length']
            with open(filename, 'ab') as f_handle:
                for chunk in response.iter_content(chunk_size=blocksize):
                    self.offset += len(chunk)
                    self.part_offset[str(media_sequence)] += len(chunk)
                    total_size = 0
                
                    finished_calculating_ = True
                    for i in threading.enumerate():
                        if i.name == 'compute_total_size_thread_':
                            finished_calculating_ = finished_calculating_ and not i.is_alive()
                    if not finished_calculating_:
                        self.progress_bar_print[0] = progress_bar_(self.offset, self.offset+1, size_adj(self.offset, 'harddisk'),
                                                                            '    @ ' + str(size_adj(self.offset/(time.process_time()-self.start_t), 'internet')),
                                                                            text_end_lenght=17, center_bgc='', defult_bgc='' )
                    else:
                        for part_size in self.part_size.values():
                            total_size += int(part_size)
                        self.progress_bar_print[0] = progress_bar_(self.offset,total_size,size_adj(self.offset, 'harddisk')+'/'+size_adj(total_size, 'harddisk'),
                                                                            '%'+str(round(self.offset * 100 / total_size)) + ' @ ' + str(size_adj(self.offset/(time.process_time()-self.start_t), 'internet')),text_end_lenght=17)
                    self.progress_bar_print[self.tasks1.index(threading.currentThread())+1] = progress_bar_(self.part_offset[str(media_sequence)],int(response.headers['Content-Length']),
                                                                                                 'Part#'+str(media_sequence),'%'+str(round(self.part_offset[str(media_sequence)] * 100 / int(response.headers['Content-Length']),2))+' ',text_end_lenght=17)
                    if not self.printing:
                        self.printing = True
                        print('\n'.join(self.progress_bar_print)+'\033[A'*len(self.progress_bar_print)+'\x0d')
                        self.printing = False
                    if chunk:
                        f_handle.write(decryptor.update(chunk))
                decryptor.finalize()
            return filename

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

        print('\n'*len(self.progress_bar_print))
        if self.connection_n==1:
            os.rename(self.output+'0',self.output)
        else:
            with open(self.output, 'ab') as outfile:
                for fname in os.listdir(os.path.split(self.output)[0]):
                    if fname.startswith(os.path.split(self.output)[1]) and not fname.endswith(os.path.splitext(self.output)[1]):
                        #print(fname)
                        with open(os.path.join(os.path.split(self.output)[0],fname), 'rb') as infile:
                            while True:
                                byte = infile.read(blocksize)
                                if not byte:
                                    break
                                outfile.write(byte)
                        os.remove(os.path.join(os.path.split(self.output)[0],fname))

    def video_hls(self, uri, output, connection_n):
        import sys
        if 'idlelib.run' in sys.modules: #code to force this script to only run in console
            try:
                import run_code_with_console
                return run_code_with_console.run_code_with_console()
            except:
                pass                     #end of code to force this script to only run in console
        self.video = find_best_video(uri)
        self.output = output
        self.connection_n = connection_n
        fetch_encryption_key(self.video)
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
    if text_end_lenght == 0 : text_end_lenght = len(text_end)
    if text_end == '%100':
        text_end = '%'+str(currect * 100 / target)
        text_end_lenght = len('%100')
        
    c_width_croped = c_width - text_end_lenght - 2
    Lpading = round((c_width_croped - len(text_center)) / 2)
    Rpading = round(c_width_croped - len(text_center) - Lpading)

    progress_b = ' ' * Lpading + text_center + ' ' * Rpading + '\033['+ defult_bgc + 'm' + '|' + text_end + ' ' * (text_end_lenght - len(text_end))
    marker_pos = round(currect * c_width_croped / target)
    progress_b = '\033['+ center_bgc + 'm' + progress_b[:marker_pos] + '\033['+ defult_bgc + 'm' + progress_b[marker_pos:marker_pos+1] + progress_b[marker_pos+1:]
    return progress_b

def size_adj(size_, x_):
    if x_ == 'harddisk':
        if size_/1024 > 1:
            if (size_/1024)/1024 > 1:
                if ((size_/1024)/1024)/1024 > 1:
                    size_out_ = str(round(((size_/1024)/1024)/1024))+'GB'
                else:
                    size_out_ = str(round((size_/1024)/1024))+'MB'
            else:
                size_out_ = str(round(size_/1024))+'KB'
        else:
            size_out_ = str(round(size_))+'bytes'
    if x_ == 'internet':
        if size_/1024 > 1:
            if (size_/1024)/1024 > 1:
                if ((size_/1024)/1024)/1024 > 1:
                    size_out_ = format(((size_/1024)/1024)/1024, '.2f')+'Gb/s'
                else:
                    size_out_ = format((size_/1024)/1024, '.2f')+'Mb/s'
            else:
                size_out_ = format(size_/1024, '.2f')+'Kb/s'
        else:
            size_out_ = format(size_, '.2f')+'b/s'
    return size_out_

def fetch_encryption_key(video):
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

def find_best_video(uri):
    playlist = m3u8.load(uri)
    if not playlist.is_variant:
        if urlparse(playlist.segments[0].uri).netloc == '':
            for n, seg in enumerate(playlist.segments):
                seg.uri = seg.absolute_uri
        return playlist
    best_stream = playlist.playlists[0]
    for stream in playlist.playlists:
        if stream.stream_info.bandwidth == 'max' or stream.stream_info.bandwidth > best_stream.stream_info.bandwidth:
            best_stream = stream
    return find_best_video(best_stream.absolute_uri)




##########################################################################################:---      
##########################################################################################:---      Main
##########################################################################################:---
    
if __name__ == '__main__':
    connection_n = 1
    try:
        uri = sys.argv[1]
        #uri = 'https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2132995.mp4,2133011.mp4,2132979.mp4,2132963.mp4,1038945.mp4,.urlset/master.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMjk5NS5tcDQsMjEzMzAxMS5tcDQsMjEzMjk3OS5tcDQsMjEzMjk2My5tcDQsMTAzODk0NS5tcDQsLnVybHNldC9tYXN0ZXIubTN1OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU1ODY4MzI1Nn19fV19&Signature=pNFL3u8YuKwyK3glAI2jLfvHk981ieKDWRgMPw6elxJXzvYeDt6z-~uuh7lCBpTfYAASO2gvktDhAkyEjkBTRzPnCovyoYRIdOe6iriFRZ4kNP1TcuEKnNF3JTJ1IPll748eIVxjKwHw4QS2GXhozF0DQ89s2cOcELTQa572SZCiAJczm0shOWkq0hyI8sysBSVkmv1LYWdk0ZS1bNUmOf0p5zpoKlu807KecQJH9v2LLop1CFl99ryB~37Lgp7~9tJY9imVJ23COoRJue-Dgs752Ei2ytep4yiw4dQdUmx8SOGaXzMEv~J-fXQTe9Lz8NWBHMj0dQF0ALp3MaUgyw__&Key-Pair-Id=DLVR'
    except:
        #import re;open('page.html','wb').write(re.findall(b'vilos\.config\.media = ({.*})',requests.get('http://www.crunchyroll.com/military/episode-1-the-mission-begins-668503').content)[0])
        print("invalid url")
        exit()
    try:
        if int(sys.argv[2]):
            connection_n = int(sys.argv[2])
    except:
        try:
            output = sys.argv[2]
        except:
            output = "download.ts"
    try:
        if int(sys.argv[3]):
            connection_n = int(sys.argv[3])
    except:
        try:
            output = sys.argv[3]

        except:
            if not 'output' in locals():
                output = "download.ts"

    download_ = video_hls()
    download_.video_hls(uri, output, connection_n)
