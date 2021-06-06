import sys
sys.path.insert(0, 'discAutoMsg/')

import discord_automessage as am
import time
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument
import random

channelID = "716140536095965194"

fillerwords = ["um", "wait", "one sec"]

nofallback = False
amTalking = False
startTime = -10000
saveUserID = 000000000000
while True:

    startingList = am.getMessages(channelID, 1)
    #print(startingList)
    startingText = startingList[0]['content']
    userID = int(startingList[0]['author']["id"])
    #print (userID)
    #print('')
    if userID == 849876188238839809 \
            or "https" in startingText \
            or 'bot' in startingList[0]['author'] \
            or not startingText\
            or startingText :
        if amTalking:
            endTime = time.time()
            timeDiff = endTime - startTime
            print(timeDiff)
            if timeDiff >= 15:
                am.sendMessage(channelID, "bruh donowall <@" + str(saveUserID) + ">")
                amTalking = False
        print("skip")

        pass

    else:
        #print(2)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'private_key.json'

        DIALOGFLOW_PROJECT_ID = 'raihan-dtlk'
        DIALOGFLOW_LANGUAGE_CODE = 'en'
        SESSION_ID = 'me'

        text_to_be_analyzed = startingText + " "

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = session_client.detect_intent(session=session, query_input=query_input)
        except InvalidArgument:
            raise

        print("Query text:", response.query_result.query_text)
        print("Detected intent:", response.query_result.intent.display_name)
        print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        print("Fulfillment text:", response.query_result.fulfillment_text)
        print("")



        chance = 95
        prob = 100 / chance
        fallback = random.randint(1, round(prob))
        if response.query_result.intent.display_name == "Default Fallback Intent" and (fallback == 1 or nofallback):
            print("no fallback")
            nofallback = True

        else:
            saveUserID = userID
            amTalking = True
            startTime = time.time()
            nofallback = False
            if am.filler(3):
                time.sleep(0.2)
                word = fillerwords[random.randint(0, len(fillerwords) - 1)]
                am.sendMessage(channelID, word)
                print(3)
            time.sleep(float(random.randrange(50, 200))/100)

            am.sendMessage(channelID, response.query_result.fulfillment_text)
            #print(4)
            if response.query_result.fulfillment_text == "cant, gtg":
                time.sleep(300)
                am.sendMessage(channelID, "k im back <@" + str(saveUserID) + ">")

    time.sleep(0.5)