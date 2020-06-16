# output coloring & timing
include .scripts/mara-app/init.mk

# virtual env creation, package updates, db migration
include .scripts/mara-app/install.mk

# if you don't want to download the two big
sync-bigquery-csv-data-sets-from-s3:
	.venv/bin/aws s3 sync s3://mara-example-project-data data --delete --no-progress --no-sign-request

load-olist-data:
	. .venv/bin/activate; flask olist_ecommerce.load-data

# run saiku and mondrian
run-mondrian-server:
	java -Dmondrian-server.properties=.mondrian-server.properties -jar packages/mara-mondrian/mara_mondrian/jetty-runner.jar --port 8080 packages/mara-mondrian/mara_mondrian/mondrian-server.war 2>&1