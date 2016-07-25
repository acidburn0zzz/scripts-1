import os
import installer

def needsDeinstallation():
    return os.path.exists(installer.installation_flag)

def processDeinstallation():
    if needsDeinstallation():
        print('Cleaning setup...')
	installer.undoChanges(4)
    pass

processDeinstallation()
