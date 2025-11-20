from fastapi import FastAPI, Path
import json

app = FastAPI()
 

def load_data(): #laod the json file data
    with open('data.json', 'r') as f:  #'r'-->read mode || with --> is used to automatically open and close the file.
        data= json.load(f)
    return data    
    

@app.get("/")  # @app.--> this is route
def hello():
    return {'message':'Pataient Management Syatem API'}

@app.get("/about")
def about():
    return {'message': 'Fully functional api to manage patient records'}

@app.get("/view")
def view():
    data =load_data()
    
    return data

@app.get('/patient/{patient_id}')  #dynamic path parameter 
def view_patient(patient_id: str = Path(..., description= 'Id of the patient in the DB', example="P001")):
    data =load_data()
    
    if patient_id in data:
        return data[patient_id]
    return {'error': 'patient not found'}
   