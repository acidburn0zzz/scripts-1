import os
import installer
import scripting

def needsInstallation():
	return not os.path.exists(installer.installation_flag)

def processInstallation():
	step = 0
	try:
		if needsInstallation():
			print('Ensuring ' + installer.installation_directory + 'directory...')
			scripting.ensureDirectory(installer.installation_directory)
 			step += 1

			print('Copying bash profile...')
			installer.copyBashProfile()
			step += 1

			print('Marking installation flags...')
			scripting.touch(installer.installation_flag)
			step += 1

			print('Linking ' + installer.getScriptsDirectory() + ' to ' + scripting.getHomeDirectory() + 'bin/ ...')
			scripting.createSymbolicLink(installer.getScriptsDirectory(), scripting.getHomeDirectory() + 'bin')
			step += 1

			print('Writing path data...')
			installer.writePathData()
			step += 1
		else:
			print('Installation is not needed, skipping...')
	except Exception as data:
		print('An exception was caught due installation: ', data)
		installer.undoChanges(step)
	pass

processInstallation()
