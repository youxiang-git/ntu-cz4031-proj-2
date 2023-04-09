from explain import *

sample_query1 = "select c.c_name, o.o_orderkey, n.n_name from customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316' LIMIT 100"
sample_query2 = "select c.c_name, o.o_orderkey, n.n_name from customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316';"

# sample_query1 = "select * from customer c, nation n where n.n_nationkey = c.c_nationkey order by c_nationkey asc"
# sample_query2 = "select c.c_name from customer c, nation n where n.n_nationkey = c.c_nationkey order by c_nationkey asc"
# sample_query1 = "select c_name, o_comment from customer inner join orders on c_custkey = o_orderkey;"
# sample_query2 = "select c_name, o_comment from customer inner join orders on c_custkey = o_custkey;"

# sample_query1 = "SELECT c.c_name, o.o_orderkey, n.n_name FROM customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316';"
# sample_query2 = "SELECT c.c_name, o.o_orderkey, n.n_name FROM customer c INNER JOIN orders o ON c.c_custkey = o.o_custkey INNER JOIN nation n ON c.c_nationkey = n.n_nationkey WHERE c.c_name = 'Customer#000000316' AND o.o_orderpriority = '1-URGENT';"

# sample_query1 = "select * from customer c where c.c_name = 'Customer#000000316'"
# sample_query2 = "select * from customer c"

# sample_query1 = "SELECT sum(C.c_acctbal) FROM customer AS c, nation AS n WHERE c.c_nationkey = n.n_nationkey AND n.n_name = 'INDIA'"
# sample_query2 = "SELECT sum(C.c_acctbal) FROM customer AS c, nation AS n WHERE c.c_nationkey = n.n_nationkey AND n.n_name = 'ARGENTINA'"

plan1diff, plan2diff, qdiff = CompareQueries(sample_query1, sample_query2)

print("P has the following extra operations:")
for i in plan1diff:
    print(i)

print()

print("P' has the following extra operations:")
for i in plan2diff:
    print(i)

print()

print("The queries are different in the following ways:")
for i in qdiff:
    print(i)