# -*- coding: utf-8 -*-

import urllib2
import sys

#url = "https://api.github.com/yupe/yupe/issues"
#url = "https://api.github.com/repos/yupe/yupe/issues"

params = {"server": "api.github.com"}
#allow_params = ("server", "repouser", "reponame", "state", "since", "mentioned", "milestone", "label", "format")
config_file = ".githop"


def isUpHTTP(url):
    #ssl._create_default_https_context = ssl._create_unverified_context
    result = True

    try:
        result = urllib2.urlopen(url).read()
    except:
        result = False
    return result


def add_param(name, value):
    #default values
    #params["server"] = "api.github.com"
    #if name in allow_params:

    params[name] = value
    # else: throw "Invalid argument exception"


def check_param(param):
    pass


def get_params_from_command_prompt():
    for arg in sys.argv:
        try:
            hlp = arg.split(':')
            add_param(hlp[0], hlp[1])
        except:
            pass


def get_params_from_file():
    f = open(config_file)
    lines = f.readlines()
    f.close()
    for line in lines:
        try:
            print line
            hlp = line.split('=')
            add_param(hlp[0].strip(), hlp[1].strip())
        except:
            pass


def create_url():
    #Exit with error if mustHave params not present
    #url = "https://\s/repos/\s/\s/issues/" % (params.pop("server"), params.pop("repouser"), params.pop("reponame"))
    url = "https://{0}/repos/{1}/{2}/issues".format(params.pop("server"), params.pop("repouser"), params.pop("reponame"))

    #if params:
     #   url += '?'
        #''.join([url, "?"])


    #Ignore if params not present
    #for (key, value) in params.items():
    par = ','.join(["%s=%s" % (k, v) for k, v in params.items()])
    if par:
        url = url + '?' + par
    return url



def get_url(url):
    try:
        result = urllib2.urlopen(url).read()
    except:
        result = "Url error %s", url
    return result


def parse_url():
    for param in sys.argv:
        print param

#params = {}

get_params_from_file()
get_params_from_command_prompt()
#print params.pop("server")
url = create_url()
print url
#print get_url("https://api.github.com/repos/yupe/yupe/issues")