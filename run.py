#===================================================================================================
# Importing important libraries
from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import linecache
import random
import os
import re
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from textblob import TextBlob
import pandas as pd
import numpy as np
import os.path
import json

 #=========================================================
### 1. Data Preparation and Preprocessing #####
 #=========================================================
# Adding seriousness_index column of the diseases. As the data is not available, for the proof of concept we
# would take random seriousness_index as of now.

# read data:

df = pd.read_csv("df_diseases.csv", engine='python', encoding='utf-8', error_bad_lines=False)
#df.head()

df['name'] = df['name'].astype(str)
df["name"].replace(" ", "_")
df["name"].replace("/", "_")

df = df.replace(np.nan, 'Nothing', regex=True)
#df = df.drop("Unnamed: 0", axis = 1)
#df.head()

# appending a column with label of seriousness_index from 0-10

def label(row):
    random_val = random.randint(0,10)
    return random_val

df.loc[:, 'seriousness_index'] = df.apply(label, axis=1)
#df.head()
 #=========================================================
########## 2. Classification model: ################
 #=========================================================
# This is to get the severity of the disease and based on that suggest user multiple possibilities:
data = df[['name', 'seriousness_index']]
data.head()
#===================================================================================================


#===================================================================================================
# Saving initial conversation to the file
filenumber = int(os.listdir('saved_conversations')[-1])
filenumber = filenumber + 1
file = open('saved_conversations/' + str(filenumber), "w+")
file.write('bot : Hi! I am Dr. Bot. Can you please tell me your name?\n')
file.close()
#===================================================================================================


#===================================================================================================
# Declaring the app
app = Flask(__name__)
# Declaring the object for our learned bot
drbot = ChatBot('Bot',
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri='sqlite:///db.sqlite3',
                logic_adapters=[
                    {
                        'import_path': 'chatterbot.logic.BestMatch'

                    },

                ],
                trainer='chatterbot.trainers.ListTrainer')

#===================================================================================================

#===================================================================================================
# Initial comments to the user routing it to the web app


@app.route("/")
def home():
    return render_template("index.html")
#===================================================================================================


#===================================================================================================
# The function to match  bot response from list of possible responses
def is_phrase_in(phrase, text):
    match = re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None
    #print(match)
    return match

#===================================================================================================

#===================================================================================================
phrase_list = ["These are the symptoms of",
               "These might be the symptoms of", "These are symptoms of", "These are the sign of", "These might be sign of", "These might be symptoms of", "This is a symptom of "]
path_to_conversation = "saved_conversations/" + str(filenumber)

# routing the generated bot response to the web app and delivering  it to user
flag = 1
file = None
@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    userText1 = userText.lower()
    word_list = userText1.split()
    global flag
    global file
    global phrase_list
    global data
    # Checking with name keyword and giving customized greetings to the user
    #=========================================================
    if "name" in word_list:
        name = word_list[-1].upper()
         #=========================================================
        ###### 3. CREATE USER PROFILE FILE TO STORE PATIENTS DETAILS (Medical History) ######
         #=========================================================
        if(os.path.isfile(name.lower()+".txt")):
            file = open(name.lower()+".txt", "a")
        else:
            file = open(name.lower()+".txt", "+w")
            
        response1 = "Hi" + " " + name + " How are feeling?"
        
        response = response1
        
        flag = 1
        
    else:
        
        if(flag == 1):
            #=========================================================
            ######### 4. SENTIMENT ANLAYSIS ##############
            #=========================================================

            # Getting the sentiments of the user:
            blob = TextBlob(userText1)
            sentiment_val = blob.polarity

            # Deciding upon the reply based on user's sentiment value:
            if sentiment_val > 0.5:
                response1 = "You feel good with no symptoms but still want some precautionary measures?"
            elif sentiment_val > 0.1:
                response1 = "Well, you clearly have some symptoms, don't worry you just need rest and few medicines."
            elif sentiment_val < -0.5:
                response1 = "It seems you are not fine and have severe symptoms, I will help you out."
            else:
                response1 = "You seem to be very neutral about the health condition. I would like to know more to help you better."

        # Get reponse from our chatbot: (For the first response we would send a reply based on user's sentiment)
        # then we also append response to ask for more details:
        if(flag == 1):
            response = response1 + " " + str(drbot.get_response(userText))
            flag = 0
        else:
            response = str(drbot.get_response(userText))
            
    #=========================================================
    ###### 5. INTENT matching for proper response #############
    #=========================================================
    
    # Matching the response and giving final response for major classes like: Greetings, Thanking, Goodbye, etc.
    data_file = open('intents.json').read()
    intents = json.loads(data_file)

    
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if is_phrase_in(pattern, userText):
                tag = intent['tag']
                val = random.randint(0,2)
                response = intent['responses'][val]
                return response
                
    # Matching the response and giving customized final response for a disease detected
    punctuation_and_number = ["'"]
    punctuation_and_number1 = set('!"#$%&\()*+,-./:;<=>?@[\\]^_{|}~0123456789')
    punctuation_and_number.extend(punctuation_and_number1)
    
    for phrase in phrase_list:
        if is_phrase_in(phrase, response):
            #print("yes")
            line = linecache.getline(path_to_conversation, 3)
            name = line.split()[3].upper()
            print(name)
            disease = response.split(" ")[-1].lower()
            print(disease)
            
            # Remove punctuation marks:
            for i in punctuation_and_number:
                disease = disease.replace(i,"")
                
            # Save disease in user profile:
            file = open(name.lower()+".txt", "a")
            file.write("\n" + str(disease) + "\n")
             #=========================================================
            ####### 6. Seriousness_index ################
             #=========================================================
            # If we get a match of the disease name in the dataset we get it's seriousness_index
            # and find the probability:
            
            if(data[data['name'] == str(disease)].size != 0):
                print("yes")
                probability = str(data[data['name'] == str(disease)].seriousness_index[1] * 10)
            else:
                probability = '50'
                
            response = "Hey" + " " + name + "!" + " The symptoms you are experiencing may be of " + \
             str(disease) + " with a chance of " + \
               probability + \
              "%." + " " + "You may contact a Doctor.\n" + \
              "Do you have symptoms of any other patients also?"
    #=========================================================
    
    # Writing the conversation to a file
    appendfile = os.listdir('saved_conversations')[-1]
    appendfile = open('saved_conversations/' + str(filenumber), "a")
    appendfile.write('user : ' + userText + '\n')
    appendfile.write('bot : ' + response + '\n')
    appendfile.close()
    file.close()

    return response
    #===================================================================================================


# driver code
if __name__ == "__main__":
    app.run()