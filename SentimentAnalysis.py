#import Monkey Learn
from monkeylearn import MonkeyLearn

#import pandas
import pandas as pd

#import JSON
import json

def sentiment_analysis(path):
    
    #My API Key
    ml = MonkeyLearn('YOUR API KEY')

    #import dataset
    dataset = pd.read_csv(path)
    
    #convert a specific column to list
    data = dataset['Comments'].tolist()   
    
    #Trained Model API Key
    model_id = 'YOUR API KEY'    
    
    #Model Result
    result = ml.classifiers.classify(model_id, data)  
    
    #variable declarations
    ncount=0
    pcount=0
    count=0
    
    #process the Monkey Learn result and get the count of positive, negative and neutral comments
    for i in range(0,len(result.body)):
        jtopy=json.dumps(result.body)  
        json_object = json.loads(jtopy) 
        value = json_object[i].get('classifications')      #access the classification value
        tag = value[0]['tag_name']      #access the tag_name value

        #count the number of negative comments
        if tag.lower() == 'negative':
            ncount+=1

        #count the number of positive comments
        elif tag.lower() == 'positive':
            pcount+=1

        #count the number of neutral comments
        else:
            count+=1
            
    #print the number of comments
    #print(ncount)   #positive comments
    #print(pcount)   #negative comments
    #print(count)    #neutral comments
    return [ncount, pcount, count]

#sentiment_analysis("Comments.csv")