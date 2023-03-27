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

def CompareQueries(query1, query2):
    plan1 = GetQueryPlan(query1)
    plan2 = GetQueryPlan(query2)

    output_file = open("output.json", "w")
    json.dump([plan1, plan2], output_file, indent=2)
    output_file.close()
     
    plan1_json = json.dumps(plan1, indent=2)
    plan2_json = json.dumps(plan2, indent=2)
    
    print("PLAN 1\n----")
    print(plan1_json)
    print("\n----")
    print("PLAN 2\n----")
    print(plan2_json)
    print("\n----")
