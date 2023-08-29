from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return{"response":"hellow"}


@app.get("/predcit_move")
def predict(input_dict):
    return
