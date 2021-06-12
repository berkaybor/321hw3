from django.db import connection


def edit_reaction_affinity(reaction_id, affinity):
    query = "update reaction set affinity = {} where reaction_id = '{}'".format(affinity, reaction_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Update failed'

        return

def delete_drug_from_db(drug_id):
    query = "select * from drugs where drugbank_id = '{}'".format(drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Drug not found'

        tmp = cursor.fetchall()
        if not tmp: return 'Drug not found'

    query = "delete from drugs where drugbank_id = '{}'".format(drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Drug not found'

        return


def delete_prot_from_db(uniport_id):
    query = "select * from protein where uniprot_id = '{}'".format(uniport_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Protein not found'

        tmp = cursor.fetchall()
        if not tmp: return 'Protein not found'

    query = "delete from protein where uniprot_id = '{}'".format(uniport_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Protein not found'

        return


def drug_interactions_db(drug_id):
    query = 'select interacted_drug from interactions where drug = "{}"'.format(drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return
        return cursor.fetchall()


def view_side_effects_db(drug_id):
    query = "select umls_cui, side_effect_name from causes left join side_effects se on causes.side_effect = se.umls_cui where drug = '{}'".format(drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return
        return cursor.fetchall()


def view_interacting_targets_db(drug_id):
    query = """
    select uniprot_id, protein_name from binds_to left join protein p on p.uniprot_id = binds_to.protein
    left join undergoes u on binds_to.reaction = u.reaction
    where drug = '{}'""".format(drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return
        return cursor.fetchall()


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
