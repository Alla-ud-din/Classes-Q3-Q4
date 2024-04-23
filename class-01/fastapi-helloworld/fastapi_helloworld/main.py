from fastapi import FastAPI
def first_funtion()->str:
    return "Hello world"
print(first_funtion())
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/city')
def city():
    return {"city": "Lahore"}


@app.get("/piaic/")
def piaic():
    return {"organization": "piaic"}


