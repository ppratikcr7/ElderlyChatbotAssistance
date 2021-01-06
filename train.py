#=======================================================================
# Important imports
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
#=======================================================================


#=======================================================================
# Uncomment to train bot on new dataset and replace old database
# Skip if goal is to append to the older database
try:
    os.remove("db.sqlite3")
    print("Old database removed. Training new database")
except:
    print('No database found. Creating new database.')
#=======================================================================


#=======================================================================
# Training the bot
english_bot = ChatBot('Bot')
trainer = ListTrainer(english_bot)
for file in os.listdir('dataset'):
    print('Training using ' + file)
    convData = open('dataset/' + file).readlines()
    trainer.train(convData)
    print("Training completed for " + file)
#=======================================================================