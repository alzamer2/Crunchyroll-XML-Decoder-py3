#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import errno
import m3u8
import urllib
#from Crypto.Cipher import AES
#import StringIO
import socket
import os
#from threading import Thread
import threading
from time import sleep
import math
import time
import subprocess
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from backports.shutil_get_terminal_size import get_terminal_size
from colorama import Fore, Style, init
from urllib.parse import urljoin,urlparse
import codecs
init()

blocksize = 16384

class resumable_fetch:
    def __init__(self, uri, cur, total):
        self.uri = uri
        self.cur = cur
        self.total = total
        self.offset = 0
        self._restart()
        try:
            self.file_size = int(self.stream.info().get('Content-Length', -1))
        except:
            self.file_size = int(self.stream.headers['content-length'])
        #print(self.file_size)
        if self.file_size <= 0:
            print("Invalid file size")
            sys.exit()

    def _progress(self):
        sys.stdout.write('\x1b[2K\r%d/%d' % (self.cur, self.total))
        sys.stdout.flush()

    def _restart(self):
        try:
            #import requstss2
            req = urllib.Request(self.uri)
            if self.offset:
                req.headers['Range'] = 'bytes=%s-' % (self.offset, )

            while True:
                try:
                    self.stream = urllib.urlopen(req, timeout = 180)
                    #print(self.stream)
                    break
                except socket.timeout:
                    continue
                except socket.error as e:
                    if e.errno != errno.ECONNRESET:
                        raise
        except:
            if self.offset:
                headers = {'Range': 'bytes=%s-' % (self.offset, )}
                req = requests.get(self.uri, headers=headers, stream=True, timeout = 180)
            else:
                req = requests.get(self.uri, stream=True, timeout = 180)

            while True:
                try:
                    self.stream = req.raw
                    break
                except socket.timeout:
                    continue
                except socket.error as e:
                    if e.errno != errno.ECONNRESET:
                        raise

    def read(self, n):
        buffer = []
        global download_size_
        global progress_bar_print
        download_size_1 = 0
        total_size_s_ = 0
        if not 'download_size_' in globals():
            download_size_ = [0]*self.total
        if not 'progress_bar_print' in globals():
            #progress_bar_print = ['','']
            progress_bar_print = [''] * (len(threads)+1)
        if not 'download_size_x' in globals():
            download_size_x = []
        download_size_[self.cur-1] = self.offset
        for i in download_size_:
            download_size_1 += i
        if total_size_t_.is_alive():
            total_size_s_ = 'C.Size'
        else:
            total_size_s_ = total_size
        #print(download_size_1,total_size_s_)
        if total_size_s_ == 'C.Size':
            progress_bar_print[0] = progress_bar_(download_size_1,download_size_1+1,size_adj(download_size_1, 'harddisk'),'    @ ' + str(size_adj(download_size_1/(time.process_time()-start_t), 'internet')),text_end_lenght=17,center_bgc='')
        else:
            progress_bar_print[0] = progress_bar_(download_size_1,total_size,size_adj(download_size_1, 'harddisk')+'/'+size_adj(total_size, 'harddisk'),'%'+str(round(download_size_1 * 100 / total_size)) + ' @ ' + str(size_adj(download_size_1/(time.process_time()-start_t), 'internet')),text_end_lenght=17)
        progress_bar_print[threads.index(threading.currentThread())+1] = progress_bar_(self.offset,self.file_size,'Part#'+str(self.cur),'%'+str(round(self.offset * 100 / self.file_size,2))+' ',text_end_lenght=17)
        #print(progress_bar_print[0]+'\n'+progress_bar_print[1]+(b'\x0d').decode()+(b'\033['+str(2)+'A'))
        #if len(download_size_)==len(download_size_x):
        #    for x in range(len(download_size_)):
        #        if not download_size_x[x]==download_size_[x]:
        #            progress_bar_print.append(progress_bar_(download_size_[x],total_size_s_[x],'Part#'+str(x+1),'%'+str(download_size_[x] * 100 / total_size_s_[x])+' ',text_end_lenght=17))
        #            download_size_x = download_size_
        #else:
        #    download_size_x = download_size_
        #print(progress_bar_print[0]+(b'\x0d').decode()+(b'\033[f'))
        #print(threads,threads[0].is_alive(),threading.currentThread(), threads.index(threading.currentThread()))
        progress_bar_print_final = ''
        for item_ in progress_bar_print:
            progress_bar_print_final += item_ + '\n'
        progress_bar_print_final +=(b'\x0d').decode()
        magic_trick = b''
        for item_ in progress_bar_print:
            magic_trick += (b'\033[A')
        magic_trick += (b'\033[A')
        for c_thread in threads:
            if c_thread.is_alive():
                if c_thread == threading.currentThread():
                    #print(threads.index(threading.currentThread()))
                    #print(progress_bar_print[0]+'\n'+progress_bar_print[1]+(b'\x0d').decode()+(b'\033[2A'))
                    #print(progress_bar_print_final,(b'\x0d').decode(),magic_trick.decode())
                    print(progress_bar_print_final+(b'\x0d').decode()+magic_trick.decode())
                break
            

        while self.offset < self.file_size:
            try:
                data = self.stream.read(min(n, self.file_size - self.offset))
                self.offset += len(data)
                n -= len(data)
                buffer.append(data)
                if n == 0 or data:
                        break
            except socket.timeout:
                self._progress()
                self._restart()
            except socket.error as e:
                if e.errno != errno.ECONNRESET:
                    raise
                self._progress()
                self._restart()
        return b''.join(buffer)
def progress_bar_(currect,target,text_center='',text_end='%100',text_end_lenght=0,center_bgc='30;42',defult_bgc=''):
    c_width= get_terminal_size()[0]
    if text_end_lenght == 0 : text_end_lenght = len(text_end)
    if text_end == '%100':
        text_end = '%'+str(currect * 100 / target)
        text_end_lenght = len('%100')
        
    c_width_croped = c_width - text_end_lenght - 2
    Lpading = round((c_width_croped - len(text_center)) / 2)
    Rpading = round(c_width_croped - len(text_center) - Lpading)
    #print(Lpading,text_center,Rpading,defult_bgc,text_end,(text_end_lenght - len(text_end)),currect * c_width_croped / target)

    progress_b = ' ' * Lpading + text_center + ' ' * Rpading + '\033['+ defult_bgc + 'm' + '|' + text_end + ' ' * (text_end_lenght - len(text_end))
    marker_pos = round(currect * c_width_croped / target)
    progress_b = '\033['+ center_bgc + 'm' + progress_b[:marker_pos] + '\033['+ defult_bgc + 'm' + progress_b[marker_pos:marker_pos+1] + progress_b[marker_pos+1:]
    return progress_b

def compute_total_size(video):
    global total_size
    global total_size_l_
    #global stop_threads 
    total_size = 0
    #stop_threads = False
    total_size_l_=[]
    for n, seg in enumerate(video.segments):
        try:
            req_1 = urllib.Request(seg.uri)
            stream_1 = urllib.urlopen(req_1, timeout = 180)
            total_size += int(stream_1.info().get('Content-Length', -1))
            total_size_l_.append(stream_1.info().get('Content-Length', -1))
        except:
            stream_1r = requests.head(seg.uri, timeout = 180).headers['content-length']
            total_size += int(stream_1r)
            total_size_l_.append(stream_1r)
        #print(total_size,total_size_l_,stop_threads)
        if stop_threads:
            break

def copy_with_decrypt(input, output, key, media_sequence):
    if key.iv is not None:
        iv = str(key.iv)[2:]
    else:
        iv = "%032x" % media_sequence
    backend = default_backend()
    decode_hex = codecs.getdecoder("hex_codec")
    #print(iv,media_sequence,decode_hex(iv)[0])
    aes = Cipher(algorithms.AES(key.key_value), modes.CBC(decode_hex(iv)[0]), backend=backend)
    #aes = Cipher(algorithms.AES(key.key_value), modes.CBC(iv.decode('hex')), backend=backend)
    #aes = AES.new(key.key_value, AES.MODE_CBC, iv.decode('hex'))
    decryptor = aes.decryptor()
    while True:
        data = input.read(blocksize)
        if not data:
            break
        output.write(decryptor.update(data))
        #output.write(aes.decrypt(data))
    decryptor.finalize()

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

def download(video, output, Url, seg_n, connection_n):
    global start_t
    if not 'start_t' in globals():
        start_t = time.process_time()
    raw = resumable_fetch(Url, seg_n, len(video.segments))
    progress_.append(seg_n)
    percentage = ((len(progress_)) * 100)/len(video.segments)
    avail_dots = 30
    if total_size_t_.is_alive():
        total_size_s_ = 'C.Size'
    else:
        total_size_s_ = size_adj(total_size, 'harddisk')
    shaded_dots = int(math.floor(float(len(progress_) + 1) / len(video.segments) * avail_dots))
    global max_output_len
    if not 'max_output_len' in globals():
        max_output_len = 0
    for i in range(0,connection_n):
        try:
            os.path.getsize(os.path.join(os.getcwd(), output.name[:-1]+str(i)))
        except:
            pass
    global download_size_
    if not 'download_size_' in globals():
        download_size_ = [0]*len(video.segments)
    #if not 'progress_bar_print' in globals():
    #    progress_bar_print = ['']*(connection_n+1)
    #elif len(progress_bar_print) != connection_n+1:
    #    progress_bar_print = ['']*(connection_n+1)
    download_size_1 = 0
    for i in download_size_:
        download_size_1 += i

    #c_width= get_terminal_size()[0]
    #c_width_croped = c_width - len('[]%100')-1
    #second_bar_  = '[' + '*' * (i * c_width_croped / counting_) + ' ' * (c_width_croped - (i * c_width_croped / counting_)) + ']%' + str(i * 100 / counting_) + ' ' * (3 - len(str(i * 100 / counting_)))
    #output_p = "\r" + '[' + '.'*shaded_dots + ' '*(avail_dots-shaded_dots) + '] %'+str(percentage)+' (%d/%d) %s/%s @ %s' % (len(progress_), len(video.segments),size_adj(download_size_1, 'harddisk'), total_size_s_, str(size_adj(download_size_1/(time.clock()-start_t), 'internet')))
    #max_output_len = max(max_output_len, len(output_p))
    #sys.stdout.write(output_p + ' '*(max_output_len-len(output_p)))
    
    #sys.stdout.flush()
    if hasattr(video, 'key'):
        copy_with_decrypt(raw, output, video.key, video.media_sequence + seg_n-1)
    else:
        copy_with_decrypt(raw, output, video.keys[0], video.media_sequence + seg_n-1)
    size = output.tell()
    if size % 188 != 0:
        size = size // 188 * 188
        output.seek(size)
        output.truncate(size)
	
def down_thread(video, output, start, end, seg_url, connection_n):
    #this function is for debug
    for i in range(start, end+1):
        download(video, output, seg_url[i-1], i, connection_n)

def fetch_streams(output_dir, video, connection_n):
    global total_size
    global total_size_t_
    global threads
    global stop_threads 

    stop_threads = False
    total_size_t_ = threading.Thread(target=compute_total_size,args=[video])
    total_size_t_.start()
    if len(video.segments)/connection_n <2:
        connection_n = len(video.segments)/2
    connection_dist = []
    seg_arr_list_=[]
    seg_arr_list_2_=[]
    for i in range(1, len(video.segments)+1):
        seg_arr_list_.append(i)
        seg_arr_list_2_.append(i)
    seg_arr_list_.reverse()
    seg_arr_list_2_.reverse()
    for l in range(0, len(video.segments)):
        for i in range(0,connection_n):
            if not 'seg_arr_list_len_{0}'.format(i) in locals():
                locals()['seg_arr_list_len_{0}'.format(i)]=[]
            try:
                locals()['seg_arr_list_len_{0}'.format(i)].append(seg_arr_list_.pop())
            except:
                pass
    for i in range(0, connection_n):
        for l in range(0, len(locals()['seg_arr_list_len_{0}'.format(i)])):
            if not 'thread_dis_{0}'.format(i) in locals():
                locals()['thread_dis_{0}'.format(i)]=[]
            try:
                locals()['thread_dis_{0}'.format(i)].append(seg_arr_list_2_.pop())
            except:
                pass
    connection_dist = []
    for i in range(0, connection_n):
        connection_dist.append(min(locals()['thread_dis_{0}'.format(i)]))
        connection_dist.append(max(locals()['thread_dis_{0}'.format(i)]))
            
    seg_url = []
    for n, seg in enumerate(video.segments):
        seg_url.append(seg.uri)
    connection_dist.reverse()
    threads = []
    global progress_
    progress_ = []
    for i in range (1, connection_n+1):
        locals()['file_seg_{0}'.format(i)] =  open(output_dir+str(i), 'wb')
        threads.append(threading.Thread(target=down_thread,args=(video, locals()['file_seg_{0}'.format(i)], connection_dist.pop(), connection_dist.pop(), seg_url, connection_n)))

    # Start all threads
    #print(threads)
    for x in threads:
        x.start()
    #print(threads, total_size_t_)
    # Wait for all of them to finish
    for x in threads:
        x.join()
    #print(threads, total_size_t_)
    stop_threads = True
    total_size_t_.join()
    #print(threads, total_size_t_)
    #print(locals())
    for i in range (1, connection_n+1):
        locals()['file_seg_{0}'.format(i)].close()

    print('\n'*(len(threads)+1))
    if connection_n==1:
        locals()['file_seg_1'].close()
        os.rename(output_dir+'1',output_dir)
    else:
        '''
        #final_file_ = open(output_dir, 'wb')
        cmd_appd = ['copy /b ','cat ']
        for i in range (1, connection_n+1):
            cmd_appd[0] += '"'+output_dir+str(i)+'"+'
            cmd_appd[1] += '"'+output_dir+str(i)+'" '
            #temp_file_ = open(output_dir+str(i), 'rb')
            #final_file_.write(temp_file_.read())
            #temp_file_.close()
            locals()['file_seg_{0}'.format(i)].close()
        #final_file_.close()
        cmd_appd[0] = cmd_appd[0][:-1]
        cmd_appd[0] += ' "'+output_dir+'"'
        cmd_appd[1] += '> "'+output_dir+'"'
        #print(cmd_appd)
        try:
            subprocess.call(cmd_appd[0], shell=True)
        except:
            subprocess.call(cmd_appd[1], shell=True)
        '''
        ofile_list_ = []
        for i in range (1, connection_n+1):
            ofile_list_ += [output_dir+str(i)]


        with open(output_dir, 'ab') as outfile:
            for fname in ofile_list_:
                with open(fname, 'rb') as infile:
                    #byte = infile.read(16384)
                    while True:
                        byte = infile.read(16384)
                        if not byte:
                            break
                        outfile.write(byte)
                os.remove(fname)

        
    print('\n')



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
    connection_n = connection_n
    fetch_encryption_key(video)
    fetch_streams(output, video, connection_n)

if __name__ == '__main__':
    connection_n = 1
    try:
        uri = sys.argv[1]
        #uri = 'https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/master.m3u8?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMjk5My5tcDQsMjEzMjk3Ny5tcDQsMTAzODk0My5tcDQsLnVybHNldC9tYXN0ZXIubTN1OCIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU1MjU1MzU4MH19fV19&Signature=p014sYK-yGJu0HldhEjlOBQs9afsK-~~UpWGw5PdYWi77dn2FJNs6DyFQPr-O-NA0R2NYlgxMJVWzbm15KZh1UgNRBG9H01chdRx2v~ay~FOjreg5DU~jtLaYxSP-yVEBtgQv5pFPaeaRMQwB~vZ0CrxZ1sIEzxaZLgHz6gDzA~t8L006FNA1FRGD-zw~FofpSVOFiUR10-6BMSh~dZIMaxOWkztR6zrub~ihTmOfjmt~m0X7eshocylT5EdBF4c1UBha-JIM2t-rm11And-ehhl0eXHZDdn4Hz90YGo6pOUOPLbNzVn7xXmvYAkvwk9xfDjoN2s8J~NcDppk7VXmg__&Key-Pair-Id=DLVR'
    except:
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
