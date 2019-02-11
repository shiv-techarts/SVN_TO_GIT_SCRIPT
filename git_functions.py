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
from contextlib import contextmanager


def copyfile(src, dest):
    """
        Copy Files from src to destination
    :param src: source file
    :param dest: destination file
    :return: None
    """

    # Checks for OS
    if os.name == "nt":
        os.system(f"copy {src} {dest}")
    else:
        os.system(f"cp {src} {dest}")


@contextmanager
def mk_ch_dir(dir_name):
    """
        Creates the Directory if not exists, else change the directory
    :param dir_name: Directory Name
    :return: None
    """
    try:
        os.mkdir(dir_name)
        os.chdir(dir_name)
        yield
        os.chdir("..")
    except FileExistsError:
        os.chdir(dir_name)
        yield
        os.chdir("..")


def git_init_cmd(git_dir, comment, config):
    """
        Initializing the GIT repo based on Config details and Initial SVN Commit [ r1 ]
    :param git_dir: Git Repo Dir
    :param comment: Comment from 1st Commit Message from SVN Logs [ r1 ]
    :param config: config JSON - for Origin details
    :return: None
    """

    os.system(f'git init')

    # Creating README.md File for Information
    with open('README.md', 'w') as fh:
        fh.write(f"""
Initializing Git Repo {os.path.basename(git_dir)}
        """)

    # Adding Config details
    os.system(f'git add README.md')
    os.system(f"""git config --local user.name "{config['NAME']}" """)
    os.system(f"""git config --local user.email "{config['EMAIL']}" """)

    # Checking if GIT URL is present or not - Creates Local Repo if not Provided
    if config['GIT_URL']:
        os.system(f'git remote add origin {str(config["GIT_URL"])}')

    os.system(f'git commit -m "{comment}"')


class BranchStatus:
    """
        Checks if Branch is already been created or not
    """

    branches = ['master']
    curr_branch = ""

    def get_checkout(self, create_trigger):
        """
            Commands required for creating a branch and checkout
        :param create_trigger: True or False - for creating Branch or Not
        :return: None
        """
        if create_trigger:
            os.system(f'git branch {self.curr_branch}')
        os.system(f'git checkout {self.curr_branch}')

    def __init__(self, branch_name):
        """
            Checks if Branch is already present or not
        :param branch_name: Branch to be created
        """

        if branch_name not in self.branches:
            self.branches.append(branch_name)
            self.curr_branch = branch_name
            self.get_checkout(True)
        elif not self.curr_branch == branch_name:
            self.curr_branch = branch_name
            self.get_checkout(False)


def git_add_cmd(from_svn, to_git, log_data, config):
    """
        Adds Files from SVN Repo to GIT repo and creates commits and PUSH
    :param from_svn: SVN Repo Path
    :param to_git: GIT Repo Path
    :param log_data: Dict of SVN Logs
    :param config: Config Details
    :return:
    """

    # Gets the SVN Directory Name
    from_svn = os.path.join(from_svn, os.path.basename(to_git))

    branch_to_push = ""

    # Checking for the Branches
    if log_data['Path'] == 'branches':

        if log_data['Branch_Name'] != "":
            branch_name = str(log_data['Branch_Name'])
            BranchStatus(branch_name)

        for files in log_data['Files_Commit']:
            file = str(from_svn + str(files[1]))
            copyfile(file, to_git)

        os.system(f'git add .')
        os.system(f'git commit -m "{str(log_data["Comment"])}"')
        branch_to_push = branch_name

    # Checking for the trunk
    if log_data['Path'] == 'trunk':

        BranchStatus("master")

        for files in log_data['Files_Commit']:
            file = str(from_svn + str(files[1]))
            copyfile(file, to_git)

        os.system(f'git add .')
        os.system(f'git commit -m "{str(log_data["Comment"])}"')

        branch_to_push = "master"

    # Checking for the tags
    if log_data['Path'] == 'tags':

        if log_data['Branch_Name'] != "":
            branch_name = str(log_data['Branch_Name'])
            BranchStatus(branch_name)
            rev = str(log_data['Revision']).split("|")[0].strip()
            os.system(f'git tag -a v{rev.upper()} -m "{str(log_data["Comment"])}"')

        branch_to_push = branch_name

    # Push Commands for GIT repo - If User and password provided else changes are saved locally
    if log_data['Branch_Name'] != "" and config['GIT_URL']:
        git_url = str(config['GIT_URL'])
        git_username = str(config['GIT_USERNAME'])
        git_password = str(config['GIT_PASSWORD'])

        git_url = git_url.replace("https://", f"https://{git_username}:{git_password}@")

        os.system(f'git push -u {git_url}')

    elif log_data['Branch_Name'] != "":
        os.system(f'git push -u origin {branch_to_push}')

    elif branch_to_push == "master":
        os.system(f'git push -u origin {branch_to_push}')


def git_dir(from_svn, to_git, svn_log_dict, config):
    """
        Creates, Initializes and Adds files to GIT Repo based on log Dictionary Provided
    :param from_svn: SVN Repo Path
    :param to_git: GIT Repo Path
    :param svn_log_dict: SVN Log Dict
    :param config: Config JSON File
    :return: None
    """

    with mk_ch_dir("GIT_TEMP_DIR"):
        with mk_ch_dir(to_git):

            try:
                for key in svn_log_dict.keys():
                    if key == "r1":
                        git_init_cmd(git_dir=os.getcwd(), comment=svn_log_dict[key]['Comment'], config=config)
                    else:
                        git_add_cmd(from_svn=from_svn, to_git=os.getcwd(), log_data=svn_log_dict[key], config=config)
            except KeyError:
                print(f"ERROR: No Key Found")
            except AttributeError:
                print(f"ERROR: None Key Found")
