# Ensure that databases and app/local_setup.py exist

dwh-etl-db := example_project_1_dwh
dwh-mara-db := example_project_1_mara
olist-db := olist_ecommerce
metabase-db := example_project_1_metabase


ensure-config:
	make -s -j app/local_setup.py $(addprefix .ensure-database-, $(dwh-etl-db) $(dwh-mara-db) $(olist-db) $(metabase-db))

app/local_setup.py:
	cp -v app/local_setup.py.example app/local_setup.py

.ensure-database-%:
	if psql -lqt | cut -d \| -f 1 | grep -qw $* ; then \
		echo "$* database exists"; \
	else \
		psql postgres -c "create database $*;"; \
	fi;