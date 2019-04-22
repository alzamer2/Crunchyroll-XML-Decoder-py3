#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import errno
import m3u8
import urllib
import socket
import os
import threading
from time import sleep
import math
import time
import subprocess
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
#from backports.shutil_get_terminal_size import get_terminal_size
from pager import _windows_get_window_size as get_terminal_size
from colorama import Fore, Style, init
from urllib.parse import urljoin,urlparse
import codecs
import re
init()

blocksize = 16384

class output_offset_cls():
    size = 0
    offset = 0
    part_size = {}
    part_offset = {}
    progress_bar_print = ['']
    start_t = time.process_time()
    printing = False

def compute_total_size_part(session, output_offset, url, n):
    with session.head(url) as response:
        output_offset.part_size[n] = response.headers['Content-Length']

def compute_total_size(video,tasks,output_offset,connection_n):
    with requests.session() as session:
        for n in range(len(video)-1,-1,-1):
            finished_download_ = True
            for i in threading.enumerate():
                if i.name == 'download_thread_':
                    finished_download_ = finished_download_ and not i.is_alive()
            if finished_download_:
                break
            if not str(video[n].media_sequence) in output_offset.part_size:
                compute_total_size_part(session, output_offset, video[n].absolute_uri, str(video[n].media_sequence))

def download_part(session, url,output, key, media_sequence,output_offset, tasks):
    if key.iv is not None:
        iv = str(key.iv)[2:]
    else:
        iv = "%032x" % media_sequence
    backend = default_backend()
    decode_hex = codecs.getdecoder("hex_codec")
    aes = Cipher(algorithms.AES(key.key_value), modes.CBC(decode_hex(iv)[0]), backend=backend)
    decryptor = aes.decryptor()
    output_offset.part_offset[str(media_sequence)] = 0
    with session.get(url, stream=True) as response:
        response.raise_for_status()
        filename = output
        output_offset.part_size[str(media_sequence)] = response.headers['Content-Length']
        with open(filename, 'ab') as f_handle:
            for chunk in response.iter_content(chunk_size=blocksize):
                output_offset.offset += len(chunk)
                output_offset.part_offset[str(media_sequence)] += len(chunk)
                total_size = 0
            
                finished_calculating_ = True
                for i in threading.enumerate():
                    if i.name == 'compute_total_size_thread_':
                        finished_calculating_ = finished_calculating_ and not i.is_alive()
                if not finished_calculating_:
                    output_offset.progress_bar_print[0] = progress_bar_(output_offset.offset, output_offset.offset+1, size_adj(output_offset.offset, 'harddisk'),
                                                                        '    @ ' + str(size_adj(output_offset.offset/(time.process_time()-output_offset.start_t), 'internet')),
                                                                        text_end_lenght=17, center_bgc='', defult_bgc='' )
                else:
                    for part_size in output_offset.part_size.values():
                        total_size += int(part_size)
                    output_offset.progress_bar_print[0] = progress_bar_(output_offset.offset,total_size,size_adj(output_offset.offset, 'harddisk')+'/'+size_adj(total_size, 'harddisk'),
                                                                        '%'+str(round(output_offset.offset * 100 / total_size)) + ' @ ' + str(size_adj(output_offset.offset/(time.process_time()-output_offset.start_t), 'internet')),text_end_lenght=17)
                output_offset.progress_bar_print[tasks.index(threading.currentThread())+1] = progress_bar_(output_offset.part_offset[str(media_sequence)],int(response.headers['Content-Length']),
                                                                                             'Part#'+str(media_sequence),'%'+str(round(output_offset.part_offset[str(media_sequence)] * 100 / int(response.headers['Content-Length']),2))+' ',text_end_lenght=17)
                if not output_offset.printing:
                    output_offset.printing = True
                    print('\n'.join(output_offset.progress_bar_print)+'\033[A'*len(output_offset.progress_bar_print)+'\x0d')
                    output_offset.printing = False
                if chunk:
                    f_handle.write(decryptor.update(chunk))
            decryptor.finalize()
        return filename

def download_thread(video,output,key,output_offset, tasks):
    with requests.session() as session:
        for n, seg in enumerate(video):
            download_part(session, seg.absolute_uri,output, key, seg.media_sequence,output_offset, tasks)

def fetch_streams(output, video, connection_n):
    tasks = []
    output_offset = output_offset_cls
    
    output_offset.size = 0
    output_offset.offset = 0
    output_offset.part_size = {}
    output_offset.part_offset = {}
    output_offset.progress_bar_print = ['']
    output_offset.start_t = time.process_time()
    output_offset.printing = False

    for n, seg in enumerate(video.segments):
        seg.media_sequence=video.media_sequence+n

    for n, i in enumerate(range(0,len(video.segments),math.ceil(len(video.segments)/connection_n))):
        output_offset.progress_bar_print.append('')
        if hasattr(video, 'key'):
            task = threading.Thread(target=download_thread,name='download_thread_',args=(video.segments[i:i+math.ceil(len(video.segments)/connection_n)],
                                                                 output+str(n), video.key, output_offset, tasks))
        else:
            task = threading.Thread(target=download_thread,name='download_thread_',args=(video.segments[i:i+math.ceil(len(video.segments)/connection_n)],
                                                                 output+str(n), video.keys[0], output_offset, tasks))
        tasks.append(task)
    for n, i in enumerate(range(0,len(video.segments),math.ceil(len(video.segments)/connection_n))):
        task = threading.Thread(target=compute_total_size,name='compute_total_size_thread_',args=(video.segments[i:i+math.ceil(len(video.segments)/connection_n)],
                                 tasks, output_offset,connection_n))
        tasks.append(task)
    for x in tasks:
        x.start()
    for x in tasks:
        x.join()

    print('\n'*len(output_offset.progress_bar_print))
    if connection_n==1:
        os.rename(output+'0',output)
    else:
        with open(output, 'ab') as outfile:
            for i in range (0, connection_n):
                fname = output+str(i)
                with open(fname, 'rb') as infile:
                    while True:
                        byte = infile.read(blocksize)
                        if not byte:
                            break
                        outfile.write(byte)
                os.remove(fname)
        
    


##########################################################################################:---      
##########################################################################################:---      Functions
##########################################################################################:---

def progress_bar_(currect,target,text_center='',text_end='%100',text_end_lenght=0,center_bgc='30;42',defult_bgc=''):
    try:
        c_width = get_terminal_size()[0]
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

def video_hls(uri, output, connection_n):
    video = find_best_video(uri)
    fetch_encryption_key(video)
    fetch_streams(output, video, connection_n)


##########################################################################################:---      
##########################################################################################:---      Main
##########################################################################################:---
    
if __name__ == '__main__':
    connection_n = 1
    try:
        #uri = sys.argv[1]
        uri = 'https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/master.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMzAwOS5tcDQsMjEzMzAyNS5tcDQsMjEzMjk5My5tcDQsMjEzMjk3Ny5tcDQsMTAzODk0My5tcDQsLnVybHNldC9tYXN0ZXIubTN1OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU1NTE4MDMyOX19fV19&Signature=U-Gm-f6fVCKgtW86WPhCiD0B9dykPkjt77XLQtjPoUh9IrmED-XHtinpkKUcGeuC4omVRDjDHod7UdUzXDM346uMGRvC2O2mQLaTPhP6w2qNk0IJu13RLf8~svomxiwTPJgBoQ-HZQ8RPFe0GMPDq2z-5E1O0XoONucT3g7i8fTwbh~DHgME-IImKbINh9tXAgT8PxQV5Fui7xNoSTBT89-KrnkCNTtomkdYQlhI8W8BiFwLbDSsNabA2WSJeYaobnwVyemSNAa5tZtrYaTx~fZ-n5BVOR~ydob~L9qMRYeiKUI472suT~CapWaJcV8COGOyz0y8PX9NgE4WiqGBOw__&Key-Pair-Id=DLVR'
    except:
        #open('page.html','wb').write(re.findall(b'vilos\.config\.media = ({.*})',requests.get('http://www.crunchyroll.com/military/episode-1-the-mission-begins-668503').content)[0])
        print("invalid url")
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

    video_hls(uri, output, connection_n)
