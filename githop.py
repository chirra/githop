# -*- coding: utf-8 -*-

import urllib2
import sys
import json
import datetime




config_file = ".githop"

params = {}
#params = {"server": "api.github.com"}


def add_param(name, value):
    params[name] = value


def set_default_params():
    params["server"] = "api.github.com"
    params["since"] = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    params["state"] = "close"


def print_usage_message():
    print "Usage: githop user repository [server=githubserver] [since=YYYY-MM-DDTHH:MM:SSZ] [state=open|close] " \
              "[assignee=<username>] [labels=<label1>,<label2>,..,<labelN>] [milestone=<milestone>]"


def get_params_from_command_prompt():
    for arg in sys.argv[1:]:
        try:
            hlp = arg.split('=')
            add_param(hlp[0], hlp[1])
        except:
            pass

    if not params["server"] or not params["repouser"] or not params["reponame"]:
        print_usage_message()
        sys.exit(1)


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
    # Exit with error if mustHave params not present

    try:
        url = "https://{0}/repos/{1}/{2}/issues".format(params.pop("server"), params.pop("repouser"), params.pop("reponame"))
    except:
        print_usage_message()
        sys.exit(1)

    # Ignore if optional params not present
    pars = '&'.join(["%s=%s" % (k, v) for k, v in params.items() if v])
    if pars:
        url = url + '?' + pars
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
        result.append("id: " + str(element["id"]))
        result.append("title: " + element["title"])
        result.append("body: " + element["body"])
        result.append("updated_at: " + element["updated_at"])
        result.append("state: " + element["state"])
        result.append("assignee: " + element["assignee"]["login"])
        result.append("milestone: " + element["milestone"]["title"] + ' ' + element["milestone"]["description"])
        result.append('\n')
    return result


def out(output_list):
    for item in output_list:
        print item


get_params_from_file()
get_params_from_command_prompt()
url = create_url()
response = get_url(url)
output_list = parse_url(response)
out(output_list)
