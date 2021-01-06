For this code to work you need to have the following dependencies resolved.

You'll need to have the following modules and versions running in your machine-

-python 3.6
-flask 0.11
-chatterbot 0.8.4
-spacy
-tensorflow 1.14
-linecache

------------------------------------------------------

What has be done and how it can be run-

-I have manually used the raw dataset present inside the dataset folder as yml files for 3 diseases.  The "df_diseases.csv" contains the seriousness_index for these 3 diseases.
- The index.html code is present inside the templates folder. The css file 
is in the static folder.

-The model has already been trained using the code present in train.py so you'll simply need to run the run.py (If if place more yml files or change yml chats you can run train.py again to generate new db.sqlite3 file)

- Commands to run in terminal or cmd when you are in "chatbot" root folder are
python3 run.py
(OR first run python3 train.py) in case you want to train the chatbot again.

- file to execute the chatbot that I have created. It'll be displayed in the web browser in the address http://127.0.0.1:5000/

--------------------------------------------------------

What are the features?

-It is a very basic chatbot for doctor consultation.
-have sentiment analysis present in this chatbot.
-Also  has user profiles with previous conditions so that these can be used to predict the possible condition.
-The bot can understand phrases of 1 or more words. I have provided screenshots of many sample conversations.
- Predicts seriousness of the disease, like "You have the symptoms of Covid-19 virus with a probability of 82%. You should consult a doctor immediately."
-greeting messages response.
-closure goodbye response.

----------------------------------------------------------
