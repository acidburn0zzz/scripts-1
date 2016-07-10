#!/usr/bin/python

import os
import platform
import subprocess

def getScriptsDirectory():
    return os.path.dirname(__file__)

def executeShellCommand(cmd):
    subprocess.call(cmd)
    pass

def getHomeDirectory():
    return os.path.expanduser('~') + '/';

def createSymbolicLink(src, dest):
    executeShellCommand(['ln', '-s', src, dest])
    pass

def getBashConfigurationFile():
    if platform.system() == 'Linux':
        return getHomeDirectory() + '.bashrc'
    else:
        return getHomeDirectory() + '.bash_profile'

def writePathData():
    profile = open(getBashConfigurationFile(), 'a')
    profile.write('\n# Inserted automatically by scripts installer\nexport PATH=' + getHomeDirectory() + 'bin:$PATH\n')
    profile.close()
    pass

def main():
    createSymbolicLink(getScriptsDirectory(), getHomeDirectory() + 'bin')
    writePathData()

main()
