"""
##############################################################
##
## Name         : Shiv Pratap Singh
## Description  : SVN TO GIT Migration Script
## Requirements : git-bash.exe for windows and git for linux
##                svn for Windows and svn for linux
##                config JSON
##
##############################################################
"""

# Libraries Required

import sys
import json
from svn2git_functions import svn_log2json, json_to_git


if __name__ == "__main__":
    """
        python3 svn2git_main.py --svn_url="svn://url"
    :return:
    """

    usage = """
    python3 svn2git_main.py --config=config.json

    [Parameters]

        --config = JSON File with configuration
        
        Must Have Following Key Pairs:
        
        {
              "NAME": "",
              "EMAIL": "",
              "SVN_URL": "",
              "SVN_USERNAME": "",
              "SVN_PASSWORD": "",
              "GIT_USERNAME": "",
              "GIT_PASSWORD": ""
        }

        """

    # Creating Argument Dictionary for Config Details and Usage Details
    arg_dict = dict()
    arg_dict['Usage'] = usage

    try:
        arg_val = str(sys.argv[1])
        if arg_val.find("--config") != -1:
            arg_dict['--config'] = str(arg_val.split("=")[1]).strip('"')
        else:
            print(arg_dict['Usage'])
            exit(-1)
    except IndexError:
        print(arg_dict['Usage'])
        exit(-1)

    # Reading the config JSON File for Details
    with open(str(arg_dict['--config'])) as fh:
        config_data = json.load(fh)

    # Get the JSON dictionary for SVN Logs
    result = svn_log2json(config_data)

    # Debug Code
    # with open('svn_logs.json', 'w') as fh:
    #     json.dump(result, fh)

    # Create or Initialize JSON Dictionary to GIT Repo
    json_to_git(config=config_data, log_dict=result)
