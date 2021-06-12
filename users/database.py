from django.db import connection


def check_credentials(name, institution, password):
    query = 'select * from users where username = "{}" and institution = "{}" and password = "{}"'.format(name, institution, password)
    with connection.cursor() as cursor:
        cursor.execute(query)
        tmp = cursor.fetchall()
        if tmp:
            return True
        return False

def check_credentials_db_manager(username, password):
    query = 'select * from database_managers where managerusername = "{}" and password = "{}"'.format(username, password)
    with connection.cursor() as cursor:
        cursor.execute(query)
        tmp = cursor.fetchall()
        if tmp:
            return True
        return False


def return_users():
    stmt = 'SELECT * FROM users;'
    cursor = connection.cursor()
    cursor.execute(stmt)
    tmp = cursor.fetchall()
    users = []
    for u in tmp:
        x = {"username":u[0], "institution":u[1], "password":u[2]}
        users.append(x)
    return users


def add_user_to_db(name, institution, password):
    query = "INSERT INTO users VALUES ('{}', '{}', '{}')".format(name, institution, password)
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
        except:
            return 'User creation failed: User exists or bad input'

        return
