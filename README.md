# Crunchyroll-XML-Decoder-py3


ORIGINALLY BY @einstein95

Requires Python modules:

* Node.js is required for (safe) Javascript execution. Your computer or server may already have it (check with node -v). If not, you can install it with apt-get install nodejs on Ubuntu and Debian. Otherwise, please read ( https://nodejs.org/en/download/package-manager/ )Node's installation instructions.

### Requires Python modules(autoinstall dont need to download):

* lxml (https://pypi.python.org/pypi/lxml/3.2.5)
* m3u8 (https://pypi.python.org/pypi/m3u8/)
* cfscrape (https://pypi.python.org/pypi/cfscrape/)
* requests
* colorama
* cryptography==2.4.2
* m3u8
* beautifulsoup4
* pager
* unidecode
* wget

This is a composite of various scripts required to download video files from CrunchyRoll that have been automated with a batch file.

### INSTRUCTIONS:

Pre-Setup (Only need to do these once.):
1.  Install Python 3.4.0 or newer
2.  Run crunchy-xml-decoder.bat or crunchy-xml-decoder.py to generate necessary files (settings.ini and cookies)
3.  choices	from the option 

for Linux user:

you need to prepare wine32 environment:

i'm not that expert in liunix system but thanks to @RGFRv2 he gave me some tips

for those that don't know:
1. connected directly as root with:
`dpkg --add-architecture i386 && apt-get update && apt-get install wine32`
2. update in case with:
`sudo apt-get update`

Per-Video Process:
1.  Copy the URL of the CrunchyRoll video you want to download from your web browser
2.  Run crunchy-xml-decoder-py3.bat or crunchy-xml-decoder-py3.py choice 1 and paste link
3.  Download will start automatically. Everything is automated.
4.  Browse to the 'export' folder to view the completed file.

SPECIAL NOTE: There is another batch file in the _run folder..
    Run crunchy-xml-decoder-py3.bat or crunchy-xml-decoder-py3.py choice 2 and paste link
        Just want the subtitles to an episode? OK.. fair 'nuff. Use this.

#### WHAT IS THE POINT OF THIS SCRIPT? WHAT IS IT ACTUALLY DOING?:

The process of getting a working download from CrunchyRoll is effectively doing the following:
* Downloading and decrypting subtitles
* Downloading the video as FLV or MPEG-TS
* Splitting the FLV/TS file into 264 video and aac audio
* Merging video, audio, and subtitles into a mkv file
* Naming the new video something other than 'video.mkv'

NOTES FROM THE AUTHORS:
> From the DX author: Yeah, I wrote the basis for this "new 'n' improved version". Basically, I monitored the traffic to and from Crunchyroll while a video was loading, found a few (read: a lot of) similarities, and basically wrote the script to do the same thing, but parse the file and call upon RTMPdump to dump the video (RTMPexplorer was doing the same thing basically).

From the anonymous original author:
>I did not write these programs, and I didn't even come up with this method. All I have done is created a few little bat files to bring them together. Original instructions on how this is done can be found here: 
>
> http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-%28noob-friendly%29
#### DOS Arguments Help:
  -h, --help                    show this help message and exit
  
  -d URL, --download URL        Download Crunchyroll Anime Link
  
  -s URL, --subtitle URL        Download Crunchyroll Anime Subtitles only
  
  -l usename password,          Login with your Crunchyroll Account
   --Login usename password         
                
  -g, --guest                   Login As Guest
  
  -a URL, --autocatch URL       Download an entire Anime
  
  -q [Queue Directory],
  --queue [Queue Directory]     Run List of Crunchyroll Anime Link in queue file
                        
  -D, --default                 Restore Default Settings
  
  --debug                       Run Code in Debug Mode


#### What new:

* new way for login that dont need cfscrape
* add progressbar to download
* add color for console
* use new way to get video url which include Hardsub video and 240p
* new way to get usa sesson_id
* add new proxy function
* cleaned HLS code and removed extra parts, now its faster
* add Pretty Menu
* add DASH stream download
* add YoutubeDL support
* add Dos argument

#### What TO-DO:

* clean the code from unused lines and codes


