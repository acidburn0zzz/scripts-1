#!/usr/bin/python

import os
import platform
import shutil

installation_directory = '/etc/bezzubtsev-shell-scripts/'
installation_flag = installation_directory + 'installed'

def getHomeDirectory():
    return os.path.expanduser('~') + '/'

def getBashConfigurationFile():
    if platform.system() == 'Linux':
        return getHomeDirectory() + '.bashrc'
    else:
        return getHomeDirectory() + '.bash_profile'

def restoreBashProfile():
    shutil.copyfile(installation_directory + 'shell-setup', getBashConfigurationFile())
    pass

def cleanupSetup():
    shutil.rmtree(installation_directory)
    os.remove(getHomeDirectory() + 'bin')
    pass

def needsDeinstallation():
    return os.path.exists(installation_flag)

def processDeinstallation():
    if needsDeinstallation():
        print('Restoring bash profile...')
        restoreBashProfile()

        print('Cleaning setup...')
        cleanupSetup()
    pass

processDeinstallation()
