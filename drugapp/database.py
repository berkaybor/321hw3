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
    query = "select umls_cui, side_effect_name from causes left join side_effects se on causes.side_effect = se.umls_cui where drug = '{}'".format(
        drug_id)
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


def view_interacting_drugs_db(drug_id):
    query = """
    select drugbank_id, drug_name from binds_to left join undergoes u on binds_to.reaction = u.reaction left join drugs d on d.drugbank_id = u.drug where protein = 
'{}'""".format(
        drug_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return
        return cursor.fetchall()


def update_contributors_db(reaction_id, authors, username, password):
    with connection.cursor() as cursor:
        query = 'update written_by set username = "{}" where reaction = "{}";'.format(username, reaction_id)
        try:
            cursor.execute(query)
        except:
            return 'Update failed1'

        query = 'update users set password = "{}" where username = "{}" and institution = (select institution from written_by where reaction = "{}");'.format(
            password, username, reaction_id)
        try:
            cursor.execute(query)
        except:
            return 'Update failed2'

        query = 'delete from author_list where doi = (select doi from written_by where reaction = "{}");'.format(
            reaction_id)
        try:
            cursor.execute(query)
        except:
            return 'Update failed3'

        author_list = [aut.strip() for aut in authors.split(';')]
        for aut in author_list:
            query = 'insert into author_list values ((select doi from written_by where reaction = "{}"), "{}");'.format(
                reaction_id, aut)
            try:
                cursor.execute(query)
            except:
                return 'Update failed4'

        return


def return_drugs():
    stmt = 'SELECT drugbank_id, drug_name FROM drugs'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for u in tmp:
        x = {"drugbank_id": u[0], "drug_name": u[1]}
        drugs.append(x)
    return drugs


def return_drug_details(drugid):
    stmt = "select drugbank_id, drug_name, smiles, description from drugs left join notation n on drugs.drugbank_id = n.drug_id left join undergoes u on drugs.drugbank_id = u.drug left join binds_to bt on u.reaction = bt.reaction where drugbank_id = '{}'".format(
        drugid)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    x = {"drugbank_id": tmp[0][0], "drug_name": tmp[0][1], "smiles": tmp[0][2], "description": tmp[0][3]}
    stmt = "select side_effect_name from causes left join side_effects se on se.umls_cui = causes.side_effect where drug = '{}'".format(
        drugid)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    side = []
    for s in tmp:
        side.append(s[0])
    x["side_effect"] = side
    stmt = "select protein_name from undergoes left join binds_to bt on undergoes.reaction = bt.reaction left join protein p on p.uniprot_id = bt.protein where drug = '{}'".format(
        drugid)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    targets = []
    for p in tmp:
        targets.append(p[0])
    x["protein"] = targets
    return x


def view_drugs_of_side_effect_db(side_effect):
    stmt = 'select drugbank_id, drug_name from causes left join side_effects se on se.umls_cui = causes.side_effect left join drugs d on d.drugbank_id = causes.drug where umls_cui = "{}"'.format(
        side_effect)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for u in tmp:
        x = {"drugbank_id": u[0], "drug_name": u[1]}
        drugs.append(x)
    return drugs


def get_same_protein_drugs_db():
    stmt = 'select protein,count(drug) from binds_to left join undergoes u on binds_to.reaction = u.reaction group by (protein) having count(drug) > 1'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    proteins = []
    for u in tmp:
        proteins.append(u[0])

    proteins_list = []
    for p in proteins:
        stmt = 'select drug from binds_to left join undergoes u on binds_to.reaction = u.reaction where protein = "{}"'.format(
            p)
        cursor = connection.cursor()
        cursor.execute(stmt)
        tmp = cursor.fetchall()
        x = {}
        y = []
        for d in tmp:
            y.append(d[0])
        x = {"protein": p, "drugs": y}
        proteins_list.append(x)
    return proteins_list


def return_proteins():
    stmt = 'SELECT * FROM protein'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    proteins = []
    for u in tmp:
        x = {"uniprot_id": u[0], "protein_name": u[2]}
        proteins.append(x)
    return proteins


def return_side_effects():
    stmt = 'SELECT * FROM side_effects'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    side_effects = []
    for u in tmp:
        x = {"umls_cui": u[0], "side_effect_name": u[1]}
        side_effects.append(x)
    return side_effects


def list_papers_db():
    stmt = 'SELECT * FROM written_by'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    side_effects = []
    for u in tmp:
        doi = u[3]
        stmt = 'select * from author_list where doi = "{}"'.format(doi)
        cursor = connection.cursor()
        cursor.execute(stmt)
        tmp2 = cursor.fetchall()
        authors = []
        for a in tmp2:
            authors.append(a[1])
        x = {"doi": u[3], "institution": u[1], "reaction": u[0], "contributors": authors}
        side_effects.append(x)
    return side_effects


def list_users_db():
    stmt = 'SELECT * FROM users'
    with connection.cursor() as cursor:
        cursor.execute(stmt)
        tmp = cursor.fetchall()
        users = []
        for u in tmp:
            x = {"username": u[0], "institution": u[1]}
            users.append(x)
        return users


def get_same_drug_proteins_db():
    stmt = 'select drug, count(protein) from binds_to left join undergoes u on binds_to.reaction = u.reaction group by drug having count(protein) > 1'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for u in tmp:
        drugs.append(u[0])

    drugs_list = []
    for d in drugs:
        stmt = 'select uniprot_id, protein_name from binds_to left join undergoes u on binds_to.reaction = u.reaction left join protein p on p.uniprot_id = binds_to.protein where drug = "{}"'.format(
            d)
        cursor = connection.cursor()
        cursor.execute(stmt)
        tmp = cursor.fetchall()
        x = {}
        y = []
        for p in tmp:
            y.append({"uniprot_id": p[0], "protein_name": p[1]})
        x = {"drug": d, "proteins": y}
        drugs_list.append(x)
    return drugs_list


def filter_by_keyword_db(keyword):
    stmt = "select drugbank_id from drugs where description like '%{}%'".format(keyword)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for d in tmp:
        drugs.append(d[0])
    return drugs


def least_side_effect_db(uniprot_id):
    stmt = "select u.drug from binds_to left join undergoes u on binds_to.reaction = u.reaction left join causes c on u.drug = c.drug where protein = '{}' group by u.drug order by count(side_effect)".format(
        uniprot_id)
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    drugs = []
    for d in tmp:
        drugs.append(d[0])
    return drugs


def rank_institutes_db():
    stmt = "select * from institute order by score desc"
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    ranks = []
    for r in tmp:
        ranks.append({"institute_name": r[0], "score": r[1]})
    return ranks
def dt_interactions():
    query = """
    select drugbank_id, drug_name, uniprot_id, protein_name from drugs
    inner join undergoes u on drugs.drugbank_id = u.drug
    inner join binds_to bt on u.reaction = bt.reaction
    inner join protein p on bt.protein = p.uniprot_id
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        tmp = cursor.fetchall()
        ids = [i[0] + ", " + i[1] for i in tmp]
        ids = list(set(ids))
        drug_ints = []
        for id_ in ids:
            id_wo_name = id_.split(',')[0]
            filtered_proteins = []
            for i in tmp:
                if i[0] == id_wo_name:
                    filtered_proteins.append(i[2] + ", " + i[3])
            drug_ints.append([id_, filtered_proteins])
        print(drug_ints)
        return drug_ints
