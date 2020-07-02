all:
	make -j ensure-config ensure-databases
	make setup-mara
	make -j load-olist-data setup-metabase


# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# ensure local_setup.py exists
include .scripts/config.mk

# creation of databases that are needed in a local setup
include .scripts/databases.mk

# metabase setup
include .scripts/mara-metabase/metabase.mk

load-olist-data:
	. .venv/bin/activate; flask olist_ecommerce.load-data

# run saiku and mondrian
run-mondrian-server:
	java -Dmondrian-server.properties=./mondrian-server.properties -jar packages/mara-mondrian/mara_mondrian/jetty-runner.jar --port 8080 packages/mara-mondrian/mara_mondrian/mondrian-server.war 2>&1


cleanup:
	make -j .cleanup-vitualenv .cleanup-databases .cleanup-metabase .cleanup-config