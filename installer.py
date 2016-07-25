import os
import shutil
import scripting

installation_directory = '/etc/bezzubtsev-shell-scripts/'
installation_flag = installation_directory + 'installed'
bash_profile_copy = installation_directory + 'shell-script'

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

def copyBashProfile():
	shutil.copyfile(getBashConfigurationFile(), bash_profile_copy)
	pass


def undoEnsuring():
	print('Undoing ensure...')
	shutil.rmtree(installation_directory)
	pass

def recoverBashProfile():
	print('Recovering bash profile...')
	shutil.move(bash_profile_copy, getBashConfigurationFile())
	pass

def clearInstallationFlag():
	print('Removing installation flags')
	os.remove(installation_flag)
	pass

def undoSymlink():
	print('Deleting symlinks')
	os.remove(scripting.getHomeDirectory() + 'bin')
	pass

def undoPathData():
	print('Removing path records')
	pass

def undoStep(identifier):
	undo = [
		undoEnsuring,
		recoverBashProfile,
		clearInstallationFlag,
		undoSymlink,
		undoPathData
	]

	if identifier >= 0 and identifier <= 4:
		undo[identifier]()
	pass

def undoChanges(last_step_id):
	for i in range(last_step_id, 0, -1):	
		undoStep(i)
	pass

