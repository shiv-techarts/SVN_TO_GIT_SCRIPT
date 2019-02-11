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

import os
import re
from git_functions import git_dir, mk_ch_dir


def svn2dict(data_str=None):
    """
        Parses the SVN logs and generates the JSON Object Based on that
    :param data_str: logs to be parsed
    :return: JSON Object of Details required for GIT Repo
    """

    lines = list()

    lines_w_nl = str(data_str).split("\n")

    for line in lines_w_nl:
        lines.append(str(line).strip("\n"))

    del lines_w_nl

    dashes = re.compile(r'^-+$')
    key = 0
    dict_of_log = dict()

    for line in lines:
        if not dashes.match(line):
            dict_of_log[str(key)].append(line)
        else:
            key += 1
            dict_of_log[str(key)] = []

    del dict_of_log[str(list(dict_of_log.keys())[-1])]

    parsed_log = {}

    for key in reversed(list(dict_of_log.keys())):

        data = dict_of_log[str(key)]

        spaces_in_file_commit = re.compile(r'^\s+')
        revision_number = re.compile(r'^r.*$')
        blank_line = re.compile(r'^$')

        blank_line_flag = False

        per_rev_dict = dict()
        per_rev_dict['Files_Commit'] = []

        path = ""
        branch_name = ""

        for details in data:
            if revision_number.match(details):
                per_rev_dict['Revision'] = details
                revision = str(details).split("|")[0].strip(" ") if str(details).split("|")[0].strip(" ") else "r"

            if blank_line.match(details):
                blank_line_flag = True
            elif blank_line_flag:
                per_rev_dict['Comment'] = details

            if spaces_in_file_commit.match(details) and not blank_line_flag:
                added_modified = str(details).strip(" ").split(" ")[0] if str(details).strip(" ").split(" ")[0] else ""
                files = str(details).strip(" ").split(" ")[1] if str(details).strip(" ").split(" ")[1] else ""

                if files.find("/trunk") != -1:
                    path = "trunk"
                if files.find("/branches") != -1:
                    path = "branches"
                    try:
                        branch_name = files.replace("/branches/", "").split("/")[0]
                    except Exception as err:
                        print(str(err))
                        branch_name = ""

                if files.find("/tags") != -1:
                    path = "tags"
                    try:
                        branch_name = files.replace("/tags/", "").split("/")[0]
                    except Exception as err:
                        print(str(err))
                        branch_name = ""

                if os.name == "nt":
                    files = files.replace('/', os.sep)

                per_rev_dict['Files_Commit'].append(tuple([added_modified, files]))

        per_rev_dict['Path'] = path
        per_rev_dict['Branch_Name'] = branch_name
        try:
            parsed_log['r1']['Path'] = ""
        except KeyError:
            pass
        parsed_log[revision] = per_rev_dict

    # Debug Line
    # print(parsed_log)

    return parsed_log


def svn_log2json(config):
    """
        Takes the config JSON file and reads the SVN Logs and Create a JSON Dictionary sorted on Revision Number
    :param config: config JSON
    :return: JSON Dictionary Contains details of revision and Files to be commited
    """

    # Get SVN URL
    try:
        svn_url = config['SVN_URL']
    except KeyError:
        print("ERROR: SVN URL not Found")
        exit(-1)

    # Creating SVN Commands to read the logs
    svn_log_command = "svn log -v"
    svn_command = f"{svn_log_command} {svn_url}"
    data_str = os.popen(f"{svn_command}").read()

    # Checking Error for Logs
    if not data_str:
        print(f"Error: While getting logs for the SVN Url")
        exit(-1)

    try:
        # Parsing the logs
        log_dict = svn2dict(data_str)
    except FileNotFoundError as err1:
        print(f"Error: While getting logs for the SVN Url : {str(err1)}")
        exit(-1)
    except Exception as err2:
        print(f"Error: While getting logs for the SVN Url : {str(err2)}")
        exit(-1)

    return log_dict


def svn_checkout(svn_url, config):
    """
        Take SVN Checkout for Copying the files to a GIT Repo
    :param svn_url: SVN Url
    :param config: Config JSON Object
    :return: Directory SVN Checkout is taken
    """

    # Context Manager defined in git_functions
    with mk_ch_dir("SVN_TEMP_DIR"):
        # Checking for Username or Password if Provided
        if config['SVN_USERNAME'] and config['SVN_PASSWORD']:
            svn_checkout_cmd = f"svn checkout --username " \
                f"{str(config['SVN_USERNAME'])} --password {str(config['SVN_PASSWORD'])}"
        else:
            svn_checkout_cmd = "svn checkout"
        svn_command = f"{svn_checkout_cmd} {svn_url}"
        os.popen(svn_command)
        current_dir = os.getcwd()

    return current_dir


def json_to_git(config, log_dict):
    """
        Creates a Git Repo with config and details Provided by JSON Object
    :param config: Config Details for Initializing Git Repo
    :param log_dict: JSON Objects containing details for git Repo
    :return: None
    """

    svn_url = config['SVN_URL']

    with mk_ch_dir("TEMP_DIR"):
        dir_name = svn_checkout(svn_url, config)
        svn_dir = os.path.basename(svn_url)
        git_dir(from_svn=dir_name, to_git=svn_dir, svn_log_dict=log_dict, config=config)
