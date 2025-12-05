# ---- Nested model is someting like use a pydantic model as a field to an other model then it is called nested-model
# ---- it is kindda like structure as I learend in webtech

    
    # Why use nested models:
    
# ---- Better organization of related data
# ---- Reuserable 
# ---- Automitacally validated 

from pydantic import BaseModel

class address(BaseModel):
    road:str
    city: str
    postalcode: str

class patient(BaseModel):
    
    name: str
    gender: str
    age: int 
    address: address       #address is it self a complex data
    

address_dict = {'road': 'Badda','city':'Dhaka', 'postalcode': '2200'}  

#the pydantic obj

address1 = address(**address_dict)

patient_dict ={
    'name': 'Niloy',
    'gender': 'Male',
    'age': 22,
    'address': address1
}

patient1 = patient(**patient_dict)

print(patient1)
print(patient1.name)
print(patient1.address.city)