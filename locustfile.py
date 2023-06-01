from locust import HttpUser, task, between
from locust_generators.users_generator import generate_admin_list, generate_client_list, generate_employee_list

class AppUser(HttpUser):
    wait_time = between(2, 5)

    # AUTH
    @task(3)
    def login(self):
        with self.client.post('/auth/signin/', json={'email': 'kim@email3.com', 'password': '123456789'}, catch_response=True) as response:
        # response = self.client.post('/auth/signin/', json={'email': 'kim@email3.com', 'password': '12345678'})
            if response.status_code != 200:
                response.failure('Failure')
            else:
                response.success()

    @task
    def register_admin(self):
        user_list = generate_admin_list()

        for user in user_list:
            with self.client.post('/auth/admin/', json=user, catch_response=True) as response:
                print(response)
                if response.status_code != 201:
                    response.failure('Error while creating an admin')
                else:
                    response.success()

    @task 
    def register_employee(self):
        user_list = generate_employee_list()

        for user in user_list:
            with self.client.post('/auth/employee/', json={user}, catch_response=True) as response:
                if response.status_code != 201:
                    response.failure('Error while creating an employee')
                else:
                    response.success()

    @task(2)
    def register_client(self):
        user_list = generate_client_list()

        for user in user_list:
            with self.client.post('/auth/client/', json=user, catch_response=True) as response:
                print(response)
                if response.status_code != 201:
                    response.failure('Error while creating a client')
                else:
                    response.success()