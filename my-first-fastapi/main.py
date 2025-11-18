from fastapi import FastAPI
import json

app = FastAPI()


def load_data(): #laod the json file data
    with open('data.json', 'r') as f:  #'r'-->read mode || with --> is used to automatically open and close the file.
        data= json.load(f)
    return data    
    

@app.get("/")
def hello():
    return {'message':'Pataient Management Syatem API'}

@app.get("/about")
def about():
    return {'message': 'Fully functional api to manage patient records'}

@app. get("/view")
def view():
    data =load_data()
    
    return data
    