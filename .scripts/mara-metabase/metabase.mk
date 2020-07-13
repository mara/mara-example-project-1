# run metabase locally

# set variables unless already set earlier
metabase-directory ?= .metabase
metabase-version ?= v0.35.4
metabase-metadata-db ?= metabase_metadata
metabase-metadata-db-connection-uri ?= postgres://127.0.0.1:5432/$(metabase-metadata-db)?user=root

# the directory of this Makefile
mara-metabase-scripts-dir := $(dir $(lastword $(MAKEFILE_LIST)))

# where mara-metabase is installed relative to the project root
mara-metabase-package-dir ?= packages/mara-metabase


# run metabase with the configured metadata database connection
run-metabase: $(metabase-directory)/metabase-$(metabase-version).jar
	cd $(metabase-directory); MB_DB_CONNECTION_URI=$(metabase-metadata-db-connection-uri) java -jar metabase-$(metabase-version).jar

# download the Metabase jar file
$(metabase-directory)/metabase-$(metabase-version).jar:
	mkdir -pv $(metabase-directory)
	DISABLE_MAKESHELL wget --output-document=$@ --show-progress https://downloads.metabase.com/$(metabase-version)/metabase.jar

# run the database migrations
migrate-metabase-db: $(metabase-directory)/metabase-$(metabase-version).jar
	cd $(metabase-directory); MB_DB_CONNECTION_URI=$(metabase-metadata-db-connection-uri) java -jar metabase-$(metabase-version).jar migrate up

# create admin user, the DWH database connection and write some settings
setup-metabase: migrate-metabase-db .copy-mara-metabase-scripts
	source .venv/bin/activate; flask mara_metabase.setup


# copy scripts from mara-metabase package to project code
.copy-mara-metabase-scripts:
	rsync --archive --recursive --itemize-changes  --delete $(mara-metabase-package-dir)/.scripts/ $(mara-etabase-scripts-dir)


.cleanup-metabase:
	rm -rf $(metabase-directory)

