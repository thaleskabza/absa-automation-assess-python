### api_tests/test_petfinder_real.py
import pytest
import requests


CLIENT_ID = "1yIxd8HkNjV4ymqLi2GhaFFYOps9SrpEeT0cUWSSWwDAVHKxeF"
CLIENT_SECRET = "kih7OW7Q3yGiVK4i7Y33hEwsS24eEWRyiN6gaNMt"

@pytest.fixture(scope="session")
def token():
    if CLIENT_ID.startswith("YOUR") or CLIENT_SECRET.startswith("YOUR"):
        pytest.skip("Skipping real API tests: set CLIENT_ID and CLIENT_SECRET")
    url = "https://api.petfinder.com/v2/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    assert response.status_code == 200, f"Failed to fetch token: {response.status_code}"
    return response.json().get("access_token")


def test_fetch_types_verify_dog_exists(token):
    url = "https://api.petfinder.com/v2/types"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert any(t["name"] == "Dog" for t in data.get("types", []))


def test_fetch_breeds_and_search(token):
    breeds_url = "https://api.petfinder.com/v2/types/dog/breeds"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(breeds_url, headers=headers)
    assert response.status_code == 200
    breeds = response.json().get("breeds", [])
    assert breeds and len(breeds) > 0

    search_url = "https://api.petfinder.com/v2/animals"
    params = {"type": "dog", "breed": "Golden Retriever", "limit": 1}
    response = requests.get(search_url, params=params, headers=headers)
    assert response.status_code == 200
    animals = response.json().get("animals", [])
    assert animals and len(animals) > 0