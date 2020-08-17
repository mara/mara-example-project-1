#!/bin/bash

export PALETTE_RESET='\e[0m'
export PALETTE_INFO='\e[33m' # brown color
export PALETTE_ERROR='\e[31m' # red color

trim()
{
    local trimmed="$1"

    # Strip leading space.
    trimmed="${trimmed## }"
    # Strip trailing space.
    trimmed="${trimmed%% }"

    echo "$trimmed"
}

if [[ $1 == 'install' ]]; then

	## install package

	if [[ $2 == '-r' ]] || [[ $2 == '--requirement' ]] || [[ $2 == '--requirement='* ]]; then

		## install from requirements file

		if [[ $2 == '--requirement='* ]]; then
			REQUIREMENTS_FILE="${2:14}"
		elif [[ $3 == '' ]] || [[ -f "$3" ]]; then
			REQUIREMENTS_FILE="$3"
			shift
		else
			echo -e "${PALETTE_ERROR}requirements file not given${PALETTE_RESET}"
			exit 1
		fi

		PIP_INSTALL_SUB_ARGS=''
		while [ -n "$3" ]
		do
			PIP_INSTALL_SUB_ARGS="$PIP_INSTALL_SUB_ARGS $3"
			shift
		done

		cat $REQUIREMENTS_FILE | sed "s/\r$//" | while IFS= read -r line
		do
			# trim whitespaces
			line=$(trim "$line")

			if [[ $line != '' ]] && [[ $line != '#'* ]] ; then
				if [[ $line = '-e '* ]]; then
					PIP_INSTALL_PRE_ARGS='-e '
					PACKAGE_NAME_CALL="${line:3}"
				else
					PIP_INSTALL_PRE_ARGS=''
					PACKAGE_NAME_CALL="$line"
				fi

				# get package name
				if [[ $PACKAGE_NAME_CALL = 'git+'* ]]; then
					PACKAGE_NAME=$(cut -d '=' -f2 <<< "$PACKAGE_NAME_CALL")

					if [[ $PACKAGE_NAME == '' ]]; then
						echo -e "${PALETTE_ERROR}When installing a package with git+, you have to add #egg= to specify the package name${PALETTE_RESET}"
						exit 1
					fi

				else
					if [[ $PACKAGE_NAME_CALL = *'#'* ]]; then
						# cut away comment after package name
						PACKAGE_NAME_CALL=$(echo "$PACKAGE_NAME_CALL" | cut -f1 -d"#")
					fi

					if [[ $PACKAGE_NAME_CALL = *';'* ]]; then
						echo -e "${PALETTE_ERROR}Environment markers are not supported in the package name${PALETTE_RESET}"
						exit 1
					fi
					if [[ $PACKAGE_NAME_CALL = *'['* ]]; then
						echo -e "${PALETTE_ERROR}Extras definitions not supported in the package name${PALETTE_RESET}"
						exit 1
					fi

					# remove version info from package name
					PACKAGE_NAME="$PACKAGE_NAME_CALL"
					PACKAGE_NAME=$(cut -d '~' -f1 <<< "$PACKAGE_NAME")
					PACKAGE_NAME=$(cut -d '!' -f1 <<< "$PACKAGE_NAME")
					PACKAGE_NAME=$(cut -d '>' -f1 <<< "$PACKAGE_NAME")
					PACKAGE_NAME=$(cut -d '<' -f1 <<< "$PACKAGE_NAME")
					PACKAGE_NAME=$(cut -d '=' -f1 <<< "$PACKAGE_NAME")
				fi

				# run install
				echo -e "${PALETTE_INFO}singer-cli.sh install $PIP_INSTALL_PRE_ARGS\"$PACKAGE_NAME_CALL\"$PIP_INSTALL_SUB_ARGS${PALETTE_RESET}"
				bash ./$0 install $PIP_INSTALL_PRE_ARGS"$PACKAGE_NAME_CALL"$PIP_INSTALL_SUB_ARGS
				RC=$?; [ $RC -ne 0 ] && exit $RC
			fi
		done
	else

		## install from package name or git+ syntax

		# the additional parameters to be used with pip
		PIP_INSTALL_PRE_ARGS='' # pipe args before the package name
		PIP_INSTALL_SUB_ARGS='' # pipe args after the package name
		
		# the package name call (including version information, git etc.)
		PACKAGE_NAME_CALL=''

		# only the package name excl. version information, git etc.
		PACKAGE_NAME=''

		while [ -n "$2" ]
		do
			if [[ $2 = '-'* ]]; then
				# is a parameter
				if [[ -n "$PACKAGE_NAME_CALL" ]]; then
					PIP_INSTALL_SUB_ARGS="$PIP_INSTALL_SUB_ARGS $2"
				else
					PIP_INSTALL_PRE_ARGS="$PIP_INSTALL_PRE_ARGS $2"
				fi
			else
				# is package name

				if [ -n "$PACKAGE_NAME_CALL" ]; then
					echo -e "${PALETTE_ERROR}This shell script does not install multiple packages at once${PALETTE_RESET}"
					exit 1
				fi

				PACKAGE_NAME_CALL="$2"
			fi

			shift
		done

		if [[ $PACKAGE_NAME_CALL == '' ]]; then
			echo -e "${PALETTE_ERROR}Package name not given${PALETTE_RESET}"
			exit 1
		fi

		if [[ $PACKAGE_NAME_CALL = 'git+'* ]]; then

			PACKAGE_NAME=$(cut -d '=' -f2 <<< "$PACKAGE_NAME_CALL")

			if [[ $PACKAGE_NAME == '' ]] || [[ $PACKAGE_NAME == $PACKAGE_NAME_CALL ]]; then
				echo -e "${PALETTE_ERROR}When installing a package with git+, you have to add #egg= to specify the package name${PALETTE_RESET}"
				exit 1
			fi
		else
			# remove version info from package name

			if [[ $PACKAGE_NAME_CALL = *';'* ]]; then
				echo -e "${PALETTE_ERROR}Environment markers are not supported in the package name${PALETTE_RESET}"
				exit 1
			fi
			if [[ $PACKAGE_NAME_CALL = *'['* ]]; then
				echo -e "${PALETTE_ERROR}Extras definitions not supported in the package name${PALETTE_RESET}"
				exit 1
			fi

			PACKAGE_NAME="$PACKAGE_NAME_CALL"
			PACKAGE_NAME=$(cut -d '~' -f1 <<< "$PACKAGE_NAME")
			PACKAGE_NAME=$(cut -d '!' -f1 <<< "$PACKAGE_NAME")
			PACKAGE_NAME=$(cut -d '>' -f1 <<< "$PACKAGE_NAME")
			PACKAGE_NAME=$(cut -d '<' -f1 <<< "$PACKAGE_NAME")
			PACKAGE_NAME=$(cut -d '=' -f1 <<< "$PACKAGE_NAME")

			if [[ $PACKAGE_NAME == '' ]] || [[ $PACKAGE_NAME == $PACKAGE_NAME_CALL ]]; then
				echo -e "${PALETTE_ERROR}Could not determine package name!${PALETTE_RESET}"
				exit 1
			fi
		fi

		CURRENT_ENV="$VIRTUAL_ENV"

		if [[ $CURRENT_ENV == '' ]]; then
			echo -e "${PALETTE_ERROR}You must run in an virtual environment to execute singer-cli${PALETTE_RESET}"
			exit 1
		fi

		PACKAGE_VENV="$CURRENT_ENV/../.singer/$PACKAGE_NAME"

		if [ -d $PACKAGE_VENV/ ]; then
			# if venv exists, call pip from venv
			$PACKAGE_VENV/bin/pip install $PIP_INSTALL_PRE_ARGS $PACKAGE_NAME_CALL$PIP_INSTALL_SUB_ARGS
		else
			# if venv does not exists, create venv
			python -m venv "$PACKAGE_VENV"
			RC=$?; [ $RC -ne 0 ] && exit $RC
			$PACKAGE_VENV/bin/pip install wheel
			RC=$?; [ $RC -ne 0 ] && exit $RC
			$PACKAGE_VENV/bin/pip install $PIP_INSTALL_PRE_ARGS $PACKAGE_NAME_CALL$PIP_INSTALL_SUB_ARGS
			RC=$?; [ $RC -ne 0 ] && exit $RC

			# create symbolic link

			SYMBOLIC_LINK_TARGET="../../.singer/$PACKAGE_NAME/bin/$PACKAGE_NAME"
			SYMBOLIC_LINK_NAME="$CURRENT_ENV/bin/$PACKAGE_NAME"
			if [ -L "$SYMBOLIC_LINK_NAME" ]; then
				rm -f "$SYMBOLIC_LINK_NAME"
			fi

			ln -s "$SYMBOLIC_LINK_TARGET" "$SYMBOLIC_LINK_NAME"
			RC=$?; [ $RC -ne 0 ] && exit $RC
		fi

	fi

	# exist with OK
	exit 0

elif [[ $1 == 'uninstall' ]]; then

	## uninstall package

	if [[ $# -eq 1 ]]; then
		echo -e "${PALETTE_ERROR}Package name not given${PALETTE_RESET}"
		exit 1
	fi

	PACKAGE_NAME="$2"

	CURRENT_ENV="$VIRTUAL_ENV"

	if [[ $CURRENT_ENV == '' ]]; then
		echo -e "${PALETTE_ERROR}You must run in an virtual environment to execute singer-cli${PALETTE_RESET}"
		exit 1
	fi

	PACKAGE_VENV="$CURRENT_ENV/../.singer/$PACKAGE_NAME"

	rm -f "$CURRENT_ENV/bin/$PACKAGE_NAME"
	rm -rf "$PACKAGE_VENV"

	exit 0

elif [[ $1 == 'list' ]]; then

	# list packages

	SEARCH_STRING='*'
	if [[ $# -gt 1 ]]; then
		SEARCH_STRING="$2"
	fi

	[ -d .singer/ ] &&	find .singer/$SEARCH_STRING -maxdepth 0 -mindepth 0 -type d -printf '%f\n'

elif [[ $1 == 'freeze' ]]; then

	CURRENT_ENV="$VIRTUAL_ENV"

	bash ./$0 list |
		while IFS= read -r PACKAGE_NAME
		do
			PACKAGE_VENV="$CURRENT_ENV/../.singer/$PACKAGE_NAME"
			$PACKAGE_VENV/bin/pip freeze | grep $PACKAGE_NAME | head -1 | sed "s/#egg=.\+/#egg=$PACKAGE_NAME/"
		done

else
	echo 'singer-cli.sh 0.4.1'
	echo 'Usage: singer-cli.sh <command> [args]'
	echo ''
	echo 'singer-cli.sh is a simple package manager script for singer.io'
	echo 'tap/target pip packages'
	echo ''
	echo 'Commands:'
	echo '  install [package_name]        - Install a tap/target pip package in a isoladted environment'
	echo '  uninstall [package_name]      - Uninstall a tap/target pip package'
	echo '  list (optional_search_string) - List installed packages.'
	echo '  freeze                        - Output installed packages in requirements format.'
	echo ''
	echo 'Sample usage:'
	echo '  # install packages'
	echo '  singer-cli.sh install tap-exchangeratesapi'
	echo '  singer-cli.sh install target-csv'
	echo ''
	echo '  # call packages'
	echo '  tap-exchangeratesapi | target-csv'
	echo ''
	echo '  # uninstall packages'
	echo '  singer-cli.sh uninstall tap-exchangeratesapi'
	echo '  singer-cli.sh uninstall target-csv'
fi
