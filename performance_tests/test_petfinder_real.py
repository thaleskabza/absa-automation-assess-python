from locust import HttpUser, task, between


CLIENT_ID = "gbfuckDsPVmzzxskuQpgdeQ5tvZYX6NTa9vFszNJLkg8oTeQOK"
CLIENT_SECRET = "Y0E5cR6pNrzJinSZuvFlSVDws5NZINH4OdkJtK0d"

class PetfinderUser(HttpUser):
    host = "https://api.petfinder.com"
    wait_time = between(1, 3)

    def on_start(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = self.client.post("/v2/oauth2/token", data=data, headers=headers)
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            self.token = None

    @task
    def fetch_animals(self):
        if not self.token:
            return
        headers = {"Authorization": f"Bearer {self.token}"}
        with self.client.get("/v2/animals", headers=headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Status code {response.status_code}")
                return
            try:
                data = response.json()
            except ValueError:
                response.failure("Invalid JSON")
                return
            invalid = False
            for animal in data.get("animals", []):
                for field in ["id", "organization_id", "type", "species", "breeds", "age", "gender", "status", "contact"]:
                    if not animal.get(field):
                        invalid = True
                        break
                if invalid:
                    break
            if invalid:
                response.failure("Validation failed")
