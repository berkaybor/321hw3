from django.db import connection


def check_credentials(name, institution, password):
    if name == "berkay" and institution == "boun" and password == 'qwer1234':
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

