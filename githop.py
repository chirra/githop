# -*- coding: utf-8 -*-

import urllib2
import sys
import json


params = {"server": "api.github.com"}
config_file = ".githop"


def add_param(name, value):
    params[name] = value


def get_params_from_command_prompt():
    if len(sys.argv) < 2:
        print "Usage: githop user repositarium [server=githubserver] [since=YYYY-MM-DDTHH:MM:SSZ] [state=open|close] " \
              "[assignee=<username>] [labels=<label1>,<label2>,..,<labelN>] [milestone=<milestone>]"
    for arg in sys.argv[1:]:
        try:
            hlp = arg.split('=')
            add_param(hlp[0], hlp[1])
        except:
            pass


def get_params_from_file():
    f = open(config_file)
    lines = f.readlines()
    f.close()

    for line in lines:
        try:
            hlp = line.split('=')
            add_param(hlp[0].strip(), hlp[1].strip())
        except:
            pass


def create_url():
    #Exit with error if mustHave params not present
    url = "https://{0}/repos/{1}/{2}/issues".format(params.pop("server"), params.pop("repouser"), params.pop("reponame"))

    #Ignore if params not present
    #for (key, value) in params.items():
    par = '&'.join(["%s=%s" % (k, v) for k, v in params.items() if v])
    if par:
        url = url + '?' + par
    return url


def get_url(url):
    try:
        result = urllib2.urlopen(url).read()
    except:
        result = "Url error %s", url
    return result


def parse_url(response, *args):
    parsed_json = json.loads(response)  # list, every element is dictionary

    result = []
    for element in parsed_json:
        for key, value in element.items():
            if key in args:
                result.append("{0}: {1}".format(key, value))
            #result.append((["%s=%s" % (k, v) for k, v in params.items() if v]))
        result += '\n'
        return result


def out(output_list):
    for item in output_list:
        print item


get_params_from_file()
get_params_from_command_prompt()
url = create_url()
response = get_url(url)
output_list = parse_url(response, "state", "milestone", "title", "body", "labels")

pass
