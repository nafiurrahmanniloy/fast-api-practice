from fastapi import FastAPI, Path, HTTPException, Query
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

#code improvement 

@app.get('/patient/{patient_id}')  #dynamic path parameter 
def view_patient(patient_id: str = Path(..., description= 'Id of the patient in the DB', example="P001")):  #(...)--> requerd 
    data =load_data()
    
    if patient_id in data: 
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient not found')   #custom error message 
   
#query parameter(sort paitent by key 3 options and order=ASC or DESC)

@app.get('/sort')
def sort_patient(sort_by: str = Query(...,description='Sort on the basis of height,weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    
    valid_feilds = ['height', 'weight', 'bmi']
    
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400, detail=f'invalid felids. select from{valid_feilds}') #400-->bad request 
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order. select between asc and desc')
    
    data= load_data()
    
    sort_order = True if order=='desc' else False
    
    sorted_data=sorted(data.values(), key= lambda x: x.get(sort_by,0), reverse=sort_order) #sorting data
    
    return sorted_data