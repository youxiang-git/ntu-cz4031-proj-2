from explain import *

# sample_query1 = "select c.c_name, O.o_orderkey, n.n_name from customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316' ORDER BY o.o_orderkey;"
# sample_query2 = "select c.c_name, o.o_orderkey, n.n_name from customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316';"
# sample_query1 = "SELECT c.c_name, o.o_orderkey, n.n_name FROM customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316';"
# sample_query2 = "SELECT c.c_name, o.o_orderkey, n.n_name FROM customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316' AND o.o_orderpriority = '1-URGENT';"

# sample_query1 = "select * from customer c where c.c_name = 'Customer#000000316'"
# sample_query2 = "select * from customer c"
sample_query1 = "SELECT sum(C.c_acctbal) FROM customer AS c, nation AS n WHERE c.c_nationkey = n.n_nationkey AND n.n_name = 'INDIA'"
sample_query2 = "SELECT sum(C.c_acctbal) FROM customer AS c, nation AS n WHERE c.c_nationkey = n.n_nationkey AND n.n_name = 'ARGENTINA'"

CompareQueries(sample_query1, sample_query2)