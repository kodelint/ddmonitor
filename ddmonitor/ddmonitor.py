# -*- coding: utf-8 -*-

import sys
import argparse
import os
import json
import configparser
from datadog import initialize, api
from os.path import expanduser

config = configparser.ConfigParser()
config.read(expanduser("~") + "/" + ".ddmon.ini")


options = {
    'api_key': os.environ.get('dd_api_key') or config.get("default", "dd_api_key"),
    'app_key': os.environ.get('dd_app_key') or config.get("default", "dd_app_key")
}


def make_dataset(dataset):
    """
    This function is handy way to extract the required informatipn from full JSON dump from DataDog API.

    :param dataset: Function take "dataset" as parameter which is total json data from DataDog API call
    :return: resultset which is custom dictionary. i.e.
    {
     { "Name": XXXX,
       "Query": XXXX,
       "Creator": XXXX,
       "Status": XXXX,
       "Tags": XXXX
     }
    }
    """
    resultset = []
    result = {}
    for data in dataset:
        result["Name"] = data["name"]
        result["Query"] = data["query"]
        result["Creator"] = data["creator"]["name"]
        result["Status"] = data["overall_state"]
        result["Tags"] = data["tags"]
        resultset.append(result.copy())

    return resultset


def main():
    """
        usage: ddmonitor.py [-h] [-a] [-s SEARCH_BY_NAME] [-t SEARCH_BY_TAG]
                            [-g SEARCH_BY_GROUP_STATES] [-m SEARCH_BY_MONITOR_TAGS]

        DataDog CLI for Search Team Usages

        optional arguments:
          -h, --help            show this help message and exit

          -a, --all             Gets all monitors (default: False)
          -s SEARCH_BY_NAME, --search-by-name SEARCH_BY_NAME
                                Lookup monitors using "name" (default: None)
          -g SEARCH_BY_STATES, --search-by-group-states SEARCH_BY_GROUP_STATES
                                Lookup monitors using "group_states" (default: None)
          -m SEARCH_BY_TAGS, --search-by-tags SEARCH_BY_MONITOR_TAGS
                                Lookup monitors using "monitor_tags", These are
                                custome tags (default: None)
    """
    initialize(**options)  # DataDog function to initialize the connection using the api and app keys
    monitors = api.Monitor.get_all() # DataDog Monitor API to select all the monitors
    parser = argparse.ArgumentParser(description='DataDog CLI', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ddparser = parser.add_argument_group()
    ddparser.add_argument('-a', '--all', action='store_true', help='Gets all monitors')
    ddparser.add_argument('-n', '--search-by-name', action='store', help='Lookup monitors using "name"')
    ddparser.add_argument('-s', '--search-by-status', action='store', help='Lookup monitors using "group_states"')
    ddparser.add_argument('-t', '--search-by-tags', action='store', help='Lookup monitors using "monitor_tags", These are custome tags')
    ddargs = parser.parse_args()

    if ddargs.search_by_name:
        name = ddargs.search_by_name
        monitors = api.Monitor.get_all(name=name)
        print(json.dumps(make_dataset(monitors), indent=2, sort_keys=True))
    elif ddargs.search_by_status:
        group_states = ddargs.search_by_status
        monitors = api.Monitor.get_all(group_states=group_states)
        print(json.dumps(make_dataset(monitors), indent=2, sort_keys=True))
    elif ddargs.search_by_tags:
        monitor_tags = ddargs.search_by_tags
        monitors = api.Monitor.get_all(monitor_tags=monitor_tags)
        print(json.dumps(make_dataset(monitors), indent=2, sort_keys=True))
    elif ddargs.all:
        print(json.dumps(make_dataset(monitors), indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
