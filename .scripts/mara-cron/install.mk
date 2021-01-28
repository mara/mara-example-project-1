
setup-cron: .copy-mara-cron-scripts


# copy scripts from mara-cron package to project code
.copy-mara-cron-scripts:
	rsync --archive --recursive --itemize-changes  --delete packages/mara-cron/.scripts/ .scripts/mara-cron/
