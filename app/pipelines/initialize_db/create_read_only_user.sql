CREATE OR REPLACE FUNCTION util.ensure_user_exists(user_name TEXT)
  RETURNS VOID AS
$$
BEGIN
  IF NOT EXISTS(SELECT *
                FROM pg_catalog.pg_user
                WHERE usename = user_name)
  THEN
    EXECUTE 'CREATE ROLE ' || user_name || ' LOGIN';
  END IF;
END
$$
  LANGUAGE plpgsql;




DO $$
  DECLARE
    schema_name TEXT;
  BEGIN
    PERFORM util.ensure_user_exists('dwh_read_only');

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


