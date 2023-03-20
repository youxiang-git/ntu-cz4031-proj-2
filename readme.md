# CZ4031 Project 2

## How to import files to PostgreSQL

Ensure that you have PostgreSQL installed and have obtained the generated tbl files from dbgen.

1. Connect to your PostgreSQL database, it is recommended to use SQL shell (psql).

    Or in any terminal, type:

```bash
psql
```

2. Create a new database / schema:

```pgsql
create schema "TPC-H";
```

3. Set search path to TPC-H

```pgsql
set search_path to "TPC-H";
```

4. Create the empty relations / tables

```pgsql region
-- Table: TPC-H.region

-- DROP TABLE IF EXISTS "TPC-H".region;

CREATE TABLE IF NOT EXISTS "TPC-H".region
(
    r_regionkey integer NOT NULL,
    r_name character(25) COLLATE pg_catalog."default" NOT NULL,
    r_comment character varying(152) COLLATE pg_catalog."default",
    CONSTRAINT region_pkey PRIMARY KEY (r_regionkey)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".region
    OWNER to postgres;
```

```pgsql nation
-- Table: TPC-H.nation

-- DROP TABLE IF EXISTS "TPC-H".nation;

CREATE TABLE IF NOT EXISTS "TPC-H".nation
(
    n_nationkey integer NOT NULL,
    n_name character(25) COLLATE pg_catalog."default" NOT NULL,
    n_regionkey integer NOT NULL,
    n_comment character varying(152) COLLATE pg_catalog."default",
    CONSTRAINT nation_pkey PRIMARY KEY (n_nationkey),
	CONSTRAINT fk_nation FOREIGN KEY (n_regionkey)
		REFERENCES "TPC-H".region (r_regionkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)

WITH (
	OIDS = FALSE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".nation
    OWNER to postgres;
```

```pgsql part
-- Table: TPC-H.part

-- DROP TABLE IF EXISTS "TPC-H".part;

CREATE TABLE IF NOT EXISTS "TPC-H".part
(
    p_partkey integer NOT NULL,
    p_name character varying(55) COLLATE pg_catalog."default" NOT NULL,
    p_mfgr character(25) COLLATE pg_catalog."default" NOT NULL,
    p_brand character(10) COLLATE pg_catalog."default" NOT NULL,
    p_type character varying(25) COLLATE pg_catalog."default" NOT NULL,
    p_size integer NOT NULL,
    p_container character(10) COLLATE pg_catalog."default" NOT NULL,
    p_retailprice numeric(15,2) NOT NULL,
    p_comment character varying(23) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT part_pkey PRIMARY KEY (p_partkey)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".part
    OWNER to postgres;
```
