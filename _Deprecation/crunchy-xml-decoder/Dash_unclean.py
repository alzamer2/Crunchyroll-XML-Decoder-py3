#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from urllib.parse import urlparse, urlunparse, urljoin
from urllib.request import url2pathname
import re
from collections import OrderedDict as odict
import tempfile
import os
import threading
import math
import time
from concurrent.futures import ThreadPoolExecutor,as_completed


from altfuncs import FileAdapter, LocalFileAdapter
from bs4 import BeautifulSoup
import requests
import wget
from colorama import Fore, Style, init
import requests
from pager import _windows_get_window_size as get_terminal_size

init()

blocksize = 16384
#blocksize = 100

class dash_download:

    def __init__(self):
        self.dash_file = None
        self.dash_soup = None
        self.url_ = None
        self.connection_n = 1
        self.output_v = os.path.abspath('download.mp4')
        self.output_a = os.path.abspath('download.m4a')
        self.dash_duct = dict(dashvideo={}, dashaudio={}, dashsubtitle={})
        #self.video_br = 'MAX'
        #self.audio_br = 'MAX'
        self.dash_stream_id = [None,None]
        self.dash_v_stream_urls = list()
        self.dash_a_stream_urls = list()
        self.dash_v_list_size = list()
        self.dash_a_list_size = list()
        self.dash_v_list_size_c = list()
        self.dash_a_list_size_c = list()
        self.tasks1 = []
        self.progress_bar_print = ['']
        self.start_t = time.process_time()
        

    def get_dash_file(self, url=None):
        # self.dash_file = gethtml(url,headers=None)
        # self.dash_file = '''<?xml version="1.0"?>\n<MPD\n    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n    xmlns="urn:mpeg:dash:schema:mpd:2011"\n    xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd"\n    type="static"\n    mediaPresentationDuration="PT210.098S"\n    minBufferTime="PT10S"\n    profiles="urn:mpeg:dash:profile:full:2011">\n  <Period>\n    <AdaptationSet\n        id="1"\n        segmentAlignment="true"\n        maxWidth="1920"\n        maxHeight="1080"\n        maxFrameRate="45000/1877">\n        <SegmentTemplate\n            timescale="1000"\n            media="fragment-$Number$-$RepresentationID$.m4s?t=st=1573209533~exp=1573295933~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=aa3b311b652b472208be99fd592c29fb9dca2aedbe8fb29a1b0cad03295882bc"\n            initialization="init-$RepresentationID$.mp4?t=st=1573209533~exp=1573295933~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=aa3b311b652b472208be99fd592c29fb9dca2aedbe8fb29a1b0cad03295882bc"\n            startNumber="1">\n            <SegmentTimeline>\n                <S d="4004"/>\n                <S d="4004"/>\n                <S d="5422"/>\n                <S d="9510"/>\n                <S d="11094"/>\n                <S d="10010"/>\n                <S d="9218"/>\n                <S d="10010"/>\n                <S d="9843"/>\n                <S d="10010"/>\n                <S d="9927"/>\n                <S d="10010"/>\n                <S d="11220"/>\n                <S d="10010" r="1"/>\n                <S d="9259"/>\n                <S d="10010"/>\n                <S d="10719"/>\n                <S d="8509"/>\n                <S d="11011"/>\n                <S d="9551"/>\n                <S d="10093"/>\n                <S d="6548"/>\n            </SegmentTimeline>\n        </SegmentTemplate>\n      <Representation\n          id="f1-v1-x3"\n          mimeType="video/mp4"\n          codecs="avc1.640028"\n          width="1280"\n          height="720"\n          frameRate="45000/1877"\n          sar="1:1"\n          startWithSAP="1"\n          bandwidth="2824695">\n      </Representation>\n      <Representation\n          id="f2-v1-x3"\n          mimeType="video/mp4"\n          codecs="avc1.640028"\n          width="1920"\n          height="1080"\n          frameRate="45000/1877"\n          sar="1:1"\n          startWithSAP="1"\n          bandwidth="6020488">\n      </Representation>\n      <Representation\n          id="f3-v1-x3"\n          mimeType="video/mp4"\n          codecs="avc1.4d401f"\n          width="848"\n          height="480"\n          frameRate="45000/1877"\n          sar="1:1"\n          startWithSAP="1"\n          bandwidth="1310518">\n      </Representation>\n      <Representation\n          id="f4-v1-x3"\n          mimeType="video/mp4"\n          codecs="avc1.4d401e"\n          width="640"\n          height="360"\n          frameRate="45000/1877"\n          sar="1:1"\n          startWithSAP="1"\n          bandwidth="568746">\n      </Representation>\n      <Representation\n          id="f5-v1-x3"\n          mimeType="video/mp4"\n          codecs="avc1.42c015"\n          width="428"\n          height="240"\n          frameRate="45000/1877"\n          sar="1:1"\n          startWithSAP="1"\n          bandwidth="423361">\n      </Representation>\n    </AdaptationSet>\n    <AdaptationSet\n        id="2"\n        segmentAlignment="true">\n      <AudioChannelConfiguration\n          schemeIdUri="urn:mpeg:dash:23003:3:audio_channel_configuration:2011"\n          value="1"/>\n        <SegmentTemplate\n            timescale="1000"\n            media="fragment-$Number$-$RepresentationID$.m4s?t=st=1573209533~exp=1573295933~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=aa3b311b652b472208be99fd592c29fb9dca2aedbe8fb29a1b0cad03295882bc"\n            initialization="init-$RepresentationID$.mp4?t=st=1573209533~exp=1573295933~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=aa3b311b652b472208be99fd592c29fb9dca2aedbe8fb29a1b0cad03295882bc"\n            startNumber="1">\n            <SegmentTimeline>\n                <S d="2508"/>\n                <S d="4992"/>\n                <S d="5016"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="10008" r="1"/>\n                <S d="9985"/>\n                <S d="7597"/>\n            </SegmentTimeline>\n        </SegmentTemplate>\n      <Representation\n          id="f1-a1-x3"\n          mimeType="audio/mp4"\n          codecs="mp4a.40.2"\n          audioSamplingRate="44100"\n          startWithSAP="1"\n          bandwidth="128011">\n      </Representation>\n      <Representation\n          id="f3-a1-x3"\n          mimeType="audio/mp4"\n          codecs="mp4a.40.2"\n          audioSamplingRate="44100"\n          startWithSAP="1"\n          bandwidth="96008">\n      </Representation>\n      <Representation\n          id="f5-a1-x3"\n          mimeType="audio/mp4"\n          codecs="mp4a.40.2"\n          audioSamplingRate="22050"\n          startWithSAP="1"\n          bandwidth="64012">\n      </Representation>\n    </AdaptationSet>\n  </Period>\n</MPD>\n'''
        session = requests.session()
        resp_ = session.get(url)
        self.dash_file = resp_.content
        #print(resp_.content)
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
        # self.dash_duct['url'] = self.url_
        self.get_dash_file(self.url_)
        url_parse = urlparse(self.dash_duct['manifest_url'])
        self.dash_duct['id'] = url_parse.query.split('/')[-1:][0]
        self.dash_duct['fragment_base_url'] = urlunparse(url_parse._replace(query='/'.join(url_parse.query.split('/')[:-1])+'/'))
        self.dash_soup = BeautifulSoup(self.dash_file, 'html.parser')
        for item in self.dash_soup.mpd.period.find_all('adaptationset'):
            if item.representation['mimetype'].split('/')[0] == 'video':
                self.dash_duct['dashvideo'][item['id']] = self.attrs_convert(dict(item.attrs))
                for streams in item.find_all('representation'):
                    # print(dash_duct)
                    self.dash_duct['dashvideo'][item['id']][streams['id']] = self.attrs_convert(dict(streams.attrs))
                    self.dash_duct['dashvideo'][item['id']]['segmenttemplate'] = self.attrs_convert(dict(item.segmenttemplate.attrs))
                    self.dash_duct['dashvideo'][item['id']]['segmenttemplate']['segmenttimeline'] = []
                for segment_ in item.segmenttemplate.segmenttimeline.find_all('s'):
                    # print(dash_duct)
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
        #print(kwargs)
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
            #print(a_bandwidth)
            for i in sorted(list(a_bandwidth)):
                if i >= h_:
                    selected_bandwidth = i
                    break
            #print(selected_bandwidth)
            if selected_bandwidth == 0:
                selected_bandwidth = sorted(list(a_bandwidth))[-1:][0]
            #print(a_bandwidth)
            #print(selected_bandwidth)
            #print(selected_bandwidth,a_bandwidth[selected_bandwidth])
            if self.dash_stream_id[1] is None:
                self.dash_stream_id[1] = a_bandwidth[selected_bandwidth]
            else:
                if a_bandwidth_r[a_bandwidth[selected_bandwidth]] > a_bandwidth_r[self.dash_stream_id[1]]:
                    self.dash_stream_id[1] = a_bandwidth[selected_bandwidth]

        def a_st_audiosampling(h_):
            selected_sampling = 0
            #print(a_bandwidth)
            for i in sorted(list(a_sampling)):
                if i >= h_:
                    selected_sampling = i
                    break
            #print(selected_bandwidth)
            if selected_sampling == 0:
                selected_sampling = sorted(list(a_sampling))[-1:][0]
            #print(a_bandwidth)
            #print(selected_bandwidth)
            #print(selected_bandwidth,a_bandwidth[selected_bandwidth])
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
        #a_quality = []
        for key_ in kwargs: #this 'for' will parse kwarge and make them has set form
            for suported_value_item in suported_value:
                if str(kwargs[key_]).lower() == suported_value_item.lower():
                    #print(str(kwargs[key_]).lower() , suported_value_item.lower(), suported_value[suported_value_item])
                    kwargs[key_] = suported_value[suported_value_item]
            for suported_key_item in suported_key:
                #print(key_.lower() , suported_key_item.lower())
                if key_.lower() == suported_key_item.lower():
                    #print(key_.lower() , suported_key_item.lower(), suported_key[suported_key_item])
                    v_quality += [suported_key[suported_key_item]+str(kwargs[key_])]
            
        #print(v_quality)

        for item in v_quality: #this 'for' will the closest video stream for kwargs input
            if re.match('(?:r\=\d*[Xx]|r\=)(.*)',item): #test to find r=
                if re.fullmatch('(?:r\=\d*[Xx]|r\=)(MAX)',item): #test to find 'max'
                    v_st_best()
                    #print(1,item, re.findall('(?:r\=\d*[Xx]|r\=)([^\d\s]*)',item)[0])
                if re.fullmatch('(?:r\=\d*[Xx]|r\=)(\d*)',item): #test to find int
                    #print(2,item, re.findall('(?:r\=\d*[Xx]|r\=)(\d*)',item)[0])
                    st_height(int(re.findall('(?:r\=\d*[Xx]|r\=)(\d*)',item)[0]))
            if re.match('h=(.*)',item): #test to find h=
                if re.fullmatch('h=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('h=(\d*)',item): #test to find height
                    st_height(int(re.findall('h=(\d*)',item)[0]))
            if re.match('w=(.*)',item): #test to find w=
                if re.fullmatch('w=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('w=(\d*)',item): #test to find width
                    st_width(int(re.findall('w=(\d*)',item)[0]))
            if re.match('vbr=(.*)',item): #test to find vbr=
                if re.fullmatch('vbr=(MAX)',item): #test to find 'max'
                    v_st_best()
                if re.fullmatch('vbr=(\d*)',item): #test to find bandwidth
                    #print('test')
                    v_st_bandwidth(int(re.findall('vbr=(\d*)',item)[0]))
            if re.match('abr=(.*)',item): #test to find abr=
                if re.fullmatch('abr=(MAX)',item): #test to find 'max'
                    a_st_best()
                if re.fullmatch('abr=(\d*)',item): #test to find bandwidth
                    #print('test')
                    a_st_bandwidth(int(re.findall('abr=(\d*)',item)[0]))
            if re.match('hz=(.*)',item): #test to find hz=
                if re.fullmatch('hz=(MAX)',item): #test to find 'max'
                    a_st_best()
                if re.fullmatch('hz=(\d*)',item): #test to find audiosampling
                    #print('test')
                    a_st_audiosampling(int(re.findall('hz=(\d*)',item)[0]))
                    

        if self.dash_stream_id[0] is None:
            v_st_best()
        if self.dash_stream_id[1] is None:
            a_st_best()
            
    
                

        
        #for key_ in kwargs:
            
        #    if key_ == 'resolution':
       #         if kwargs['resolution'] in suported_value:
       #             self.video_br = suported_value[kwargs['resolution']]
       #         elif re.match('\d+?(?:x|X)(\d+)',kwargs['resolution']):
       #             self.video_br = re.findall('\d+?(?:x|X)(\d+)',kwargs['resolution'])[0]
       #         else:
       #             self.video_br = 'MAX'
       #         #print(kwargs['resolution'])
       #         break
            
        
            
                        
        #print(kwargs,width_list,height_list,v_bandwidth,a_bandwidth)
        # self.dash_stream_id
        #if self.video_br == 'MAX':
        #    self.video_br = 0
        #    for v_id in self.dash_duct['dashvideo']:
        #        for v_stream in self.dash_duct['dashvideo'][v_id]:
        #            #print(self.dash_duct['dashvideo'][v_id]['maxheight'])
        #            # if 'video/mp4' in self.dash_duct['dashvideo'][v_id][v_stream]:
        #            if type(self.dash_duct['dashvideo'][v_id][v_stream]) == dict:
        #                if 'mimetype' in self.dash_duct['dashvideo'][v_id][v_stream]:
        #                    #print(self.dash_duct['dashvideo'][v_id][v_stream])
        #                    if self.dash_duct['dashvideo'][v_id][v_stream]['bandwidth'] > self.video_br:
        #                        self.video_br = self.dash_duct['dashvideo'][v_id][v_stream]['bandwidth']
        #                        self.dash_stream_id[0] = self.dash_duct['dashvideo'][v_id][v_stream]['id']
        #                        
        #if self.audio_br == 'MAX':
        #    self.audio_br = 0
        #    for v_id in self.dash_duct['dashaudio']:
        #        for v_stream in self.dash_duct['dashaudio'][v_id]:
        #            #print(self.dash_duct['dashvideo'][v_id]['maxheight'])
        #            # if 'video/mp4' in self.dash_duct['dashvideo'][v_id][v_stream]:
        #            if type(self.dash_duct['dashaudio'][v_id][v_stream]) == dict:
        #                if 'mimetype' in self.dash_duct['dashaudio'][v_id][v_stream]:
        #                    #print(self.dash_duct['dashvideo'][v_id][v_stream])
        #                    if self.dash_duct['dashaudio'][v_id][v_stream]['bandwidth'] > self.audio_br:
        #                        self.audio_br = self.dash_duct['dashaudio'][v_id][v_stream]['bandwidth']
        #                        self.dash_stream_id[1] = self.dash_duct['dashaudio'][v_id][v_stream]['id']


        pass

    def buildup_st_urls(self):
        for v_id in self.dash_duct['dashvideo']:
            if self.dash_stream_id[0] in self.dash_duct['dashvideo'][v_id]:
                #print(self.dash_duct['dashvideo'][v_id]['segmenttemplate'].keys())
                startnumber = int(self.dash_duct['dashvideo'][v_id]['segmenttemplate']['startnumber'])
                media_url = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['media'].replace('$RepresentationID$',self.dash_stream_id[0])
                init_url = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['initialization'].replace('$RepresentationID$',self.dash_stream_id[0])
                segments_ = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['segmenttimeline']
                segment_time_line = self.dash_duct['dashvideo'][v_id]['segmenttemplate']['segmenttimeline']
                bandwidth = int(self.dash_duct['dashvideo'][v_id][self.dash_stream_id[0]]['bandwidth'])
                #print(startnumber,media_url,init_url,segments_)
                self.dash_v_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], init_url)]
                for i in range(startnumber,len(segments_)+1):
                    self.dash_v_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], media_url.replace('$Number$',str(i)))]
                self.dash_v_list_size = [0]+[i*bandwidth/8*1000 for i in segment_time_line]
                self.dash_v_list_size_c = [0]*len(self.dash_v_list_size)
                #for i in self.dash_v_stream_urls[:3]:
                #    print(i)
            #if self.dash_duct['dashvideo'][v_id]
            #print(self.dash_duct['dashvideo'][v_id][self.dash_stream_id[0]])
            #for v_stream in self.dash_duct['dashvideo'][v_id]:
        for a_id in self.dash_duct['dashaudio']:
            if self.dash_stream_id[1] in self.dash_duct['dashaudio'][a_id]:
                #print(self.dash_duct['dashvideo'][a_id]['segmenttemplate'].keys())
                startnumber = int(self.dash_duct['dashaudio'][a_id]['segmenttemplate']['startnumber'])
                media_url = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['media'].replace('$RepresentationID$',self.dash_stream_id[1])
                init_url = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['initialization'].replace('$RepresentationID$',self.dash_stream_id[1])
                segments_ = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['segmenttimeline']
                segment_time_line = self.dash_duct['dashaudio'][a_id]['segmenttemplate']['segmenttimeline']
                bandwidth = int(self.dash_duct['dashaudio'][a_id][self.dash_stream_id[1]]['bandwidth'])
                #print(startnumber,media_url,init_url,segments_)
                self.dash_a_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], init_url)]
                for i in range(startnumber,len(segments_)+1):
                    self.dash_a_stream_urls += [urljoin(self.dash_duct['fragment_base_url'], media_url.replace('$Number$',str(i)))]
                self.dash_a_list_size = [0]+[i*bandwidth/8*1000 for i in segment_time_line]
                self.dash_a_list_size_c = [0]*len(self.dash_a_list_size)
                #for i in self.dash_a_stream_urls[:3]:
                #    print(i)
    #def compute_total_size(self):
    #    for v_id in self.dash_duct['dashvideo']:
    #        if self.dash_stream_id[0] in self.dash_duct['dashvideo'][v_id]:
    #            pass#total_dur = sum(self.dash_duct['dashvideo'][v_id]

    def print_progress(self):
        #still_downloading = True
        #counter_=0
        total_start_time = time.process_time()
        while True:
            #print(len(threading.enumerate()),threading.enumerate())
            #print([i.is_alive() for i in self.tasks1])
            #active_task_index=list()
            still_downloading = False
            for indx_,task_ in enumerate(self.tasks1):
                #if task_.is_alive():
                #    active_task_index += [indx_]
                still_downloading = still_downloading or task_.is_alive()
            #print(active_task_index)
            #print(self.progress_bar_print[0]+'\x0d',end='')
            #if len(active_task_index) ==0:
            
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
            #counter_+=1
            
    def download_link(self,url,output):
        pass
        #import time
        #import random
        #print(os.path.split(urlparse(url).path)[1])
        #time.sleep(int(random.uniform(3, 7)))
        #temp_tott =int(random.uniform(5000, 7000))
        #for i in range(0, temp_tott):
        #    print(progress_bar_(i,temp_tott)+'\x0d',end='')
        #print(self.session.get(url).headers['Content-Length'])
        with self.session.get(url, stream=True) as response:
            response.raise_for_status()
            filename = output
            #print(url)
            #print(self.dash_a_stream_urls)
            #input()
            
            if url in self.dash_v_stream_urls:
                pass#print('v ',self.dash_v_stream_urls.index(url))
                self.dash_v_list_size[self.dash_v_stream_urls.index(url)] = int(response.headers['Content-Length'])
            if url in self.dash_a_stream_urls:
                pass#print('a ',self.dash_a_stream_urls.index(url))
                self.dash_a_list_size[self.dash_a_stream_urls.index(url)] = int(response.headers['Content-Length'])
            #self.part_size[str(media_sequence)] = response.headers['Content-Length']
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
            #self.download_link(url_,output_)
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
                        #print(self.progress_bar_print)
                        #print(int(threading.current_thread().name.replace('download_thread_','')))
                        index_thread_ = int(threading.current_thread().name.replace('download_thread_',''))
                        self.progress_bar_print[index_thread_] = progress_bar_(chunk_size,
                                                                               int(response.headers['Content-Length']),
                                                                               'Part #'+str((self.dash_v_stream_urls+self.dash_a_stream_urls).index(url)),
                                                                               '%'+str(int(chunk_size/int(response.headers['Content-Length'])*100))+'@'+ part_speed)
                        if chunk:
                            f_handle.write(chunk)
                
                
                    
        

    def download_streams(self, video=True, audio=True):
        num_parts=len(self.dash_v_stream_urls)+len(self.dash_a_stream_urls)
        #num_parts=len(self.dash_v_stream_urls)
        if num_parts/self.connection_n < 2:
            self.connection_n = len(range(0,num_parts,math.ceil(num_parts/self.connection_n)))
        self.progress_bar_print = ['']*(self.connection_n+1)
        self.urls_list_r = list(self.dash_v_stream_urls+self.dash_a_stream_urls)
        self.urls_list_r.reverse()
            
            
        with tempfile.TemporaryDirectory(dir=os.path.split(self.output_v)[0]) as tempD_:
            print(tempD_)
            #print(urls_list_r.[0])
            with requests.session() as self.session:
                self.session.mount('file://', FileAdapter())
                #with ThreadPoolExecutor(max_workers=self.connection_n) as executor:
                #    pass
                #    future_to_url = {executor.submit(self.download_thread, url_, 'test'): url_ for url_ in urls_list_}
                #    print(future_to_url)
                #    
                #    for future in as_completed(future_to_url):
                #        url = future_to_url[future]
                #        data = future.result()
                print_task = threading.Thread(target=self.print_progress,name='print_thread_')
                
                #self.tasks1.append(print_task)
                #for url_ in urls_list_:
                    #task = threading.Thread(target=self.download_thread,name='download_thread_',
                    #                        args=(url_, os.path.join(tempD_,os.path.split(urlparse(url_).path)[1])))
                for n, i in enumerate(range(0,self.connection_n)):
                    #print(tempD_)
                    task = threading.Thread(target=self.download_thread,name='download_thread_'+str(n), args=([tempD_]))
                    self.tasks1.append(task)
                
                for x in self.tasks1:
                    #print(threading.active_count())
                    x.start()
                    #if threading.active_count() >= (self.connection_n+3):
                    #    for x in threading.enumerate():
                    #        if x.name == 'download_thread_':
                    #            x.join()
                                #print('test')
                                #print(self.dash_v_list_size[:4],self.dash_v_list_size_c[:4])
                                #print(size_adj(sum(self.dash_v_list_size_c+self.dash_a_list_size_c),'harddisk')+'/'+size_adj(sum(self.dash_v_list_size+self.dash_a_list_size),'harddisk'))
                                #print(progress_bar_(sum(self.dash_v_list_size_c+self.dash_a_list_size_c),
                                #                    sum(self.dash_v_list_size+self.dash_a_list_size),
                                #                    size_adj(sum(self.dash_v_list_size_c+self.dash_a_list_size_c),'harddisk')+'/'+size_adj(sum(self.dash_v_list_size+self.dash_a_list_size),'harddisk'),
                                #                    text_end='%'+str(int(100*sum(self.dash_v_list_size_c+self.dash_a_list_size_c)/sum(self.dash_v_list_size+self.dash_a_list_size))))+'\x0d',end='')
                                                    
                                #break
                print_task.start()
                for x in self.tasks1:
                    x.join()
                print_task.join()

                
                        

                #while True:
                #    print(threading.enumerate())
                #    import time
                #    time.sleep(5)
                #for x in self.tasks1:
                #    print(threading.active_count() )
                #    x.join()
            

            vfiles=[os.path.split(urlparse(url_).path)[1] for url_ in self.dash_v_stream_urls]
            afiles=[os.path.split(urlparse(url_).path)[1] for url_ in self.dash_a_stream_urls]
            #for file in os.listdir(tempD_):
            #    print(file)
            #print(vfile)
            with open(self.output_v, 'wb') as outfile:
                for fname in vfiles:
                    with open(os.path.join(tempD_,fname), 'rb') as infile:
                        while True:
                            byte = infile.read(blocksize)
                            if not byte:
                                break
                            outfile.write(byte)
            with open(self.output_a, 'wb') as outfile:
                for fname in afiles:
                    with open(os.path.join(tempD_,fname), 'rb') as infile:
                        while True:
                            byte = infile.read(blocksize)
                            if not byte:
                                break
                            outfile.write(byte)
                            
                

            input()
            for n, i in enumerate(range(0,num_parts,math.ceil(num_parts/self.connection_n))):
                pass#print(n,i)

        '''
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
'''
        
        print(num_parts)
        if video:
            for url_ in self.dash_v_stream_urls[:3]:
                print(url_)
                #wget.download(url_)
        '''
        if audio:
            for url_ in self.dash_a_stream_urls:
                wget.download(url_)
        #'''
            

            

    #def download(self, url=None, output=None, connection_n=1, resolution = None, audio_br = None):
    def download(self, url=None, output=None, connection_n=1, video=True, audio=True, **kwargs):
        if url is None:
            url = input('dashlink>>')
        self.url_ = url
        if not output is None:
            #output = 'download.mp4'
            self.output_v = os.path.abspath(output)
            self.output_a = os.path.abspath(output[:-4]+'.m4a')
        
        #if os.path.split(output)[0] == '':   
        #if type(resolution) == int:
        #    self.resolution = resolution
        #if type(audio_br) == int:
        #    self.audio_br = audio_br
        #self.output = output
        self.connection_n = connection_n
        # '''
        self.parse_dash()
        print(self.dash_duct)
        '''
        self.dash_duct = {'dashvideo': {'1': {'id': '1', 'segmentalignment': True, 'maxwidth': 1920, 'maxheight': 1080,
                             'maxframerate': 23.97442727757059,
                             'f1-v1-x3': {'id': 'f1-v1-x3', 'mimetype': 'video/mp4', 'codecs': 'avc1.640028',
                                          'width': 1280, 'height': 720, 'framerate': 23.97442727757059, 'sar': '1:1',
                                          'startwithsap': 1, 'bandwidth': 2824.695},
                             'segmenttemplate': {'timescale': '1000',
                                                 'media': 'fragment-$Number$-$RepresentationID$.m4s?t=st=1573330067~exp=1573416467~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=052604aec47a9710e220a825e9752ec292c565b5949e6acf426338dc76003444',
                                                 'initialization': 'init-$RepresentationID$.mp4?t=st=1573330067~exp=1573416467~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=052604aec47a9710e220a825e9752ec292c565b5949e6acf426338dc76003444',
                                                 'startnumber': '1',
                                                 'segmenttimeline': [4.004, 4.004, 5.422, 9.51, 11.094, 10.01, 9.218,
                                                                     10.01, 9.843, 10.01, 9.927, 10.01, 11.22, 10.01,
                                                                     10.01, 9.259, 10.01, 10.719, 8.509, 11.011, 9.551,
                                                                     10.093, 6.548]},
                             'f2-v1-x3': {'id': 'f2-v1-x3', 'mimetype': 'video/mp4', 'codecs': 'avc1.640028',
                                          'width': 1920, 'height': 1080, 'framerate': 23.97442727757059, 'sar': '1:1',
                                          'startwithsap': 1, 'bandwidth': 6020.488},
                             'f3-v1-x3': {'id': 'f3-v1-x3', 'mimetype': 'video/mp4', 'codecs': 'avc1.4d401f',
                                          'width': 848, 'height': 480, 'framerate': 23.97442727757059, 'sar': '1:1',
                                          'startwithsap': 1, 'bandwidth': 1310.518},
                             'f4-v1-x3': {'id': 'f4-v1-x3', 'mimetype': 'video/mp4', 'codecs': 'avc1.4d401e',
                                          'width': 640, 'height': 360, 'framerate': 23.97442727757059, 'sar': '1:1',
                                          'startwithsap': 1, 'bandwidth': 568.746},
                             'f5-v1-x3': {'id': 'f5-v1-x3', 'mimetype': 'video/mp4', 'codecs': 'avc1.42c015',
                                          'width': 428, 'height': 240, 'framerate': 23.97442727757059, 'sar': '1:1',
                                          'startwithsap': 1, 'bandwidth': 423.361}}}, 'dashaudio': {
            '2': {'id': '2', 'segmentalignment': True,
                  'f1-a1-x3': {'id': 'f1-a1-x3', 'mimetype': 'audio/mp4', 'codecs': 'mp4a.40.2',
                               'audiosamplingrate': 44100, 'startwithsap': 1, 'bandwidth': 128.011},
                  'segmenttemplate': {'timescale': '1000',
                                      'media': 'fragment-$Number$-$RepresentationID$.m4s?t=st=1573330067~exp=1573416467~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=052604aec47a9710e220a825e9752ec292c565b5949e6acf426338dc76003444',
                                      'initialization': 'init-$RepresentationID$.mp4?t=st=1573330067~exp=1573416467~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_*~hmac=052604aec47a9710e220a825e9752ec292c565b5949e6acf426338dc76003444',
                                      'startnumber': '1',
                                      'segmenttimeline': [2.508, 4.992, 5.016, 9.985, 10.008, 10.008, 9.985, 10.008,
                                                          10.008, 9.985, 10.008, 10.008, 9.985, 10.008, 10.008, 9.985,
                                                          10.008, 10.008, 9.985, 10.008, 10.008, 9.985, 7.597]},
                  'f3-a1-x3': {'id': 'f3-a1-x3', 'mimetype': 'audio/mp4', 'codecs': 'mp4a.40.2',
                               'audiosamplingrate': 44100, 'startwithsap': 1, 'bandwidth': 96.008},
                  'f5-a1-x3': {'id': 'f5-a1-x3', 'mimetype': 'audio/mp4', 'codecs': 'mp4a.40.2',
                               'audiosamplingrate': 22050, 'startwithsap': 1, 'bandwidth': 64.012}}},
         'dashsubtitle': {},
         'url': 'https://dl.v.vrv.co/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/manifest.mpd?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cCo6Ly9kbC52LnZydi5jby9ldnMvMmQ2MGMwYTY2MDY0MjRiY2U3NzcyYzBkZGMzMzViMDgvYXNzZXRzLzY0b3VtbG83anM0NG5ndl8sMjEzMzAwOS5tcDQsMjEzMzAyNS5tcDQsMjEzMjk5My5tcDQsMjEzMjk3Ny5tcDQsMTAzODk0My5tcDQsLnVybHNldC9tYW5pZmVzdC5tcGQiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NzMzODE0NzZ9fX1dfQ__&Signature=fYmQV9q4yvLPyQ7ZpOwqt~gaYnDzCPQgfYYEse4ebI-863T5wjEOoWfgiCz517e3tsIudOkYatLYJxxZ7Ewm5mwKpGQHt5w~rIUQ7HtexYdA-vnpr~eukEwYkqD~njaMPLsacQz6EGGSSfq3TBsm84SLRdY4Yp8HoTadl26NEjlHYEwOQjmSNwo0GzDr-nUN3fG3S8GpC0w1xE9GxDc2dpdsSsPNsp9c8T1RO7Sdd23KmvutyetSrrWePJkeNJ2lhvShnydUXsjBkU4suIfGbbGs5s2Y9cxDIS-vBn-n57432c1BN79xBg8Ulu88BDDsGsS0Ko07MGmaYPik6w97~Q__&Key-Pair-Id=DLVR',
         'manifest_url': 'https://a-vrv.akamaized.net/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/manifest.mpd?t=exp=1573381476~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/*~hmac=77ac0deec3f6b384b7ab26ee5aa46b9b4cbc38e1dc871bf83eb8c0d0f41b65d3',
         'id': '*~hmac=77ac0deec3f6b384b7ab26ee5aa46b9b4cbc38e1dc871bf83eb8c0d0f41b65d3',
         'fragment_base_url': 'https://a-vrv.akamaized.net/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/manifest.mpd?t=exp=1573381476~acl=/evs/2d60c0a6606424bce7772c0ddc335b08/assets/64oumlo7js44ngv_,2133009.mp4,2133025.mp4,2132993.mp4,2132977.mp4,1038943.mp4,.urlset/'}
        self.dash_duct['fragment_base_url'] = urlunparse(urlparse(urljoin(('file:///'+os.path.join(os.path.abspath('frag/'),'dump.tmp')).replace('\\','/'),urlparse(self.dash_duct['fragment_base_url']).path.split('/')[-1]))._replace(params=urlparse(self.dash_duct['fragment_base_url']).params, query=urlparse(self.dash_duct['fragment_base_url']).query, fragment=urlparse(self.dash_duct['fragment_base_url']).fragment))
        
        #'''
        self.find_best_stream(kwargs)
        #print(self.video_br, self.audio_br,self.dash_stream_id)
        print(self.dash_stream_id)
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
