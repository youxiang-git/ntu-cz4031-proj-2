from explain import * 

sample_query1 = "SELECT * FROM region r INNER JOIN nation n ON r.r_regionkey = n.n_regionkey;"
sample_query2 = "SELECT * FROM region r INNER JOIN nation n ON r.r_regionkey = n.n_regionkey WHERE r.r_name = 'ASIA';"
CompareQueries(sample_query1, sample_query2)