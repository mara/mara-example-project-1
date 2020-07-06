# properties file setup, run mondrian-server locally

project_dir := $(CURDIR)
saiku_storage_dir := $(CURDIR)/data/saiku-queries

dwh-db ?= example_project_1_dwh
dwh-db-connection-url ?= jdbc:postgresql://localhost/$(dwh-db)?user=root

# run saiku and mondrian server
run-mondrian-server:
	java -Dmondrian-server.properties=mondrian-server.properties -jar packages/mara-mondrian/mara_mondrian/jetty-runner.jar --port 8080 packages/mara-mondrian/mara_mondrian/mondrian-server.war 2>&1

setup-mondrian-server: .copy-mara-mondrian-scripts
	make mondrian-server-properties

mondrian-server-properties:
	if [ ! -f mondrian-server.properties ] ; then \
    	cp mondrian-server.properties.example mondrian-server.properties; \
        echo "!!! copied mondrian-server.properties.example to mondrian-server.properties. Please check"; \
    fi;
	make mondrian-server-properties-config

mondrian-server-properties-config:
	sed -i '' 's~databaseUrl.*~databaseUrl=$(dwh-db-connection-url)~g' mondrian-server.properties
	sed -i '' 's~mondrianSchemaFile.*~mondrianSchemaFile=$(project_dir)/mondrian_schema.xml~g' mondrian-server.properties
	sed -i '' 's~saikuStorageDir.*~saikuStorageDir=$(saiku_storage_dir)~g' mondrian-server.properties

# copy scripts from mara-app package to project code
.copy-mara-mondrian-scripts:
	rsync --archive --recursive --itemize-changes  --delete packages/mara-mondrian/.scripts/ .scripts/mara-mondrian/

.cleanup-mondrian-server:
	rm -f mondrian-server.properties