

DO $$
  DECLARE
    schema_name TEXT;
  BEGIN
      -- create a role that has read-only access to the DWH
      IF NOT EXISTS(SELECT *
                    FROM pg_catalog.pg_user
                    WHERE usename = 'dwh_read_only')
      THEN
          EXECUTE 'CREATE ROLE dwh_read_only LOGIN';
      END IF;


      -- grant read only permission on all tables in all existing schemas
      FOR schema_name IN SELECT nspname
                       FROM pg_namespace
      LOOP
        EXECUTE 'GRANT USAGE ON SCHEMA ' || schema_name || ' to dwh_read_only';
        EXECUTE 'GRANT SELECT ON ALL TABLES IN SCHEMA ' || schema_name || ' to dwh_read_only';
      END LOOP;

    -- grant permissions for tables and schemas created in the future
    ALTER DEFAULT PRIVILEGES GRANT SELECT ON TABLES TO dwh_read_only;
    ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO dwh_read_only;

  END $$;


