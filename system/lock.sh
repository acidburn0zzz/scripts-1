#!/bin/bash

set -o errexit -o noclobber -o nounset

mydir=$(readlink -f -- "$0")
mydir=${mydir%/*}

hue=(-level "0%,100%,1.0")
effect=(-blur 0x10)

font=$(convert -list font | awk "{ a[NR] = \$2 } /family: $(fc-match sans -f "%{family}\n")/ { print a[NR-1]; exit }")
image=$(mktemp).png
shot=(import -window root)
desktop=""
i3lock_cmd=(i3lock -i "$image")
shot_custom=false

help() {
	echo "i3lock-awesome:
	-h/--help               -- show this text.
	-d/--desktop            -- show desktop before lock(minimize all windows).
	-g/--greyscale          -- make background image greyscale(color by default).
	-p/--pixelate           -- make background pixelated(blur by default).
	-f <font>/--font <font> -- select custom font.
	-t <text>/--text <text> -- set custom text.
	-l/--list               -- list avalible fonts.
	"
}

set -o pipefail
trap 'rm -f "$image"' EXIT
temp="$(getopt -o :hdnpglt:f: -l desktop,help,listfonts,nofork,pixelate,greyscale,text:,font: --name "$0" -- "$@")"
eval set -- "$temp"

text="Type password to unlock"
case "${LANG:-}" in
	en_* ) text="Type password to unlock" ;;
	ru_* ) text="Введите пароль"          ;;
	*    ) text="Type password to unlock" ;;
esac

while true ; do
	case "$1" in
		-h|--help)
			printf "Usage: %s [options]\n" "${0##*/}"
			help
			exit 1
			;;

		-d|--desktop) 
			desktop=$(command -V wmctrl) 
			shift 
			;;

		-g|--greyscale) 
			hue=($hue -set colorspace Gray -separate -average)
			shift 
			;;

		-p|--pixelate) 
			effect=(-scale 10% -scale 1000%)
			shift 
			;;

		-f|--font)
			case "$2" in
				"") 
					shift 2 
					;;

				*)  
					font=$2 
					shift 2 
					;;
			esac 
			;;

		-t|--text) 
			text=$2
			shift 2 
			;;

		-l|--listfonts)
			convert -list font | awk -F: '/Font: / { print $2 }' | sort -du | command -- ${PAGER:-less}
			exit 0 
			;;

		--)
			shift
			shot_custom=true
			break
			;;

		*)
			printf "Invalid option '%s'\n" "$1"
			help
			exit 1
			;;

		esac
	done

	if "$shot_custom" && [[ $# -gt 0 ]]; then
		shot=("$@");
	fi

	command -- "${shot[@]}" "$image"

	value="60"

	color=$(convert "$image" -gravity center -crop 100x100+0+0 +repage -colorspace hsb \
		-resize 1x1 txt:- | awk -F '[%$]' 'NR==2{gsub(",",""); printf "%.0f\n", $(NF-1)}');

	if [[ $color -gt $value ]]; then
		bw="black"
		icon="$mydir/icons/lockdark.png"
		param=("--textcolor=00000000" "--insidecolor=0000001c" "--ringcolor=0000003e" \
			"--linecolor=00000000" "--keyhlcolor=ffffff80" "--ringvercolor=ffffff00" \
			"--separatorcolor=22222260" "--insidevercolor=ffffff1c" \
			"--ringwrongcolor=ffffff55" "--insidewrongcolor=ffffff1c")
	else
		bw="white"
		icon="$mydir/icons/lock.png"
		param=("--textcolor=ffffff00" "--insidecolor=ffffff1c" "--ringcolor=ffffff3e" \
			"--linecolor=ffffff00" "--keyhlcolor=00000080" "--ringvercolor=00000000" \
			"--separatorcolor=22222260" "--insidevercolor=0000001c" \
			"--ringwrongcolor=00000055" "--insidewrongcolor=0000001c")
	fi

	convert "$image" "${hue[@]}" "${effect[@]}" -font "$font" -pointsize 26 -fill "$bw" -gravity center \
		-annotate +0+160 "$text" "$icon" -gravity center -composite "$image"

	${desktop} ${desktop:+-k on}

	if ! "${i3lock_cmd[@]}" "${param[@]}" >/dev/null 2>&1; then
		"${i3lock_cmd[@]}"
	fi

	${desktop} ${desktop:+-k off}
