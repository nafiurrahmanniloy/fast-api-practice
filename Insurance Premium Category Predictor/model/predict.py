import pickle
import pandas as pd 

#import the ml model 
with open('model/model.pkl','rb') as f:  #* rb--> read binary
    model = pickle.load(f)

#! Always show the model version 
MODEL_VERSION = '1.0.0'

#get class labels form model (important for matching probabilities to class names:: names are high, medium and low)
class_labels= model.classes_.tolist()

def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])   #convert the dict to dataframe--> need to pass data in a list for dataframe 

    predicted_class = model.predict(input_df)[0]

    #* get the probabilities for all classes 
    probabilities = model.predict_proba(input_df)[0]
    confidence =max(probabilities)
    
    #create dict to map the classes
    class_probs =dict(zip(class_labels,map(lambda p: round(p,4),probabilities)))

    
#added confidence score in api
    return {
        'predicted_catagory': predicted_class,
        'confidence': round(confidence,4),
        'class_probabilities': class_probs
    }