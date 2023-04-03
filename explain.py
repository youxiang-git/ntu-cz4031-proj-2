from pprint import pprint
import psycopg2
import json
import difflib as dl
import re

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
    explain_query = f"EXPLAIN (FORMAT JSON) {query};"

    db_conn = StartDBConnection()

    with db_conn.cursor() as cur:
        cur.execute(explain_query)
        return cur.fetchall()[0][0][0][
            'Plan']  # PROBABLY NEED TO FORMAT THIS PROPERLY


def print_query_plan(plan):
    for row in plan:
        print(row[0])

# this function traverses one query plan and prints all the additional "Node Type"s
# used when one tree is longer than the other for whatever reason
# eg. one query is a lot shorter than the other
def traverse_qp_json_1(plan):
    if "Plans" in plan:
        if isinstance(plan["Plans"], dict):
            traverse_qp_json_1(plan["Plans"])
        elif isinstance(plan["Plans"], list):
            for i in range(len(plan["Plans"])):
                traverse_qp_json_1(plan["Plans"][i])
    
    print("\t an additional {nodeType}".format(nodeType = plan["Node Type"]))

# this function traverses both query plans at the same time and finds differences in "Node Type"
# TODO - include a short explanation on different "Node Types" and what they are operated on eg. on what relation
def traverse_qp_json_2(plan1, plan2):

    if "Plans" in plan1 and "Plans" in plan2:
        if isinstance(plan1["Plans"], dict) and isinstance(plan2["Plans"], dict):
            traverse_qp_json_2(plan1["Plans"], plan2["Plans"])
        elif isinstance(plan1["Plans"], list) and isinstance(plan2["Plans"], list):
            for i in range(min(len(plan1["Plans"]), len(plan2["Plans"]))):
                traverse_qp_json_2(plan1["Plans"][i], plan2["Plans"][i])
            # print("i = {i}".format(i = i))
    elif "Plans" in plan1 and "Plans" not in plan2:
        print("P has:")
        for i in range(len(plan1["Plans"])):
            traverse_qp_json_1(plan1["Plans"][i])
    elif "Plans" in plan2 and "Plans" not in plan1:
        print("P' has: \n")
        for i in range(len(plan2["Plans"])):
            traverse_qp_json_1(plan2["Plans"][i])

    if (plan1["Node Type"] != plan2["Node Type"]):
        print("P is doing: {nodeType_1}, whereas P' is doing: {nodeType_2}".format(nodeType_1 = plan1["Node Type"], nodeType_2 = plan2["Node Type"]))


def CompareQueries(query1, query2):
    if query1 == query2:
        print(
            "There are no differences between the SQL queries, please check your input."
        )
        return

    plan1 = GetQueryPlan(query1)
    plan2 = GetQueryPlan(query2)

    out1 = open("plan1_output.json", "w")
    out2 = open("plan2_output.json", "w")
    json.dump(plan1, out1, indent=2)
    json.dump(plan2, out2, indent=2)
    out1.close()
    out2.close()

    # check if the plans are the same
    if plan1 == plan2:
        print("The provided queries have the same query plan.")
        return


    traverse_qp_json_2(plan1, plan2)
    print('\n')
    print(" ----- Because -----")
    # here we compare the differences in the queries
    # remove all commas and semi-colons so that the printed results look nice
    q1 = re.sub(r'[,;]', '', query1)
    q2 = re.sub(r'[,;]', '', query2)
    matcher = dl.SequenceMatcher(lambda x: x == ",", q1, q2)

    same = []

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'replace':
            for word in same:
                if word.isupper():
                    print(word)
            print("'{q1}' has been modified to '{q2}' under the {clause} clause".format(q1 = q1[i1:i2], q2 = q2[j1:j2], clause = same.pop()))

        elif op == 'delete':
            for word in same:
                if word.isupper():
                    print(word)
            print("'{q1}' has deleted under the {clause} clause".format(q1 = q1[i1:i2], clause = same.pop()))

        elif op == 'equal':
            words = q1[i1:i2].split(' ')
            for word in words[::-1]:
                if word.isupper():
                    same.append(word)
                    if len(same) == 1:
                        break
            
            
        elif op == 'insert':
            for word in same:
                if word.isupper():
                    print(word)
            print("'{q2}' has added under the {clause} clause".format(q2 = q2[j1:j2], clause = same.pop()))
