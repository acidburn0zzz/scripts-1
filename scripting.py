import os
import platform
import subprocess
import shutil

def check4compatiblity():
	if platform.system() != 'Linux' and platform.system() != 'Darwin':
		   raise Exception('You are using ' + getOSName() + 'OS, which is not supported by the scripting package.')
	pass

def linux():
	check4compatiblity()
	return 'Linux'

def os_x():
	check4compatiblity()
	return 'Darwin'

def getOSName():
	check4compatiblity()
	return platform.system()

def getFileDirectory(path):
	check4compatiblity()
	return os.path.dirname(os.path.realpath(path))

def touch(path):
	check4compatiblity()
	open(path, 'a').close()
	pass

def executeShellCommand(cmd):
	check4compatiblity()
	subprocess.call(cmd)
	pass

def getHomeDirectory():
	check4compatiblity()
	return os.path.expanduser('~') + '/'

def createSymbolicLink(src, dest):
	check4compatiblity()
	executeShellCommand(['ln', '-s', src, dest])
	pass

def ensureDirectory(directory):
	check4compatiblity()
	if not os.path.exists(directory):
		os.makedirs(directory)
	pass

