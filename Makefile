all:
	make -j ensure-config ensure-databases
	make setup-mara
	make -j load-olist-data setup-metabase setup-mondrian-server

run:
	make -j run-metabase run-mondrian-server run-flask

# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# ensure local_setup.py exists
include .scripts/config.mk

# creation of databases that are needed in a local setup
include .scripts/databases.mk

# overwrite metabase version
metabase-version ?= v0.37.0.1

# metabase setup
include .scripts/mara-metabase/metabase.mk

# mondrian server setup
include .scripts/mara-mondrian/mondrian-server.mk

load-olist-data:
	. .venv/bin/activate; flask olist_ecommerce.load-data

cleanup:
	make -j .cleanup-vitualenv .cleanup-databases .cleanup-metabase .cleanup-mondrian-server .cleanup-config