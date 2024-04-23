from fastapi_helloworld import main
def test_function1():
    r = main.first_funtion()
    assert r == "Hello world"

def test_function2():
    r= main.first_funtion()
    assert r != "Pakistan"