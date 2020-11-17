# properties file setup, run mondrian-server locally

mondrian-server-directory ?= .mondrian-server
mondrian-server-properties-file := $(mondrian-server-directory)/mondrian-server.properties
saiku-storage-directory ?= $(mondrian-server-directory)/saiku-queries

mondrian-server-db ?= dwh
mondrian-server-db-connection-url ?= jdbc:postgresql://localhost/$(mondrian-server-db)?user=root

# absolute path to mondrian schema file
mondrian-schema-file ?= $(shell pwd)/.mondrian-schema.xml

# where mara-mondrian is installed relative to the project root
mara-mondrian-dir ?= packages/mara-mondrian

# the directory of this Makefile in project
mara-mondrian-scripts-dir := $(dir $(lastword $(MAKEFILE_LIST)))



# run mondrian server
run-mondrian-server: $(mondrian-server-properties-file)
	java -Dmondrian-server.properties=$(mondrian-server-properties-file) -Dlog4j.logLevel=INFO \
	   -jar $(mara-mondrian-dir)/jetty-runner.jar \
	   --port 8080 \
	   $(mara-mondrian-dir)/mondrian-server.war 2>&1


# create mondrian server directory and config file
setup-mondrian-server: .copy-mara-mondrian-scripts
	make -j $(mondrian-server-properties-file) $(saiku-storage-directory) .copy-mara-mondrian-scripts

$(mondrian-server-directory):
	mkdir -pv $@

$(saiku-storage-directory):
	mkdir -pv $@



$(mondrian-server-properties-file): $(mondrian-server-directory)
	cat $(mara-mondrian-dir)/mondrian-server.properties.example \
	   | sed 's@/absolute/path/to/mondrian-schema.xml@$(subst @,\@,$(mondrian-schema-file))@g' \
	   | sed 's@^databaseUrl.*@databaseUrl=$(subst @,\@,$(mondrian-server-db-connection-url))@g' \
	   | sed 's@^saikuStorageDir.*@saikuStorageDir=$(subst @,\@,$(saiku-storage-directory))@g' \
	   > $(mondrian-server-properties-file)
	>&2 echo '!!! copied $(mara-mondrian-dir)/mondrian-server.properties.example to $(mondrian-server-properties-file). Please check'


# copy scripts from mara-app package to project code
.copy-mara-mondrian-scripts:
	rsync --archive --recursive --itemize-changes  --delete $(mara-mondrian-dir)/.scripts/ $(mara-mondrian-scripts-dir)

.cleanup-mondrian-server:
	rm -rf $(mondrian-server-directory)
