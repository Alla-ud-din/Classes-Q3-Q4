from fastapi_helloworld import main
from fastapi.testclient import TestClient
from fastapi_helloworld.main import app


def test_function1():
    r = main.first_funtion()
    assert r == "Hello world"

def test_function2():
    r= main.first_funtion()
    assert r != "Pakistan"



def test_root_path():
    client = TestClient(app = app)
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}