#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('crunchy-xml-decoder')
#globals().update(vars(__import__('crunchy-xml-decoder-py3')))
locals().update({'crunchy_xml_decoder_py3':__import__('crunchy-xml-decoder-py3')})
#globals().update({'proxy_cr':__import__('proxy_cr')})
#print(globals())
if __name__ == '__main__':
    #proxy_cr.get_proxy(['HTTPS'],['US'])
    #crunchy_xml_decoder_py3.make_choise()
    crunchy_xml_decoder_py3.menu_test.start_()
    #debug(test_)
    #print('done?')
    #input()
