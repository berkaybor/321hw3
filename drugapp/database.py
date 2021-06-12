from django.db import connection


def return_drugs():
    stmt = 'SELECT * FROM drugs'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for u in tmp:
        x = {"drugbank_id": u[0], "drug_name": u[1], "description": u[2]}
        drugs.append(x)
    return drugs


def return_drug_details(drugid):
    stmt = 'SELECT * FROM drugs where drugbank_id = "{}"'.format(drugid)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    x = {"drugbank_id": tmp[0][0], "drug_name": tmp[0][1], "description": tmp[0][2]}
    return x
