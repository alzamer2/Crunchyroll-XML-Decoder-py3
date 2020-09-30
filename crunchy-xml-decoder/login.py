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
#import cloudscraper
import re
from cryptography.fernet import Fernet

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
    """
    status = 'Guest'
    user1 = 'Guest'
    sess_id_usa = ''
    
    device_id = ''
    device_id_usa = ''
    auth = ''
    auth2 = ''
    session = cloudscraper.create_scraper(interpreter='nodejs')
    #https://www.crunchyroll.com/acct/membership
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    if sess_id =='':
      device_id = cookies_.get('COOKIES', 'device_id')
      device_id_usa = cookies_.get('COOKIES', 'device_id_usa')
      sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
      sess_id = cookies_.get('COOKIES', 'sess_id')
      auth = cookies_.get('COOKIES', 'auth')
      if 'auth2' in cookies_.options('COOKIES'):
        auth2 = cookies_.get('COOKIES', 'auth2')
    checkid = session.get('https://www.crunchyroll.com/acct/membership')
    username_check = re.findall('''<li class="username">.*?\n.*?<a href="/user/.+?" token="topbar">.*?\n +(.+?)\n.*?</a>''',checkid.text)
    print(username_check)
    if username_check:
      user1 = username_check[0]
    status_check = re.findall('''<table class="acct-membership-status">.*?\n.*?<tr>.*?\n.*?\
<th>Status:</th>.*?\n.*?<td>(.+?)</td>.*?\n.*?</tr>.*?\n.*?</table>''',checkid.text)
    if status_check:
      status = status_check[0]
    print(status, user1)
    return [status, user1]
      
"""
    status = 'Guest'
    user1 = 'Guest'
    sess_id_usa = ''
    
    device_id = ''
    device_id_usa = ''
    auth = ''
    auth2 = ''

    #session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    if sess_id =='':
        device_id = cookies_.get('COOKIES', 'device_id')
        device_id_usa = cookies_.get('COOKIES', 'device_id_usa')
        sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
        sess_id = cookies_.get('COOKIES', 'sess_id')
        auth = cookies_.get('COOKIES', 'auth')
        if 'auth2' in cookies_.options('COOKIES'):
          auth2 = cookies_.get('COOKIES', 'auth2')
    resp = requests.get('http://api.crunchyroll.com/start_session.0.json', params={'session_id' : sess_id})
    checkusaid = resp.json()
    #print('test1',resp)
    #print(resp.url)
    #print(checkusaid)
    if config()['forceusa']:
      resp = requests.get('http://api.crunchyroll.com/start_session.0.json', params={'session_id' : sess_id_usa})
      checkusaid_us = resp.json()
      #print('test2',resp)
      #print(resp.url)
      #print(checkusaid_us)
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
      requests.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_usa)
      requests.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id)

      if not auth2:
        return ['Guest', 'Guest']

      re_username, re_password = extrct_auth2(auth2)
      #print(re_username, re_password)
      re_login_status = login(re_username, re_password)
      return re_login_status
      """

      generate_sess_id = create_sess_id()
      sess_id = generate_sess_id['sess_id']
      device_id = generate_sess_id['device_id']
      #proxies = generate_sess_id['proxies']
      #generate_sess_id['country_code'] = 'JO'
      if generate_sess_id['country_code'] != 'US' and  config()['forceusa']:
        #print('us seesss')
        generate_sess_id_usa = create_sess_id(True)
        sess_id_usa = generate_sess_id_usa['sess_id']
        device_id_usa = generate_sess_id_usa['device_id']

      checkusaid = requests.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id).json()
      print('test3')
      print(checkusaid)
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

    """
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
  headers = {'Referer': 'http://crunchyroll.com/'}
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
      usa_session_post = session.post('https://images-focus-opensocial.googleusercontent.com/gadgets/proxy', params=google_p_params, headers=headers)
      #print(usa_session_post.json())
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
    auth2 = ''
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
    #print(generate_sess_id)
    sess_id = generate_sess_id['sess_id']
    device_id = generate_sess_id['device_id']
    proxies = generate_sess_id['proxies']
    #generate_sess_id['country_code'] = 'JO'
    ##print(generate_sess_id['country_code'], 'forceusa:'+str(config()['forceusa']), generate_sess_id['country_code'] != 'US' and  config()['forceusa'])
    if generate_sess_id['country_code'] != 'US' and  config()['forceusa']:
      ##print('us seesss')
      generate_sess_id_usa = create_sess_id(True)
      sess_id_usa = generate_sess_id_usa['sess_id']
      device_id_usa = generate_sess_id_usa['device_id']

    ##print(sess_id_usa)
    #try:
    #    sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
    #except requests.exceptions.ProxyError:
    #    sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    #auth = ''
    if username != '' and password != '':
        #print('test1')
        auth2 = generate_auth2(username, password)
        payload = {'session_id' : sess_id,'locale': 'jaJP','duration': '9999999999','account' : username, 'password' : password}
        try:
            respond = session.post('https://api.crunchyroll.com/login.0.json', params=payload)
            #print(respond,respond.text)
            #print(respond.url)
            auth = respond.json()['data']['auth']
            
        except:
            pass
        if sess_id_usa:
            payload = {'session_id' : sess_id_usa,'locale': 'jaJP','duration': '9999999999','account' : username, 'password' : password}
            try:
                respond = session.post('https://api.crunchyroll.com/login.0.json', params=payload)
                #print(respond,respond.text)
                #print(respond.url)
            except:
                pass
    #input()
    #payload = {'device_id': device_id, 'api_ver': '1.0',
    #           'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'WveH9VkPLrXvuNm', 'version': '2313.8',
    #           'locale': 'jaJP', 'duration': '9999999999', 'auth': auth}
    #try:
    #    respond = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload)
    #    print(respond, respond.text)
    #    print(respond.url)
    #    input()
    #    sess_id = respond.json()['data']['session_id']
    #except requests.exceptions.ProxyError:
    #    sess_id = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    
    cookies_out = '''\
[COOKIES]
device_id = {}
device_id_usa = {}
sess_id = {}
sess_id_usa = {}
auth = {}
auth2 = {}
'''.format(device_id, device_id_usa, sess_id, sess_id_usa, auth, auth2)
        # open("cookies", "w").write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
    open("cookies", "w").write(cookies_out)
    userstatus = getuserstatus(False)
    #userstatus = ['1','1']
    #print(userstatus)
    if username != '' and userstatus[0] == 'Guest':
        print('Login failed.' if 'idlelib.run' in sys.modules else '\x1b[31m' + 'Login failed.' + '\x1b[0m')
    # sys.exit()
    else:
        print('Login as ' + userstatus[1] + ' successfully.' if 'idlelib.run' in sys.modules else 'Login as ' + '\x1b[32m' + userstatus[1] + '\x1b[0m' + ' successfully.')
    
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
def generate_auth2(username__, password__):
  key = Fernet.generate_key()
  f = Fernet(key)
  username__ = '[{username='+username__+'}]'
  password__ = '[{password='+password__+'}]'
  pad_1 = ''
  pad_2 = ''
  pad_3 = ''
  pad_1_length = random.randint(1, 256-(len(username__)+len(password__)+2))
  #print(pad_1_length)
  for i in range(0,pad_1_length):
    pad_1 += random.sample(string.ascii_letters + string.digits, 1)[0]
  #print(len(pad_1))
  #pad_1 = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1,pad_1_length)))
  pad_2_length = random.randint(1, 256-(pad_1_length+len(username__)+len(password__)+1))
  for i in range(0,pad_2_length):
    pad_2 += random.sample(string.ascii_letters + string.digits, 1)[0]
  #pad_2 = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(1,pad_2_length)))
  pad_3_length = 256-(pad_1_length+len(username__)+pad_2_length+len(password__))
  for i in range(0,pad_3_length):
    pad_3 += random.sample(string.ascii_letters + string.digits, 1)[0]
  #pad_3 = ''.join(random.sample(string.ascii_letters + string.digits, pad_3_length))
  auth2 = pad_1+username__+pad_2+password__+pad_3
  key_file = """\
def get_key():
    return '{}'
""".format(key.decode()).encode()
  open('key.py','wb').write(key_file)
  return f.encrypt(auth2.encode()).decode()

def extrct_auth2(auth2):
  from key import get_key
  key = get_key()
  f = Fernet(key.encode())
  user_pass_ = re.findall('\[\{username=(.+?)\}\].+\[\{password=(.+?)\}\]',f.decrypt(auth2.encode()).decode())[0]
  return user_pass_

if __name__ == '__main__':
    #print(sys.argv[1])
    if len(sys.argv) == 1:
        #print(getuserstatus())
        check_sess_id()
        #username = input(u'Username: ')
        #password = getpass('Password(don\'t worry the password are typing but hidden:')
        #login(username, password)
    elif sys.argv[1] == '-getuserstatus':
        print(getuserstatus())
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
