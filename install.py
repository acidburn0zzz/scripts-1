import os
import shutil
import scripting

installation_directory = '/etc/bezzubtsev-shell-scripts/'
installation_flag = installation_directory + 'installed'
bash_profile_copy = installation_directory + 'shell-script'

step = 0

def getScriptsDirectory():
	return scripting.getFileDirectory(__file__)

def getBashConfigurationFile():
	scripting.check4compatiblity()
	if scripting.getOSName() == scripting.linux():
		return scripting.getHomeDirectory() + '.bashrc'
	elif scripting.getOSName() == scripting.os_x():
		return scripting.getHomeDirectory() + '.bash_profile'
	pass

def writePathData():
	profile = open(getBashConfigurationFile(), 'a')
	profile.write('\n# Inserted automatically by scripts installer\nexport PATH=' + scripting.getHomeDirectory() + 'bin:$PATH\n')
	profile.close()
	pass

def needsInstallation():
	return not os.path.exists(installation_flag)

def copyBashProfile():
	shutil.copyfile(getBashConfigurationFile(), bash_profile_copy)
	pass


def undoStep(identifier):
	undo = {
		0: shutil.rmtree(installation_directory),
		1: shutil.move(bash_profile_copy, getBashConfigurationFile()),
		2: os.remove(installation_flag),
		3: os.remove(scripting.getHomeDirectory() + 'bin'),
		4: {}
	}

	if identifier < 0 or identifier > 4:
		return
	else:
		undo[identifier]()
	pass

def undoChanges():
	global step

	for i in range(step, 0):	
		undoStep(i)
	pass

def processInstallation():
	global step

	try:
		if needsInstallation():
			print('Ensuring ' + installation_directory + 'directory...')
			scripting.ensureDirectory(installation_directory)
 			step += 1

			print('Copying bash profile...')
			copyBashProfile()
			step += 1

			print('Marking installation flags...')
			scripting.touch(installation_flag)
			step += 1

			print('Linking ' + getScriptsDirectory() + ' to ' + scripting.getHomeDirectory() + 'bin/ ...')
			scripting.createSymbolicLink(getScriptsDirectory(), scripting.getHomeDirectory() + 'bin')
			step += 1

			print('Writing path data...')
			writePathData()
			step += 1
		else:
			print('Installation is not needed, skipping...')
	except Exception as data:
		print('An exception was caught due installation: ', data)
		undoChanges()
	pass

processInstallation()
