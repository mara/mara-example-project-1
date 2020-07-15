# databases that are needed in a local setup

dwh-db := example_project_1_dwh
mara-db := example_project_1_mara
olist-db := olist_ecommerce

# overwrites variables in ./mara-metabase/metabase.mk
metabase-data-db := example_project_1_metabase_data
metabase-metadata-db := example_project_1_metabase_metadata

# overwrites variable in ./mara-mondrian/mondrian-server.mk
mondrian-server-db := $(dwh-db)

databases := dwh-db mara-db olist-db metabase-data-db metabase-metadata-db


# create all configured databases
ensure-databases: $(addprefix .ensure-database-, $(databases))

.ensure-database-%:
	if psql -lqt | cut -d \| -f 1 | grep -qw $($*) ; then \
		echo "$* database exists"; \
	else \
		psql postgres -c "create database $($*);"; \
	fi;


# delete all databases
.cleanup-databases: $(addprefix .cleanup-database-, $(databases))

.cleanup-database-%:
	if psql -lqt | cut -d \| -f 1 | grep -qw $($*) ; then \
		psql postgres -c "drop database $($*);"; \
	fi;
