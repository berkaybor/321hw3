from django.db import connection


def edit_reaction_affinity(reaction_id, affinity):
    query = "update reaction set affinity {} where reaction_id = '{}'".format(affinity, reaction_id)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'Update failed'

        return