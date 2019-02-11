# SVN_TO_GIT_MIGRATION

*Description*

 SVN2GIT Migration Script is a python script that checks the logs of SVN Repository, Parse it and Create a JSON Dictionary from it.
 Every Key:Value Pair consist of following details
 
     "Files_Commit": [
      [
        "A", # A - Added | M - Modified
        "branches/0002/file.sh" # files those are modified or created
      ],
      [
        "M", # A - Added | M - Modified
        "branches/0002/file2.sh" # files those are modified or created
      ]
    ],
    "Revision": "r8 | USERNAME | 2018-12-27 18:54:59 +0530 (Thu, 27 Dec 2018) | 1 line", # Revision Information
    "Comment": "[0002] Adding files.sh and file2.sh to the SVN repository", # Comment for Each Commit Made
    "Path": "branches", # Check if Branch / Trunk / Tag
    "Branch_Name": "0002" # Branch Name
 
 Above details are used for creating individual commits at a time into a new GIT repository 
 [ README.md is added with GIT Initialization ]
 
 SNV Checkout is taken in a temporary dir and a GIT Repository is initailized in a parallel repository.
 SVN Files are copied one by one to GIT Repository and Added with the commit that has done in SVN Repository.
 
 Once individual commit is done, directory is PUSHED to GIT Origin if GIT_URL is provided else the repo is created locally.
 
*Requirements*

[Windows]

1. git.exe
2. svn.exe

Git-Bash

https://git-scm.com/downloads

Tortoise SVN

https://tortoisesvn.net/downloads.html

Add both the tools in the path

[Linux]

1. git
2. svn

sudo apt-get install git
sudo apt-get install svn

*Usage*

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
              "GIT_URL": "",
              "GIT_USERNAME": "",
              "GIT_PASSWORD": ""
        }
  
    NAME          : Username for GIT Configuration
    EMAIL         : Email ID for GIT Configuration
    SVN_URL       : SVN Url Which is to be converted to a GIT repository
    SVN_USERNAME  : If SVN requires Username and Password
    SVN_PASSWORD  : If SVN requires Username and Password
    GIT_URL       : GIT Url to be set as Origin
    GIT_USERNAME  : If GIT requires Username and Password
    GIT_PASSWORD  : If GIT requires Username and Password
    

# Shiv Pratap Singh
https://www.linkedin.com/in/shiv-pratap-singh/
