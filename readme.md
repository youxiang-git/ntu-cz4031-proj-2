# CZ4031 Project 2

## How to import files to PostgreSQL

Ensure that you have PostgreSQL installed and have obtained the generated tbl files from dbgen.

1. Connect to your PostgreSQL database, it is recommended to use SQL shell (psql).

    Or in any terminal, type:

```bash
psql
```

2. Create a new database / schema:

```postgresql
create schema "TPC-H";
```

3. Set search path to TPC-H

```postgresql
set search_path to "TPC-H";
```

4. Create the empty relations / tables

```postgresql region
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

```postgresql nation
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

```postgresql part
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

```postgresql supplier
-- Table: TPC-H.supplier

-- DROP TABLE IF EXISTS "TPC-H".supplier;

CREATE TABLE IF NOT EXISTS "TPC-H".supplier
(
    s_suppkey integer NOT NULL,
    s_name character(25) COLLATE pg_catalog."default" NOT NULL,
    s_address character varying(40) COLLATE pg_catalog."default" NOT NULL,
    s_nationkey integer NOT NULL,
    s_phone character(15) COLLATE pg_catalog."default" NOT NULL,
    s_acctbal numeric(15,2) NOT NULL,
    s_comment character varying(101) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT supplier_pkey PRIMARY KEY (s_suppkey),
    CONSTRAINT fk_supplier FOREIGN KEY (s_nationkey)
        REFERENCES "TPC-H".nation (n_nationkey) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".supplier
    OWNER to postgres;
```

```postgresql partsupp
-- Table: TPC-H.partsupp

DROP TABLE IF EXISTS "TPC-H".partsupp;

CREATE TABLE IF NOT EXISTS "TPC-H".partsupp
(
    ps_partkey integer NOT NULL,
    ps_suppkey integer NOT NULL,
    ps_availqty integer NOT NULL,
    ps_supplycost numeric(15,2) NOT NULL,
    ps_comment character varying(199) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT partsupp_pkey PRIMARY KEY (ps_partkey, ps_suppkey),
    CONSTRAINT fk_ps_suppkey_partkey FOREIGN KEY (ps_partkey)
        REFERENCES "TPC-H".part (p_partkey) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
	CONSTRAINT fk_ps_suppkey_suppkey FOREIGN KEY (ps_suppkey)
		REFERENCES "TPC-H".supplier (s_suppkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".partsupp
    OWNER to postgres;
```

```postgresql customer
-- Table: TPC-H.customer

-- DROP TABLE IF EXISTS "TPC-H".customer;

CREATE TABLE IF NOT EXISTS "TPC-H".customer
(
    c_custkey integer NOT NULL,
    c_name character varying(25) COLLATE pg_catalog."default" NOT NULL,
    c_address character varying(40) COLLATE pg_catalog."default" NOT NULL,
    c_nationkey integer NOT NULL,
    c_phone character(15) COLLATE pg_catalog."default" NOT NULL,
    c_acctbal numeric(15,2) NOT NULL,
    c_mktsegment character(10) COLLATE pg_catalog."default" NOT NULL,
    c_comment character varying(117) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customer_pkey PRIMARY KEY (c_custkey),
	CONSTRAINT fk_customer FOREIGN KEY (c_nationkey)
		REFERENCES "TPC-H".nation (n_nationkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".customer
    OWNER to postgres;
```

```postgresql orders
-- Table: TPC-H.orders

-- DROP TABLE IF EXISTS "TPC-H".orders;

CREATE TABLE IF NOT EXISTS "TPC-H".orders
(
    o_orderkey integer NOT NULL,
    o_custkey integer NOT NULL,
    o_orderstatus character(1) COLLATE pg_catalog."default" NOT NULL,
    o_totalprice numeric(15,2) NOT NULL,
    o_orderdate date NOT NULL,
    o_orderpriority character(15) COLLATE pg_catalog."default" NOT NULL,
    o_clerk character(15) COLLATE pg_catalog."default" NOT NULL,
    o_shippriority integer NOT NULL,
    o_comment character varying(79) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT orders_pkey PRIMARY KEY (o_orderkey),
	CONSTRAINT fk_orders FOREIGN KEY (o_custkey)
		REFERENCES "TPC-H".customer (c_custkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".orders
    OWNER to postgres;
```

```postgresql lineitem
-- Table: TPC-H.lineitem

-- DROP TABLE IF EXISTS "TPC-H".lineitem;

CREATE TABLE IF NOT EXISTS "TPC-H".lineitem
(
    l_orderkey integer NOT NULL,
    l_partkey integer NOT NULL,
    l_suppkey integer NOT NULL,
    l_linenumber integer NOT NULL,
    l_quantity numeric(15,2) NOT NULL,
    l_extendedprice numeric(15,2) NOT NULL,
    l_discount numeric(15,2) NOT NULL,
    l_tax numeric(15,2) NOT NULL,
    l_returnflag character(1) COLLATE pg_catalog."default" NOT NULL,
    l_linestatus character(1) COLLATE pg_catalog."default" NOT NULL,
    l_shipdate date NOT NULL,
    l_commitdate date NOT NULL,
    l_receiptdate date NOT NULL,
    l_shipinstruct character(25) COLLATE pg_catalog."default" NOT NULL,
    l_shipmode character(10) COLLATE pg_catalog."default" NOT NULL,
    l_comment character varying(44) COLLATE pg_catalog."default" NOT NULL,
	CONSTRAINT lineitem_pkey PRIMARY KEY (l_orderkey, l_partkey, l_suppkey, l_linenumber),
	CONSTRAINT fk_lineitem_orderkey FOREIGN KEY (l_orderkey)
		REFERENCES "TPC-H".orders (o_orderkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_lineitem_partkey FOREIGN KEY (l_partkey)
		REFERENCES "TPC-H".part (p_partkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION,
	CONSTRAINT fk_lineitem_suppkey FOREIGN KEY (l_suppkey)
		REFERENCES "TPC-H".supplier (s_suppkey) MATCH SIMPLE
		ON UPDATE NO ACTION
		ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "TPC-H".lineitem
    OWNER to postgres;
```

5. Import the data into the database

#### Before importing, run the following regex script in a terminal to remove the extra '|' character as mentioned in the brief

<u>Please make sure you're in the directory where the .tbl files are located.</u>

```bash
for i in `ls *.tbl`; do sed 's/|$//' $i > ${i/tbl/csv}; echo $i; done;
```

#### IMPORTANT! Replace 'tbl\\\*.csv' with the path to the files on your computer

```postgresql
\copy "region"     from 'tbl\region.csv'      DELIMITER '|' CSV;
\copy "nation"     from 'tbl\nation.csv'      DELIMITER '|' CSV;
\copy "part"       from 'tbl\part.csv'        DELIMITER '|' CSV;
\copy "supplier"   from 'tbl\supplier.csv'    DELIMITER '|' CSV;
\copy "partsupp"   from 'tbl\partsupp.csv'    DELIMITER '|' CSV;
\copy "customer"   from 'tbl\customer.csv'    DELIMITER '|' CSV;
\copy "orders"     from 'tbl\orders.csv'      DELIMITER '|' CSV;
\copy "lineitem"   from 'tbl\lineitem.csv'    DELIMITER '|' CSV;
```
