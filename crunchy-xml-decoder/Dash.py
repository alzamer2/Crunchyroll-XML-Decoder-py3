#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urlunparse, urljoin
import re
import tempfile
import os
import threading
import math
import time

#from altfuncs import FileAdapter, LocalFileAdapter
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import requests
from pager import _windows_get_window_size as get_terminal_size

init()

blocksize = 16384

class dash_download:

    def __init__(self):
        self.dash_file = None
        self.dash_soup = None
        self.url_ = None
        self.connection_n = 1
        self.output_v = os.path.abspath('download.mp4')
        self.output_a = os.path.abspath('download.m4a')
        self.dash_duct = dict(dashvideo={}, dashaudio={}, dashsubtitle={})
        self.dash_stream_id = [None,None]
        self.dash_v_stream_urls = list()
        self.dash_a_stream_urls = list()
        self.active_urls_list = list()
        self.urls_list_r = list()
        self.dash_v_list_size = list()
        self.dash_a_list_size = list()
        self.dash_v_list_size_c = list()
        self.dash_a_list_size_c = list()
        self.tasks1 = []
        self.progress_bar_print = ['']
        self.start_t = time.process_time()


    def get_dash_file(self, url=None):
        session = requests.session()
        resp_ = session.get(url)
        self.dash_file = resp_.content
        self.dash_duct['url'] = url
        self.dash_duct['manifest_url'] = resp_.url



    def attrs_convert(self, attr_={}):
        for key_ in attr_:
            int_list = ['maxwidth', 'maxheight', 'width', 'height', 'startwithsap', 'startwithsap', 'audiosamplingrate']
            float_list = ['maxframerate', 'framerate']
            float_1000 = ['bandwidth']
            bool_list = ['segmentalignment']
            if key_ in int_list:
                attr_[key_] = int(attr_[key_])
            if key_ in bool_list:
                attr_[key_] = bool(attr_[key_])
            if key_ in float_list:
                flo = attr_[key_].split('/')
                if len(flo) == 1:
                    flo += [1]
                attr_[key_] = int(flo[0]) / int(flo[1])
            if key_ in float_1000:
                attr_[key_] = int(attr_[key_]) / 1000
        return attr_

    def parse_dash(self):
        self.get_dash_file(self.url_)
        url_parse = urlparse(self.dash_duct['manifest_url'])
        self.dash_duct['id'] = url_parse.query.split('/')[-1:][0]
        self.dash_duct['fragment_base_url'] = urlunparse(url_parse._replace(query='/'.join(url_parse.query.split('/')[:-1])+'/'))
        self.dash_soup = BeautifulSoup(self.dash_file, 'html.parser')
        for item in self.dash_soup.mpd.period.find_all('adaptationset'):
            if item.representation['mimetype'].split('/')[0] == 'video':
                self.dash_duct['dashvideo'][item['id']] = self.attrs_convert(dict(item.attrs))
                for streams in item.find_all('representation'):
                    self.dash_duct['dashvideo'][item['id']][streams['id']] = self.attrs_convert(dict(streams.attrs))
                    self.dash_duct['dashvideo'][item['id']]['segmenttemplate'] = self.attrs_convert(dict(item.segmenttemplate.attrs))
                    self.dash_duct['dashvideo'][item['id']]['segmenttemplate']['segmenttimeline'] = []
                for segment_ in item.segmenttemplate.segmenttimeline.find_all('s'):
                    repeat_ = 1
                    if segment_.has_attr('r'):
                        repeat_ += int(segment_['r'])
                    for i in range(0, repeat_):
                        self.dash_duct['dashvideo'][item['id']]['segmenttemplate']['segmenttimeline'] += [
                            int(segment_['d']) / 1000]
            if item.representation['mimetype'].split('/')[0] == 'audio':
                self.dash_duct['dashaudio'][item['id']] = self.attrs_convert(dict(item.attrs))
                for streams in item.find_all('representation'):
                    self.dash_duct['dashaudio'][item['id']][streams['id']] = self.attrs_convert(dict(streams.attrs))
                    self.dash_duct['dashaudio'][item['id']]['segmenttemplate'] = self.attrs_convert(dict(item.segmenttemplate.attrs))
                    self.dash_duct['dashaudio'][item['id']]['segmenttemplate']['segmenttimeline'] = []
                for segment_ in item.segmenttemplate.segmenttimeline.find_all('s'):
                    repeat_ = 1
                    if segment_.has_attr('r'):
                        repeat_ += int(segment_['r'])
                    for i in range(0, repeat_):
                        self.dash_duct['dashaudio'][item['id']]['segmenttemplate']['segmenttimeline'] += [
                            int(segment_['d']) / 1000]
            if item.representation['mimetype'].split('/')[0] == 'subtitle':
                self.dash_duct['dashsubtitle'][item['id']] = self.attrs_convert(dict(item.attrs))
                for streams in item.find_all('representation'):
                    self.dash_duct['dashsubtitle'][item['id']][streams['id']] = self.attrs_convert(dict(streams.attrs))
                    self.dash_duct['dashsubtitle'][item['id']]['segmenttemplate'] = self.attrs_convert(
                    dict(item.segmenttemplate.attrs))
                    self.dash_duct['dashsubtitle'][item['id']]['segmenttemplate']['segmenttimeline'] = []
                for segment_ in item.segmenttemplate.segmenttimeline.find_all('s'):
                    repeat_ = 1
                    if segment_.has_attr('r'):
                        repeat_ += int(segment_['r'])
                    for i in range(0, repeat_):
                        self.dash_duct['dashsubtitle'][item['id']]['segmenttemplate']['segmenttimeline'] += [
                            int(segment_['d']) / 1000]

    def find_best_stream(self, kwargs):
        ## suported key: resolution, r, size, s, width, height, w, h, bandwidth, audio_quality,v_bandwidth,a_bandwidth
        suported_key = {'resolution' : 'r=', 'r' : 'r=', 'size' : 'r=', 's' : 'r=',
                        'width' : 'w=', 'w' : 'w=', 'height' : 'h=', 'h' : 'h=',
                        'bandwidth' : 'vbr=', 'v_bandwidth' : 'vbr=', 'vbr' : 'vbr=',
                        'audio_quality' : 'abr=', 'a_bandwidth' : 'abr=', 'abr':'abr=',
                        'audiosampling' : 'hz=', 'hz' : 'hz=', 'as' : 'hz='}
        ## suported value: MAX, best, high, highest, low, lowest, worst, 0
        suported_value = {'MAX' : 'MAX','best': 'MAX','high': 'MAX','highest': 'MAX',
                          'low' : 0, 'lowest' : 0, 'worst' : 0}
        ''' Create dict'''
        width_list = dict()
        height_list = dict()
        v_bandwidth = dict()
        a_bandwidth = dict()
        a_sampling = dict()
        for v_id in self.dash_duct['dashvideo']:
            for v_stream in self.dash_duct['dashvideo'][v_id]:
                if type(self.dash_duct['dashvideo'][v_id][v_stream]) == dict:
                    if 'mimetype' in self.dash_duct['dashvideo'][v_id][v_stream]:
                        width_list.update({self.dash_duct['dashvideo'][v_id][v_stream]['width'] :
                                           self.dash_duct['dashvideo'][v_id][v_stream]['id']})
                        height_list.update({self.dash_duct['dashvideo'][v_id][v_stream]['height'] :
                                           self.dash_duct['dashvideo'][v_id][v_stream]['id']})
                        v_bandwidth.update({self.dash_duct['dashvideo'][v_id][v_stream]['bandwidth'] :
                                           self.dash_duct['dashvideo'][v_id][v_stream]['id']})
        for a_id in self.dash_duct['dashaudio']:
            for a_stream in self.dash_duct['dashaudio'][a_id]:
                if type(self.dash_duct['dashaudio'][a_id][a_stream]) == dict:
                    if 'mimetype' in self.dash_duct['dashaudio'][a_id][a_stream]:
                        a_bandwidth.update({self.dash_duct['dashaudio'][a_id][a_stream]['bandwidth'] :
                                           self.dash_duct['dashaudio'][a_id][a_stream]['id']})
                        a_sampling.update({self.dash_duct['dashaudio'][a_id][a_stream]['audiosamplingrate'] :
                                           self.dash_duct['dashaudio'][a_id][a_stream]['id']})
        v_bandwidth_r = {k:v for v,k in v_bandwidth.items()}
        a_bandwidth_r = {k:v for v,k in a_bandwidth.items()}
        '''function to get closer stream'''
        def st_width(h_):
            selected_width = 0
            for i in sorted(list(width_list)):
                if i >= h_:
                    selected_width = i
                    break
            if selected_width == 0:
                selected_width = sorted(list(width_list))[-1:][0]
            if self.dash_stream_id[0] is None:
                self.dash_stream_id[0] = width_list[selected_width]
            else:
                if v_bandwidth_r[width_list[selected_width]] > v_bandwidth_r[self.dash_stream_id[0]]:
                    self.dash_stream_id[0] = width_list[selected_width]

        def st_height(h_):
            selected_height = 0
            for i in sorted(list(height_list)):
                if i >= h_:
                    selected_height = i
                    break
            if selected_height == 0:
                selected_height = sorted(list(height_list))[-1:][0]
            if self.dash_stream_id[0] is None:
                self.dash_stream_id[0] = height_list[selected_height]
            else:
                if v_bandwidth_r[height_list[selected_height]] > v_bandwidth_r[self.dash_stream_id[0]]:
                    self.dash_stream_id[0] = height_list[selected_height]

        def v_st_bandwidth(h_):
            selected_bandwidth = 0
            for i in sorted(list(v_bandwidth)):
                if i >= h_:
                    selected_bandwidth = i
                    break
            if selected_bandwidth == 0:
                selected_bandwidth = sorted(list(v_bandwidth))[-1:][0]
            if self.dash_stream_id[0] is None:
                self.dash_stream_id[0] = v_bandwidth[selected_bandwidth]
            else:
                if v_bandwidth_r[v_bandwidth[selected_bandwidth]] > v_bandwidth_r[self.dash_stream_id[0]]:
                    self.dash_stream_id[0] = v_bandwidth[selected_bandwidth]

        def a_st_bandwidth(h_):
            selected_bandwidth = 0
            for i in sorted(list(a_bandwidth)):
                if i >= h_:
                    selected_bandwidth = i
                    break
            if selected_bandwidth == 0:
                selected_bandwidth = sorted(list(a_bandwidth))[-1:][0]
            if self.dash_stream_id[1] is None:
                self.dash_stream_id[1] = a_bandwidth[selected_bandwidth]
            else:
                if a_bandwidth_r[a_bandwidth[selected_bandwidth]] > a_bandwidth_r[self.dash_stream_id[1]]:
                    self.dash_stream_id[1] = a_bandwidth[selected_bandwidth]

        def a_st_audiosampling(h_):
            selected_sampling = 0
            for i in sorted(list(a_sampling)):
                if i >= h_:
                    selected_sampling = i
                    break
            if selected_sampling == 0:
                selected_sampling = sorted(list(a_sampling))[-1:][0]
            if self.dash_stream_id[1] is None:
                self.dash_stream_id[1] = a_sampling[selected_sampling]
            else:
                if a_bandwidth_r[a_bandwidth[selected_sampling]] > a_bandwidth_r[self.dash_stream_id[1]]:
                    self.dash_stream_id[1] = a_sampling[selected_sampling]

        def v_st_best():
            self.dash_stream_id[0] = v_bandwidth[sorted(list(v_bandwidth))[-1:][0]]

        def v_st_worst():
            self.dash_stream_id[0] = v_bandwidth[sorted(list(v_bandwidth))[:1][0]]

        def a_st_best():
            self.dash_stream_id[1] = a_bandwidth[sorted(list(a_bandwidth))[-1:][0]]

        def a_st_worst():
            self.dash_stream_id[1] = a_bandwidth[sorted(list(a_bandwidth))[:1][0]]


        '''Parse kwargs'''
        v_quality = []

        for key_ in kwargs: #this 'for' will parse kwarge and make them has set form
            for suported_value_item in suported_value:
                if str(kwargs[key_]).lower() == suported_value_item.lower():
                    kwargs[key_] = suported_value[suported_value_item]
            for suported_key_item in suported_key:
                if key_.lower() == suported_key_item.lower():
                    v_quality += [suported_key[suported_key_item]+str(kwargs[key_])]

        for item in v_quality: #this 'for' will the closest video stream for kwargs input
            if re.match('(?:r\=\d*[Xx]|r\=)(.*)',item): #test to find r=
                if re.fullmatch('(?:r\=\d*[Xx]|r\=)(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('(?:r\=\d*[Xx]|r\=)(\d*)p{,1}',item): #test to find int
                    st_height(int(re.findall('(?:r\=\d*[Xx]|r\=)(\d*)',item)[0]))
            if re.match('h=(.*)',item): #test to find h=
                if re.fullmatch('h=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('h=(\d*)p{,1}',item): #test to find height
                    st_height(int(re.findall('h=(\d*)',item)[0]))
            if re.match('w=(.*)',item): #test to find w=
                if re.fullmatch('w=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('w=(\d*)p{,1}',item): #test to find width
                    st_width(int(re.findall('w=(\d*)',item)[0]))
            if re.match('vbr=(.*)',item): #test to find vbr=
                if re.fullmatch('vbr=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('vbr=(\d*)',item): #test to find bandwidth
                    v_st_bandwidth(int(re.findall('vbr=(\d*)',item)[0]))
            if re.match('abr=(.*)',item): #test to find abr=
                if re.fullmatch('abr=(MAX)',item): #test to find 'max'
                    a_st_best()
                if re.fullmatch('abr=(\d*)',item): #test to find bandwidth
                    a_st_bandwidth(int(re.findall('abr=(\d*)',item)[0]))
            if re.match('hz=(.*)',item): #test to find hz=
                if re.fullmatch('hz=(MAX)',item): #test to find 'max'
                    a_st_best()
                if re.fullmatch('hz=(\d*)',item): #test to find audiosampling
                    a_st_audiosampling(int(re.findall('hz=(\d*)',item)[0]))

        if self.dash_stream_id[0] is None:
            v_st_best()
        if self.dash_stream_id[1] is None:
            a_st_best()

    def buildup_st_urls(self):
        for v_id in self.dash_duct['dashvideo']:
            if self.dash_stream_id[0] in self.dash_duct['dashvideo'][v_id]:
                startnumber = int(self.dash_duct['dashvideo'][v_id]['segmenttemplate']['startnumber'])
                media_url = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['media'].replace('$RepresentationID$',self.dash_stream_id[0])
                init_url = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['initialization'].replace('$RepresentationID$',self.dash_stream_id[0])
                segments_ = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['segmenttimeline']
                segment_time_line = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['segmenttimeline']
                bandwidth = int(self.dash_duct['dashvideo'][v_id][self.dash_stream_id[0]]['bandwidth'])
                self.dash_v_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], init_url)]
                for i in range(startnumber, len(segments_)+1):
                    self.dash_v_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], media_url.replace('$Number$',str(i)))]
                self.dash_v_list_size = [0]+[i*bandwidth/8*1000 for i in segment_time_line]
                self.dash_v_list_size_c = [0]*len(self.dash_v_list_size)
        for a_id in self.dash_duct['dashaudio']:
            if self.dash_stream_id[1] in self.dash_duct['dashaudio'][a_id]:
                startnumber = int(self.dash_duct['dashaudio'][a_id]['segmenttemplate']['startnumber'])
                media_url = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['media'].replace('$RepresentationID$',self.dash_stream_id[1])
                init_url = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['initialization'].replace('$RepresentationID$',self.dash_stream_id[1])
                segments_ = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['segmenttimeline']
                segment_time_line = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['segmenttimeline']
                bandwidth = int(self.dash_duct['dashaudio'][a_id][self.dash_stream_id[1]]['bandwidth'])
                self.dash_a_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], init_url)]
                for i in range(startnumber, len(segments_)+1):
                    self.dash_a_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], media_url.replace('$Number$',str(i)))]
                self.dash_a_list_size = [0]+[i*bandwidth/8*1000 for i in segment_time_line]
                self.dash_a_list_size_c = [0]*len(self.dash_a_list_size)

    def print_progress(self):
        total_start_time = time.process_time()
        while True:
            still_downloading = False
            for indx_,task_ in enumerate(self.tasks1):
                still_downloading = still_downloading or task_.is_alive()
            total_download_size = sum(self.dash_v_list_size+self.dash_a_list_size)
            download_size = sum(self.dash_v_list_size_c+self.dash_a_list_size_c)
            if total_start_time != time.process_time():
                total_speed = str(size_adj(download_size/(time.process_time()-total_start_time), 'internet'))
            else:
                total_speed = str(size_adj(0, 'internet'))
            print(progress_bar_(download_size,
                                total_download_size,
                                size_adj(download_size,'harddisk')+'/'+size_adj(total_download_size,'harddisk'),
                                text_end='%'+str(int(100*download_size/total_download_size))+'@'+total_speed))
            for print_line in self.progress_bar_print:
                print(print_line)
            print('\033[A'*(len(self.progress_bar_print)+2))
            if not still_downloading:
                print('\n'*(len(self.progress_bar_print)+2))
                break
            time.sleep(0.1)

    def download_link(self,url,output):
        with self.session.get(url, stream=True) as response:
            response.raise_for_status()
            filename = output
            if url in self.dash_v_stream_urls:
                self.dash_v_list_size[self.dash_v_stream_urls.index(url)] = int(response.headers['Content-Length'])
            if url in self.dash_a_stream_urls:
                self.dash_a_list_size[self.dash_a_stream_urls.index(url)] = int(response.headers['Content-Length'])
            with open(filename, 'ab') as f_handle:
                for chunk in response.iter_content(chunk_size=blocksize):
                    if url in self.dash_v_stream_urls:
                        self.dash_v_list_size_c[self.dash_v_stream_urls.index(url)] += len(chunk)
                    if url in self.dash_a_stream_urls:
                        self.dash_a_list_size_c[self.dash_a_stream_urls.index(url)] += len(chunk)
                    if chunk:
                        f_handle.write(chunk)

    def download_thread(self,out_dir):
        while len(self.urls_list_r) >0:
            url = self.urls_list_r.pop()
            filename = os.path.join(out_dir,os.path.split(urlparse(url).path)[1])
            with self.session.get(url, stream=True) as response:
                response.raise_for_status()
                if url in self.dash_v_stream_urls:
                    self.dash_v_list_size[self.dash_v_stream_urls.index(url)] = int(response.headers['Content-Length'])
                if url in self.dash_a_stream_urls:
                    self.dash_a_list_size[self.dash_a_stream_urls.index(url)] = int(response.headers['Content-Length'])
                with open(filename, 'ab') as f_handle:
                    chunk_size = 0
                    part_start_time = time.process_time()
                    for chunk in response.iter_content(chunk_size=blocksize):
                        chunk_size += len(chunk)
                        if part_start_time != time.process_time():
                            part_speed = str(size_adj(chunk_size/(time.process_time()-part_start_time), 'internet'))
                        else:
                            part_speed = str(size_adj(0, 'internet'))
                        if url in self.dash_v_stream_urls:
                            self.dash_v_list_size_c[self.dash_v_stream_urls.index(url)] = chunk_size
                        if url in self.dash_a_stream_urls:
                            self.dash_a_list_size_c[self.dash_a_stream_urls.index(url)] = chunk_size
                        index_thread_ = int(threading.current_thread().name.replace('download_thread_',''))
                        self.progress_bar_print[index_thread_] = progress_bar_(chunk_size,
                                                                               int(response.headers['Content-Length']),
                                                                               'Part #'+str(self.active_urls_list.index(url)),
                                                                               '%'+str(int(chunk_size/int(response.headers['Content-Length'])*100))+'@'+ part_speed)
                        if chunk:
                            f_handle.write(chunk)

    def download_streams(self, video=True, audio=True):
        if video:
            self.active_urls_list += self.dash_v_stream_urls
        if audio:
            self.active_urls_list += self.dash_a_stream_urls
        # self.active_urls_list = self.dash_v_stream_urls+self.dash_a_stream_urls
        num_parts=len(self.active_urls_list)
        if num_parts/self.connection_n < 2:
            self.connection_n = len(range(0,num_parts,math.ceil(num_parts/self.connection_n)))
        self.progress_bar_print = ['']*(self.connection_n+1)
        self.urls_list_r = list(self.active_urls_list)[::-1]
        #self.urls_list_r.reverse()


        with tempfile.TemporaryDirectory(dir=os.path.split(self.output_v)[0]) as tempD_:
            with requests.session() as self.session:
                # self.session.mount('file://', FileAdapter())
                print_task = threading.Thread(target=self.print_progress,name='print_thread_')
                for n, i in enumerate(range(0,self.connection_n)):
                    task = threading.Thread(target=self.download_thread,name='download_thread_'+str(n), args=([tempD_]))
                    self.tasks1.append(task)

                for x in self.tasks1:
                    x.start()

                print_task.start()
                for x in self.tasks1:
                    x.join()
                print_task.join()

            if video:
                vfiles = [os.path.split(urlparse(url_).path)[1] for url_ in self.dash_v_stream_urls]
                with open(self.output_v, 'wb') as outfile:
                    for fname in vfiles:
                        with open(os.path.join(tempD_, fname), 'rb') as infile:
                            while True:
                                byte = infile.read(blocksize)
                                if not byte:
                                    break
                                outfile.write(byte)
            if audio:
                afiles = [os.path.split(urlparse(url_).path)[1] for url_ in self.dash_a_stream_urls]
                with open(self.output_a, 'wb') as outfile:
                    for fname in afiles:
                        with open(os.path.join(tempD_, fname), 'rb') as infile:
                            while True:
                                byte = infile.read(blocksize)
                                if not byte:
                                    break
                                outfile.write(byte)

    def download(self, url=None, output=None, connection_n=1, video=True, audio=True, **kwargs):
        print()
        if url is None:
            url = input('dashlink>>')
        self.url_ = url
        if output is not None:
            self.output_v = os.path.abspath(output)
            self.output_a = os.path.abspath(os.path.splitext(output)[0]+'.m4a')
        self.connection_n = connection_n
        self.parse_dash()
        self.find_best_stream(kwargs)
        if not video:
            self.dash_stream_id[0] = ''
        if not audio:
            self.dash_stream_id[1] = ''
        self.buildup_st_urls()
        self.download_streams(video=video, audio=audio)

##########################################################################################:---
##########################################################################################:---      Functions
##########################################################################################:---

def progress_bar_(currect,target,text_center='',text_end='%100',text_end_lenght=0,center_bgc='30;42',defult_bgc=''):
    try:
        c_width = get_terminal_size()[0]
        if c_width == 0:
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


##########################################################################################:---      
##########################################################################################:---      Main
##########################################################################################:---
if __name__ == '__main__':
    testing = dash_download()
    testing.download('''https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/manifest.mpd?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMzAwOS5tcDQsMjEzMzAyNS5tcDQsMjEzMjk5My5tcDQsMjEzMjk3Ny5tcDQsMTAzODk0My5tcDQsLnVybHNldC9tYW5pZmVzdC5tcGQiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NzM5MjYxMjd9fX1dfQ__&Signature=lq2tgVfP6i9avXma4O~CEIRWF6hFtrUp~ZXeCMTiBzh8FLamOZUqRh~8sB8rHaL4YgDEa-0d4x2wVvxFR3G66d74muR5YPYogDR2vMAb8SmDjSrRacitfBZwohc9L3nbowEZvQ-G3q0C4nvgZrLqAYBhWcCTYvMGXJf22bGupSrCus8y0UskCFQ5ehnK0ke-p8wM-5coEoHxtFY96kU1PfvF5hO0RMVqMpHqTrnk47KjuRA87CKmaZnQ6TXRUo~CTy4a6svaL7cRWCUyIR2xQBt5vETAQ8VZOxRZOtJ4vdkCP5C~1vV1vb5781WgfzBVoSHvcZwFaXFt-JrEIb4N~A__&Key-Pair-Id=DLVR''',
                     #resolution = '1280x720', w= 0, s='low',size='MAX',r='best'
                     #abr=60, hz=44100
                     connection_n=8,vbr='best',abr='best'
                     )
    input()
