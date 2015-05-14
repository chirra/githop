#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

config_file = ".githop"

#####################################
import urllib2
import sys
import json
import datetime

params = {}


def add_param(name, value):
    params[name] = value


def set_default_params():
    params["server"] = "api.github.com"
    params["since"] = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    params["state"] = "closed"


def print_usage_message():
    print "Usage: githop user repository [server=githubserver] [since=YYYY-MM-DDTHH:MM:SSZ] [state=open|closed|all] " \
              "[assignee=<username>] [labels=<label1>,<label2>,..,<labelN>] [milestone=<milestone>]"


def get_params_from_command_prompt():

        try:
            params["repouser"] = sys.argv[1]
            params["reponame"] = sys.argv[2]
            for arg in sys.argv[3:]:
                hlp = arg.split('=')
                add_param(hlp[0], hlp[1])
        except:
            pass


def check_params():
    for key in ("server", "repouser", "reponame"):
        if not params.get(key):
            print "Missing parameter: {0}".format(key)
            print_usage_message()
            sys.exit(1)


def get_params_from_file():
    try:
        f = open(config_file)
        lines = f.readlines()
        f.close()

        for line in lines:
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
        pass
    except:
        print "Url error {0}".format(url)
        sys.exit(1)
    return result


def parse_json(json_pack):
    parsed_json = json.loads(json_pack)  # list, every element is dictionary

    result = []

    for element in parsed_json:
        if element.get("id"): result.append("id: " + str(element["id"]))
        if element.get("title"): result.append("title: " + element["title"])
        if element.get("body"): result.append("body: " + element["body"])
        if element.get("updated_at"): result.append("updated_at: " + element["updated_at"])
        if element.get("state"): result.append("state: " + element["state"])
        if element.get("assignee"): result.append("assignee: " + element["assignee"]["login"])
        if element.get("milestone"): result.append("milestone: " + element["milestone"]["title"] + ' ' + element["milestone"]["description"])
        result.append('\n')

    return result


def print_list(my_list):
    for item in my_list:
        print item

#############################################

# Highest parameters priority overwrite lowest
set_default_params()    # In first, parameters dictionary fill default parameters
get_params_from_file()  # In second, from configuration file
get_params_from_command_prompt()    # In third, from command prompt, it's highest priority

check_params()
url = create_url()
response = get_url(url)
output_list = parse_json(response)
print_list(output_list)
