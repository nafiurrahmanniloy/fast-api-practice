from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import model,MODEL_VERSION,predict_output
from schema.user_input import UserInput


app = FastAPI()

@app.get('/')    
def home():
    return{'message':'Insurance Premium Prediction API'}   


#! Always---------------->need this endpoint when deploy api-->Always cloud services will check this endpoint 
#! machine readable
@app.get('/health')
def health_check():
    return{
        'status': 'OK',
        'version': 'MODEL_VERSION',
        'model_loaded': model is not None  #this returns true if the model is loaded
            
    }


@app.post('/predict')
def predict_premium(data: UserInput):  #data will come from request body-->   Lets say :: data is an obj of UserInput class

    user_input = {     #! creating a dict to pass data to the ml model which is in predict_output function;
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }


    try:

        prediction= predict_output(user_input) #this is the predicted value from the model 

        #now pass the data as json to the output 
        return JSONResponse(status_code=200,content={'predicted_catagory': prediction})
    
    except Exception as e:
        
        JSONResponse(status_code=500,content=str(e))




