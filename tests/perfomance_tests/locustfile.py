from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def home(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/show_summary", {"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")

    @task
    def purchasePlaces(self):
        self.client.post("/purchase_places", {"competition": "Spring Festival",
                                             "club": "Simply Lift",
                                             "places": "1"})

    @task
    def points(self):
        self.client.get("/points")

    @task
    def clubReservation(self):
        self.client.get("/reservation/Spring%20Festival")
        

    @task
    def logout(self):
        self.client.get("/logout")
