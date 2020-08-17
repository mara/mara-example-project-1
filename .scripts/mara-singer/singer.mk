# singer taps/targets handling

# set variables unless already set earlier
singer-directory ?= .singer

# the directory of this Makefile in project
mara-singer-scripts-dir := $(dir $(lastword $(MAKEFILE_LIST)))

# where mara-singer is installed relative to the project root
mara-singer-package-dir ?= packages/mara-singer

setup-singer: .copy-mara-singer-scripts

# copy scripts from mara-singer package to project code
.copy-mara-singer-scripts:
	rsync --archive --recursive --itemize-changes  --delete $(mara-singer-package-dir)/.scripts/ $(mara-singer-scripts-dir)

# install singer packages from singer-requirements.txt.freeze
install-singer-packages:
	make .venv/bin/python
	source .venv/bin/activate; .scripts/mara-singer/singer-cli.sh install --requirement=singer-requirements.txt.freeze --src=./packages --upgrade --exists-action=w

# update packages from singer-requirements.txt and create singer-requirements.txt.freeze
update-singer-packages:
	make .venv/bin/python
	PYTHONWARNINGS="ignore" .scripts/mara-singer/singer-cli.sh install --requirement=singer-requirements.txt --src=./packages --upgrade --exists-action=w

	# write freeze file
	.scripts/mara-singer/singer-cli.sh freeze > singer-requirements.txt.freeze

.cleanup-singer:
	rm -rf $(singer-directory)