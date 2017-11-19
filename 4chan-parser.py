#!/usr/bin/env python3

from filedownloader import file_downloader

import sys
import json
if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse

def open_url(url):
    try:
        response = urllib2.urlopen(url)
    except:
        raise
    else:
        # everything is fine
        output = response.read().decode('utf-8');
        return output
    return None

def get_image(board,thread):
    url = 'http://a.4cdn.org/'+board+'/thread/'+thread+'.json'
    output = open_url(url)
    if output:
        # Parse for success or failure
        out = json.loads(output)
        for post in out['posts']:
            print(post)
            try:
                tim = str(post['tim'])
                ext = str(post['ext'])
            except KeyError:
                continue
            image_url = 'http://i.4cdn.org/' + board+'/' + tim + ext
            print(image_url)
            file_downloader.download(image_url)

def catalog_list(board):
    url = 'http://a.4cdn.org/'+board+'/catalog.json'
    output = open_url(url)
    if output:
        out = json.loads(output)
        for page in out:
            for thread in page['threads']:
                print('-------------------------------------')
                try:
                    print(thread['sub'])
                    print(thread['com'])
                    print(thread['no'])
                    print(thread['semantic_url'])
                except KeyError:
                    continue


def main(argv):
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-t", "--thread", dest="thread",
                     help="Thread number", metavar="THREAD")
    parser.add_option("-b", "--board", dest="board",
                     help="Board name", metavar="BOARD")
    (options, args) = parser.parse_args()
    if options.board:
        if options.thread:
            get_image(options.board,options.thread)
        else:
            catalog_list(options.board)
    else:
        print('Weird arguments, look at -h')

if __name__ == '__main__':
    try:
        main(sys.argv);
    except KeyboardInterrupt:
        print('\nGracefully exiting')
    except:
        raise
