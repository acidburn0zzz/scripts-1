import os
import platform
import subprocess
import shutil

installation_directory = '/etc/bezzubtsev-shell-scripts/'
installation_flag = installation_directory + 'installed'

def touch(path):
    open(path, 'a').close()
    pass

def getScriptsDirectory():
    return os.path.dirname(os.path.realpath(__file__))

def executeShellCommand(cmd):
    subprocess.call(cmd)
    pass

def getHomeDirectory():
    return os.path.expanduser('~') + '/'

def createSymbolicLink(src, dest):
    executeShellCommand(['ln', '-s', src, dest])
    pass

def ensureDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
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

def needsInstallation():
    return not os.path.exists(installation_flag)

def copyBashProfile():
    shutil.copyfile(getBashConfigurationFile(), installation_directory + 'shell-setup')
    pass

def processInstallation():
    if needsInstallation():
        print('Ensuring ' + installation_directory + 'directory...')
        ensureDirectory(installation_directory)
 
        print('Copying bash profile...')
        copyBashProfile()

        print('Marking installation flags...')
        touch(installation_flag)

        print('Linking ' + getHomeDirectory() + ' to ' + getScriptsDirectory() + '...')
        createSymbolicLink(getScriptsDirectory(), getHomeDirectory() + 'bin')

        print('Writing path data...')
        writePathData()
    pass

processInstallation()
