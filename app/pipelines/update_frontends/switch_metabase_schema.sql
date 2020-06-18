SELECT util.replace_schema('metabase', 'metabase_next');

DO $$
  BEGIN
    IF NOT EXISTS(SELECT *
                  FROM pg_catalog.pg_user
                  WHERE usename = 'metabase')
    THEN
      EXECUTE 'CREATE ROLE metabase LOGIN';
    END IF;
  END $$;

GRANT USAGE ON SCHEMA metabase TO metabase;
GRANT SELECT ON ALL TABLES IN SCHEMA metabase TO metabase;

