from locust import HttpLocust, TaskSet, task, between

class UserBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("auth/token/login/", {"username":"feeder", "password":"dummy123"})

    def logout(self):
        self.client.post("auth/token/logout/", auth=("feeder", "dummy123"))

    @task
    def view_avatar(self):
        self.client.get("account/avatar/", auth=("feeder", "dummy123"))

    @task
    def view_leaderboard(self):
        self.client.get("account/leaderboard/", auth=("feeder", "dummy123"))

    @task
    def lobby(self):
        self.client.get("game/expedition/", auth=("feeder", "dummy123"))

    @task
    def admin(self):
        self.client.get("admin")

    @task
    def index(self):
        self.client.get("")

    

class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)
    wait_time = between(5.0, 9.0)