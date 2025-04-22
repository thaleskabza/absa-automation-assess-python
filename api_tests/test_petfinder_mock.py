import pytest
import requests
import requests_mock

# Mock responses
mockTypesResponse = {
    "types": [
        {"name": "Dog"},
        {"name": "Cat"},
        {"name": "Rabbit"}
    ]
}

mockBreedsResponse = {
    "breeds": [
        {"name": "Golden Retriever"},
        {"name": "Labrador Retriever"},
        {"name": "German Shepherd"}
    ]
}

mockAnimalsResponse = {
    "animals": [
        {"id": 76044953, "type": "Dog", "species": "Dog", "breeds": {"primary": "Rottweiler"}, "age": "Adult", "gender": "Male", "status": "adoptable", "name": "Duke"}
    ],
    "pagination": {"count_per_page": 20, "total_count": 284088, "current_page": 1, "total_pages": 14205}
}

@pytest.fixture(autouse=True)
def _mock_adapter(requests_mock):
    return requests_mock


def test_fetch_and_validate_animal_types():
    url = "https://api.petfinder.com/v2/types"
    requests_mock.get(url, json=mockTypesResponse, status_code=200)
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert any(t["name"] == "Dog" for t in data.get("types", []))


def test_fetch_and_validate_dog_breeds():
    url = "https://api.petfinder.com/v2/types/dog/breeds"
    requests_mock.get(url, json=mockBreedsResponse, status_code=200)
    response = requests.get(url)
    assert response.status_code == 200
    breeds = response.json().get("breeds", [])
    assert breeds and len(breeds) > 0


def test_search_for_animals_and_validate_response():
    url_pattern = "https://api.petfinder.com/v2/animals"
    requests_mock.get(f"{url_pattern}", json=mockAnimalsResponse, status_code=200)
    response = requests.get(url_pattern, params={"type": "dog", "breed": "Golden Retriever"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("animals") and len(data["animals"]) > 0
    assert data.get("pagination") is not None