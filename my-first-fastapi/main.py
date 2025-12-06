from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,computed_field
from typing import Annotated,Literal, Optional
import json

app = FastAPI()
 
#----------------------model to create patient-------------------

class Patient(BaseModel):
    id: Annotated[str, Field(...,description='ID of the patient',examples=['P001'])]
    name: Annotated[str, Field(...,description='Name of the paitent')]
    city: Annotated[str,Field(...,description='city where the patient from')]
    age: Annotated[int,Field(..., gt=0,lt=100,description='Age of the patient')]
    gender: Annotated[str,Literal['male','female','others'],Field(...,description='Gender of the patient')]  #Literal is used here to give options to the user
    height: Annotated[float,Field(...,gt=0,description='height of the patient in mtrs')]
    weight: Annotated[float,Field(...,gt=0,description='weight of the patient in kgs')]
    
    
    #calculate bmi 
    @computed_field
    @property
    def bmi(self)->float:
        bmi =round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)-> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi< 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'
        
#--------------------Model to update patient--------------------------

class update_patient(BaseModel): 
    #if use optinal then must give default value.
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=100)]
    gender: Annotated[Optional[Literal['male', 'female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
    
    
#------------------------------------------------------------------------

def load_data(): #laod the json file data
    with open('data.json', 'r') as f:  #'r'-->read mode || with --> is used to automatically open and close the file.
        data= json.load(f)
    return data    
    
def save_data(data):
    with open('data.json','w') as f:
        json.dump(data,f)
        
 #-----------------------------------------------------------------------       
        
@app.get("/")  # @app.--> this is route
def hello():
    return {'message':'Pataient Management Syatem API'}

@app.get("/about")
def about():
    return {'message': 'Fully functional api to manage patient records'}

#--------------------------retrive patient-->form db-------------------------------------------

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

#------------------------create patient---> pydantic will be used here to validate data ------------------------------

@app.post('/create')

def create_patient(patient: Patient):
    
    #load the exesting data 
    data=load_data()
    
    #check if the patient_id already in the db
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    #add new patient to the db with the key:: patient id 
    data[patient.id]= patient.model_dump(exclude=['id'])
    
    
    #save the data in the db(json file)
    save_data(data)
    return JSONResponse(status_code=201,content={'message': 'patient created successfully'})  #JSONResponse used to give user message that the data is inserted 

#-----------update patient data-----------------
@app.put('/edit/{patient_id}')  #patient_id will go as path parameter
def update_patient(patient_id,patientUpdate: update_patient):
    
    #load current data
    data= load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient not found')
    
    existing_patient_data = data[patient_id] #extract patient data 
    
    #convert pydantic obj to dict so that data can be updated
    updated_patient_data = patientUpdate.model_dump(exclude_unset=True)  #only return updated fields::will not return unset fields with ::**exclude_unset=True**
    
    #run a loop on updated patient info in existing_patient_data
    for key,value in updated_patient_data.items():   #key, value as for dic---> {'key':'value'}
        existing_patient_data[key]=value
    
    
    