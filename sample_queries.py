sample_query_dict = {
    'sample_pair1_q1': "SELECT c.c_name, o.o_orderkey, n.n_name FROM customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316';",
    'sample_pair1_q2': "SELECT C.c_name, o.o_orderkey, n.n_name FROM customer C INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316' AND o.o_orderpriority = '1-URGENT';"
    
}