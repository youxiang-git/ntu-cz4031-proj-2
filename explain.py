import psycopg2
import json

def StartDBConnection():
    conn = None
    # Connect to your postgres DB
    conn = psycopg2.connect(host="localhost",
                            database="postgres",
                            user="postgres",
                            password="password1111",
                            port="5432")
    conn.cursor().execute("set search_path to \"TPC-H\"")
    return conn

def GetQueryPlan(query):
    explain_query = f"EXPLAIN (ANALYZE false, SETTINGS true, FORMAT JSON) {query};"

    db_conn = StartDBConnection()

    with db_conn.cursor() as cur:
        cur.execute(explain_query)
        return cur.fetchall()[0][0][0].get("Plan") # PROBABLY NEED TO FORMAT THIS PROPERLY
    
def GetAllNodes(query, indent):

    for k, v in query.items():
        if type(v) == str:
            print(indent*"\t" + v)
        
        if k == "Plans":
            for item in v:
                GetAllNodes(item, indent+1)

def CompareQueries(query1, query2):
    if query1 == query2:
        print("There are no differences between the queries, please check your input.")
        return

    plan1 = GetQueryPlan(query1)
    plan2 = GetQueryPlan(query2)

    output_file = open("output.json", "w")
    json.dump([plan1, plan2], output_file, indent=2)
    output_file.close()
    
    GetAllNodes(plan1, 0)
    print("\n\n")
    GetAllNodes(plan2, 0)


    # print("PLAN 1\n----")
    # print(plan1_json)
    # print("\n----")
    # print("PLAN 2\n----")
    # print(plan2_json)
    # print("\n----")
