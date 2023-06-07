import random
import string

def generate_unique_username(existing_usernames):
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    while username in existing_usernames:
        username = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return username

def generate_unique_email(existing_emails):
    email = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + '@email213.com'
    while email in existing_emails:
        email = ''.join(random.choice(string.ascii_lowercase) for _ in range(6)) + '@email213.com'
    return email

def generate_admin_list():
    admin_list = []
    existing_usernames = set()
    existing_emails = set()

    for _ in range(10000):
        username = generate_unique_username(existing_usernames)
        email = generate_unique_email(existing_emails)

        user_dict = {
            "username": username,
            "email": email,
            "first_name": "kev",
            "last_name": "kim",
            "phonenumber": "254758202697",
            "gender": "Male",
            "DOB": "2013-12-12",
            "password": "12345678",
            "confirm_password": "12345678",
            "user_type": "admin",
            "tenant_id": "1"
        }

        existing_usernames.add(username)
        existing_emails.add(email)

        admin_list.append(user_dict)

    return admin_list

def generate_client_list():
    client_list = []
    existing_usernames = set()
    existing_emails = set()

    for _ in range(10000):
        username = generate_unique_username(existing_usernames)
        email = generate_unique_email(existing_emails)

        user_dict = {
            "username": username,
            "email": email,
            "first_name": "kev",
            "last_name": "kim",
            "phonenumber": "254758202697",
            "gender": "Male",
            "DOB": "2013-12-12",
            "password": "12345678",
            "confirm_password": "12345678",
            "user_type": "client",
        }

        existing_usernames.add(username)
        existing_emails.add(email)

        client_list.append(user_dict)

    return client_list

def generate_employee_list():
    tenant_list = []
    existing_usernames = set()
    existing_emails = set()

    for _ in range(10000):
        username = generate_unique_username(existing_usernames)
        email = generate_unique_email(existing_emails)

        user_dict = {
            "username": username,
            "email": email,
            "first_name": "kev",
            "last_name": "kim",
            "phonenumber": "254758202697",
            "gender": "Male",
            "DOB": "2013-12-12",
            "password": "12345678",
            "confirm_password": "12345678",
            "user_type": "client",
            "tenant_id": "1"
        }

        existing_usernames.add(username)
        existing_emails.add(email)

        tenant_list.append(user_dict)

    return tenant_list