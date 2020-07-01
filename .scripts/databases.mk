# databases that are needed in a local setup

dwh-db := example_project_1_dwh
mara-db := example_project_1_mara
olist-db := olist_ecommerce
metabase-data-db := example_project_1_metabase_data
metabase-metadata-db := example_project_1_metabase_metadata

databases := dwh-db mara-db olist-db metabase-data-db metabase-metadata-db


ensure-databases: $(addprefix .ensure-database-, $(databases))

.ensure-database-%:
	if psql -lqt | cut -d \| -f 1 | grep -qw $($*) ; then \
		echo "$* database exists"; \
	else \
		psql postgres -c "create database $($*);"; \
	fi;


.cleanup-databases: $(addprefix .cleanup-database-, $(databases))

.cleanup-database-%:
	if psql -lqt | cut -d \| -f 1 | grep -qw $($*) ; then \
		psql postgres -c "drop database $($*);"; \
	fi;
