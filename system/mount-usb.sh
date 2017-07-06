#!/bin/bash

usage() {
	echo "Usage: $0 command device_file"
	echo "Where command is 'add' or 'remove'"
	echo "'add' mounts device_file"
	echo "'remove' unmounts device_file"

	exit 1
}

if [[ $# -ne 2 ]]; then
	echo "Bad arguments"
	usage
fi

ACTION=$1
DEVICE=$2

DEVICE_FILE="/dev/${DEVICE}"

MOUNT_POINT=$(/bin/mount | /bin/grep ${DEVICE_FILE} | /usr/bin/awk '{ print $3 }')

mount_device() {
	if [[ -n ${MOUNT_POINT} ]]; then
		echo "#### error: ${DEVICE} is already mounted at ${MOUNT_POINT}. #####"
		exit 1
	fi

	eval $(/sbin/blkid -o udev ${DEVICE})

	LABEL=${ID_FS_LABEL}

	if /bin/grep -q " /media/${LABEL} " /etc/mtab; then
		LABEL+="-${DEVBASE}"
	fi

	MOUNT_POINT="/media/${LABEL}"

	echo "#### mount point: ${MOUNT_POINT} ####"

	/bin/mkdir -p ${MOUNT_POINT}

	OPTS="rw,relatime"

	if [[ ${ID_FS_TYPE} == "vfat" ]]; then
		OPTS+=",users,gid=100,umask=000,shortname=mixed,utf8=1,flush"
	fi

	if ! /bin/mount -o ${OPTS} ${DEVICE} ${MOUNT_POINT}; then
		echo "#### error: failed to mount ${DEVICE} (status = $?)"
		/bin/rmdir ${MOUNT_POINT}
		exit 1
	fi

	echo "#### success: mounted ${DEVICE} at ${MOUNT_POINT} ####"
}

unmount_device() {
	if [[ -z ${MOUNT_POINT} ]]; then
		echo "#### error: ${DEVICE} is not mounted ####"
	else
		/bin/umount -l ${DEVICE}
		echo "#### success: unmounted ${DEVICE} ####"
	fi

	for f in /media/* ; do
		if [[ -n $(/usr/bin/find "$f" -maxdepth 0 -type d -empty) ]]; then
			if ! /bin/grep -q " $f " /etc/mtab; then
				echo "#### removing mount point $f ####"
				/bin/rmdir "$f"
			fi
		fi
	done
}
