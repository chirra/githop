# -*- coding: utf-8 -*-

import urllib2

#url = "https://api.github.com/yupe/yupe/issues"
url = "https://api.github.com/repos/yupe/yupe/issues"

def isUpHTTP(url):
    #ssl._create_default_https_context = ssl._create_unverified_context
    result = True

    try:
        result = urllib2.urlopen(url).read()
    except:
        result = False
    return result

data = isUpHTTP(url)
for line in data.split(','):
    print line