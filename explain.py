import psycopg2
import json
import difflib as dl
import re
import sqlparse
from definitions import *

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
def traverse_qp_json_1(plan, plan_operations):
    if "Plans" in plan:
        if isinstance(plan["Plans"], dict):
            traverse_qp_json_1(plan["Plans"], plan_operations)
        elif isinstance(plan["Plans"], list):
            for i in reversed(range(len(plan["Plans"]))):
                traverse_qp_json_1(plan["Plans"][i], plan_operations)
    
    if "Node Type" in plan:
        output = ""
        curr_node_type = plan["Node Type"]
        if curr_node_type in node_type_dict:
            # print(curr_node_type)
            output = output + node_type_dict[curr_node_type].format(**plan)
            if "Filter" in plan:
                output = output + ", filtered on {}".format(plan["Filter"])
            elif "Join Filter" in plan:
                output = output + ", join filtered on {}".format(plan["Join Filter"])

            plan_operations.append(output)
        else: 
            plan_operations.append(plan["Node Type"])

# this function traverses both query plans at the same time and finds differences in "Node Type"
# TODO - include a short explanation on different "Node Types" and what they are operated on eg. on what relation
# def traverse_qp_json_2(plan1, plan2):

#     if "Plans" in plan1 and "Plans" in plan2:
#         if isinstance(plan1["Plans"], dict) and isinstance(plan2["Plans"], dict):
#             traverse_qp_json_2(plan1["Plans"], plan2["Plans"])
#         elif isinstance(plan1["Plans"], list) and isinstance(plan2["Plans"], list):
#             for i in range(min(len(plan1["Plans"]), len(plan2["Plans"]))):
#                 traverse_qp_json_2(plan1["Plans"][i], plan2["Plans"][i])
#             # print("i = {i}".format(i = i))
#     elif "Plans" in plan1 and "Plans" not in plan2:
#         print("P has:")
#         for i in range(len(plan1["Plans"])):
#             traverse_qp_json_1(plan1["Plans"][i])
#     elif "Plans" in plan2 and "Plans" not in plan1:
#         print("P' has: \n")
#         for i in range(len(plan2["Plans"])):
#             traverse_qp_json_1(plan2["Plans"][i])

#     if (plan1["Node Type"] != plan2["Node Type"]):
#         print("P is doing: {nodeType_1}, whereas P' is doing: {nodeType_2}".format(nodeType_1 = plan1["Node Type"], nodeType_2 = plan2["Node Type"]))


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

    plan1_ops = []
    plan2_ops = []

    # traverse_qp_json_2(plan1, plan2)
    traverse_qp_json_1(plan1, plan1_ops)
    traverse_qp_json_1(plan2, plan2_ops)
    plan1_full=plan1_ops
    plan2_full=plan2_ops
    plan1_extras = [x for x in plan1_ops if x not in plan2_ops]
    plan2_extras = [x for x in plan2_ops if x not in plan1_ops]

    print('\n')
    print(" ----- Because -----")
    print('\n')
    # here we compare the differences in the queries
    q1 = sqlparse.format(query1, keyword_case='upper', strip_comments=True)
    q2 = sqlparse.format(query2, keyword_case='upper', strip_comments=True)

    q1_keywords = []
    q2_keywords = []

    q1_parsed = sqlparse.parse(q1)[0]
    q2_parsed = sqlparse.parse(q2)[0]

    for t in q1_parsed.tokens:
        if t.ttype is sqlparse.tokens.Keyword or t.value == 'SELECT':
            q1_keywords.append(t.value.upper())
        elif t.is_group:
            for nt in t.tokens:
                if nt.ttype is sqlparse.tokens.Keyword:
                    q1_keywords.append(nt.value)

    for t in q2_parsed.tokens:
        if t.ttype is sqlparse.tokens.Keyword or t.value == 'SELECT':
            q2_keywords.append(t.value.upper())
        elif t.is_group:
            for nt in t.tokens:
                if nt.ttype is sqlparse.tokens.Keyword:
                    q2_keywords.append(nt.value)
        
    q1 = re.sub(r'[,;]', '', q1)
    q2 = re.sub(r'[,;]', '', q2)
    q1 = q1.split()
    q2 = q2.split()

    matcher = dl.SequenceMatcher(None, q1, q2)

    q1_currClause = 0
    q2_currClause = 0

    diff_in_queries = []

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        for item in q1_keywords:
            if item in ' '.join(q1[i1:i2]):
                q1_currClause = item
        for item in q2_keywords:
            if item in ' '.join(q2[j1:j2]):
                q2_currClause = item
        if op == 'replace':
            diff_in_queries.append("'{q1}' has been modified to '{q2}' under the {clause} clause".format(q1 = ' '.join(q1[i1:i2]), q2 = ' '.join(q2[j1:j2]), clause = q1_currClause))

        elif op == 'delete':
            q1_string = ' '.join(q1[i1:i2])
            if q1_currClause in q1_string:
                q1_string = q1_string.replace(q1_currClause, '').strip()
            diff_in_queries.append("'{q1}' under the {clause} clause in original query, has been removed".format(q1 = q1_string, clause = q1_currClause))
            
        elif op == 'insert':
            q2_string = ' '.join(q2[j1:j2])
            if q2_currClause in q2_string:
                q2_string = q2_string.replace(q2_currClause, '').strip()
            diff_in_queries.append("'{q2}' has been added to the new query under the {clause} clause".format(q2 = q2_string, clause = q2_currClause))


    return plan1_extras, plan2_extras, diff_in_queries,plan1_full,plan2_full
