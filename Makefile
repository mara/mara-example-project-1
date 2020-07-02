all:
	make -j ensure-config ensure-databases
	make setup-mara
	make -j load-olist-data setup-metabase setup-mondrian-server


# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# creation of databases that are needed in a local setup
include .scripts/databases.mk

# ensure local_setup.py exists
include .scripts/config.mk

# metabase setup
include .scripts/metabase.mk

# mondrian server and saiku
include .scripts/mara-mondrian/mondrian_server.mk

load-olist-data:
	. .venv/bin/activate; flask olist_ecommerce.load-data

cleanup:
	make -j .cleanup-vitualenv .cleanup-databases .cleanup-metabase .cleanup-mondrian-server .cleanup-config