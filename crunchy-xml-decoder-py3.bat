@echo off
set PYTHONHTTPSVERIFY=0 
rem RD "%PUBLIC%\Crunchyroll-XML-Decoder_link" 1>NUL 2>NUL
rem mklink /j "%PUBLIC%\Crunchyroll-XML-Decoder_link" %cd% 1>NUL 2>NUL
rem cd "%PUBLIC%\Crunchyroll-XML-Decoder_link"
:sratre
crunchy-xml-decoder-py3.py %1 %2 %3 %4 %5 %6 %7 %8 %9
rem RD "%PUBLIC%\Crunchyroll-XML-Decoder_link" 1>NUL 2>NUL
pause

