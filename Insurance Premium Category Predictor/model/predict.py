import pickle
import pandas as pd 

#import the ml model 
with open('model/model.pkl','rb') as f:  #* rb--> read binary
    model = pickle.load(f)

#! Always show the model version 
MODEL_VERSION = '1.0.0'

#get class labels form model (important for matching probabilities to class names)
class_labels= model.classes.tolist()

def predict_output(user_input: dict):

    input_df = pd.DataFrame([user_input])   #convert the dict to dataframe--> need to pass data in a list for dataframe 

    output = model.predict(input_df)[0]
    return output