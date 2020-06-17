#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
from getpass import getpass
from configparser import ConfigParser
import random
import string
from colorama import Fore, Style, init
init()
import time

#import urllib.parse
#from requests import Request


try:
  import html2text
  h = html2text.HTML2Text()
  h.ignore_links = True
  h.ignore_emphasis = True
  h.body_width = 0
except:
  pass

from altfuncs import config
from proxy_cr import get_proxy
#def config():
#  return {'proxy':'', 'forceusa': True}
#def get_proxy(x,y):
#  return ['']

def getuserstatus(sess_id_renew = False, sess_id = ''):
    status = 'Guest'
    user1 = 'Guest'
    sess_id_usa = ''
    
    device_id = ''
    device_id_usa = ''
    auth = ''

    session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    if sess_id =='':
        device_id = cookies_.get('COOKIES', 'device_id')
        device_id_usa = cookies_.get('COOKIES', 'device_id_usa')
        sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
        sess_id = cookies_.get('COOKIES', 'sess_id')
        auth = cookies_.get('COOKIES', 'auth')
    checkusaid = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id).json()
    if config()['forceusa']:
      checkusaid_us = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id_usa).json()
      if checkusaid_us['code'] != 'ok':
        sess_id_renew = True
    else:
      sess_id_usa = ''
    #print(checkusaid)
    if checkusaid['code'] != 'ok':
      sess_id_renew = True
      #if checkusaid['country_code'] != 'US' and config()['forceusa'] and sess_id_usa != '':
      #  checkusaid_us = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id_usa).json()
      #  print(checkusaid_us)
      #  if checkusaid_us['code'] != 'ok':
      #    sess_id_renew = True
    
    if sess_id_renew:
      session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_usa)
      session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id)

      generate_sess_id = create_sess_id(auth=auth)
      sess_id = generate_sess_id['sess_id']
      device_id = generate_sess_id['device_id']
      #proxies = generate_sess_id['proxies']
      generate_sess_id['country_code'] = 'JO'
      if generate_sess_id['country_code'] != 'US' and  config()['forceusa']:
        #print('us seesss')
        generate_sess_id_usa = create_sess_id(True,auth=auth)
        sess_id_usa = generate_sess_id_usa['sess_id']
        device_id_usa = generate_sess_id_usa['device_id']

      checkusaid = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id).json()
      #print(checkusaid)
      cookies_out = '''\
[COOKIES]
device_id = {}
device_id_usa = {}
sess_id = {}
sess_id_usa = {}
auth = {}
'''.format(device_id, device_id_usa, sess_id, sess_id_usa, auth)
        # open("cookies", "w").write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
      open("cookies", "w").write(cookies_out)

    
    if not checkusaid['data']['user'] is None:
      user1 = checkusaid['data']['user']['username']
      if checkusaid['data']['user']['premium'] == '':
        status = 'Free Member'
      else:
        if checkusaid['data']['user']['access_type'] == 'premium_plus':
          status = 'Premium Plus'
        else:
          status = 'Premium'
    
    #print(1,[status, user1])
    return [status, user1]

        

    

def create_sess_id(usa_=False, auth = ''):
  session = requests.session()
  proxies = {}
  device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32))
  payload = {'device_id': device_id, 'api_ver': '1.0',
              'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'WveH9VkPLrXvuNm', 'version': '2313.8',
              'locale': 'jaJP', 'duration': '9999999999'}
  if auth != '':
    payload.update({'auth' : auth})

  if usa_:
    sess_id_data = {'session_id': ''}
    ### First Method
    p_usa_session_post = requests.Request('GET', 'https://api.crunchyroll.com/start_session.0.json', params=payload).prepare()
    #encoded_usa_session_post_url = urllib.parse.quote(p_usa_session_post.url, safe='')
    google_p_params = {'container' : 'focus', 'url' : p_usa_session_post.url}
    retries = 5
    retries_o = retries+1
    while retries >=0:
      print('using g_proxy retry #{}'.format(retries_o-retries))
      usa_session_post = session.post('https://images-focus-opensocial.googleusercontent.com/gadgets/proxy', params=google_p_params)
      if usa_session_post.status_code == 200:
        break
      else:
        retries -= 1
        time.sleep(30)   #30 sec sleep to not over heat server
    try:
      if usa_session_post.json()['error'] != "true":
        sess_id_data = usa_session_post.json()['data']
    except:
      try:
        print(h.handle(usa_session_post.text))
      except:
        print(usa_session_post.content)
        #exit()
    
    if sess_id_data['session_id'] == '': ### Second Method
      #print("Second Method")
      for prxy_ in get_proxy(['HTTPS'],['US']):
        proxies = {'https': prxy_}
        try:
          usa_session_post = session.post('https://api.crunchyroll.com/start_session.0.json', proxies=proxies,
          params=payload).json()
          sess_id_data = usa_session_post['data']
        except:
          pass

    if sess_id_data['session_id'] == '': ### Third Method
      #print("Third Method")
      try:
        usa_session_post = session.get('http://rssfeedfilter.netne.net/').json()
        sess_id_data['session_id'] = usa_session_post['sessionId']
      except:
        print('\x1b[31m'+'Could Not Create USA Session'+'\x1b[0m')
        print('\x1b[31m'+'You Will Not be Able to Download USA Locked Anime at Moment'+'\x1b[0m')
        print('\x1b[31m'+'Try Again Later'+'\x1b[0m')

    

  else:
    sess_id_data = {'session_id': ''}
    if config()['proxy'] != '':
      proxy_ = get_proxy(['HTTPS'], [config()['proxy']])
      try:
        proxies = {'http': proxy_[0]}
      except:
        proxies = {}
    try:
      sess_id_data = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']
    except requests.exceptions.ProxyError:
      sess_id_data = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']
    #print(sess_id_data)
  returned_data = {'sess_id' : sess_id_data['session_id'], 'device_id': device_id, 'proxies': proxies, 'country_code': sess_id_data['country_code']}
    
  return returned_data

def login(username, password):
    session = requests.session()
    device_id = ''
    device_id_usa = ''
    sess_id = ''
    sess_id_usa = ''
    auth = ''
    #session = requests.session()
    #device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    #device_id_usa = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    #payload_usa = {'device_id': device_id_usa, 'api_ver': '1.0',
    #           'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'WveH9VkPLrXvuNm', 'version': '2313.8',
    #           'locale': 'jaJP', 'duration': '9999999999'}
    #payload = {'device_id': device_id, 'api_ver': '1.0',
    #           'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'WveH9VkPLrXvuNm', 'version': '2313.8',
    #           'locale': 'jaJP', 'duration': '9999999999'}
    #if config()['proxy'] != '':
    #    proxy_ = get_proxy(['HTTPS'], [config()['proxy']])
    #    try:
    #        proxies = {'http': proxy_[0]}
    #    except:
    #        proxies = {}
    #else:
    #    proxies = {}


    
    generate_sess_id = create_sess_id()
    sess_id = generate_sess_id['sess_id']
    device_id = generate_sess_id['device_id']
    proxies = generate_sess_id['proxies']
    #generate_sess_id['country_code'] = 'JO'
    #print(generate_sess_id['country_code'], 'forceusa:'+str(config()['forceusa']), generate_sess_id['country_code'] != 'US' and  config()['forceusa'])
    if generate_sess_id['country_code'] != 'US' and  config()['forceusa']:
      #print('us seesss')
      generate_sess_id_usa = create_sess_id(True)
      sess_id_usa = generate_sess_id_usa['sess_id']
      device_id_usa = generate_sess_id_usa['device_id']

    #print(sess_id_usa)
    #try:
    #    sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
    #except requests.exceptions.ProxyError:
    #    sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    #auth = ''
    if username != '' and password != '':
        payload = {'session_id' : sess_id,'locale': 'jaJP','duration': '9999999999','account' : username, 'password' : password}
        try:
            auth = session.post('https://api.crunchyroll.com/login.0.json', params=payload).json()['data']['auth']
        except:
            pass
    userstatus = getuserstatus(False, sess_id)
    #print(userstatus)
    if username != '' and userstatus[0] == 'Guest':
        print('Login failed.' if 'idlelib.run' in sys.modules else '\x1b[31m' + 'Login failed.' + '\x1b[0m')
    # sys.exit()
    else:
        print('Login as ' + userstatus[1] + ' successfully.' if 'idlelib.run' in sys.modules else 'Login as ' + '\x1b[32m' + userstatus[1] + '\x1b[0m' + ' successfully.')
    payload = {'device_id': device_id, 'api_ver': '1.0',
               'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'WveH9VkPLrXvuNm', 'version': '2313.8',
               'locale': 'jaJP', 'duration': '9999999999', 'auth': auth}
    try:
        sess_id = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
    except requests.exceptions.ProxyError:
        sess_id = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    cookies_out = '''\
[COOKIES]
device_id = {}
device_id_usa = {}
sess_id = {}
sess_id_usa = {}
auth = {}
'''.format(device_id, device_id_usa, sess_id, sess_id_usa, auth)
        # open("cookies", "w").write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
    open("cookies", "w").write(cookies_out)
    return userstatus

def check_sess_id():
    getuserstatus()
    session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    sess_id = cookies_.get('COOKIES', 'sess_id')
    sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
    checkusaid = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id)
    checkusaid_usa = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id_usa)
    if checkusaid.json()['code'] == 'ok':
        print('sess_id linked to:',checkusaid.json()['data']['country_code'])
        try:
          print('sess_id_usa linked to:',checkusaid_usa.json()['data']['country_code'])
        except:
          pass
    else:
        print('something gone wroung')

if __name__ == '__main__':
    #print(sys.argv[1])
    if len(sys.argv) == 1:
        #print(getuserstatus())
        check_sess_id()
        #username = input(u'Username: ')
        #password = getpass('Password(don\'t worry the password are typing but hidden:')
        #login(username, password)
    elif sys.argv[1] == '-getuserstatus':
        getuserstatus()
    elif sys.argv[1] == '-check_sess_id':
        check_sess_id()
    elif len(sys.argv) == 2:
        username = sys.argv[1]
        password = getpass('Password(don\'t worry the password are typing but hidden:')
        login(username, password)
    elif len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]
        login(username, password)
    else:
        username = ''
        password = ''
        login(username, password)
