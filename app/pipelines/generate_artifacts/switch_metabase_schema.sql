-- create metabase read-only user if it does not already exist
DO
$$
    BEGIN
        IF NOT EXISTS(SELECT *
                      FROM pg_catalog.pg_user
                      WHERE usename = 'metabase')
        THEN
            EXECUTE 'CREATE ROLE metabase LOGIN';
        END IF;
    END
$$;


GRANT USAGE ON SCHEMA metabase_next TO metabase;
GRANT SELECT ON ALL TABLES IN SCHEMA metabase_next TO metabase;


SELECT util.replace_schema('metabase', 'metabase_next');
