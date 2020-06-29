all: ensure-config
	make -s -j setup-mara
	make load-olist-data
	make setup-metabase


# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# project specific scripts
include .scripts/config.mk
include .scripts/metabase.mk

load-olist-data:
	. .venv/bin/activate; flask olist_ecommerce.load-data

# run saiku and mondrian
run-mondrian-server:
	java -Dmondrian-server.properties=./mondrian-server.properties -jar packages/mara-mondrian/mara_mondrian/jetty-runner.jar --port 8080 packages/mara-mondrian/mara_mondrian/mondrian-server.war 2>&1