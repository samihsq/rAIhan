import http.client
import json, time
import random
import csv
from textblob.classifiers import NaiveBayesClassifier
from config import getCreds, getCompliments, getScope, getMisc

train = [
     ('I love this sandwich.', 'pos'),
     ('this is an amazing place!', 'pos'),
     ('I feel very good about these beers.', 'pos'),
     ('this is my best work.', 'pos'),
     ("what an awesome view", 'pos'),
     ('I do not like this restaurant', 'neg'),
     ('I am tired of this stuff.', 'neg'),
     ("I can't deal with this", 'neg'),
     ('he is my sworn enemy!', 'neg'),
     ('my boss is horrible.', 'neg')
 ]
cl = NaiveBayesClassifier(train)
conn = http.client.HTTPSConnection("discord.com")
username, password = getCreds()
payload = "{\"login\":\"" + username + "\",\"password\":\"" + password + "\"}"

headers = {
    'cookie': "__cfduid=d34b9649242049e3c95e9737b41c2bf4d1619142338; __dcfduid=327cde81d8964a30887a3d3d92b55dbf",
    'Content-Type': "application/json"
}

conn.request("POST", "/api/v9/auth/login", payload, headers)

res = conn.getresponse()
data = res.read()

daToken = json.loads(data.decode("utf-8"))["token"]
daCount = 0
daComplimentList = getCompliments()
reactTo, channelIDtoMsg, daGuildID = getScope()
msgAsReply = getMisc()


def createCompliment():
    #reactions = []

    '''sum = emotion["Happy"] + emotion["Angry"] + emotion["Surprise"] + emotion["Sad"] + emotion["Fear"]
    if sum > 0:
        filter = dict()
        for key, value in emotion.items():
            if value != 0:
                filter[key] = value
        with open("FilteredCSVFiles/" + str(list(filter)[0]) + ".csv", "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                reactions.append(row[0])'''
    daMessage = ""  # "bre, you really said " + daMessageContent
    #daMessage += reactions[random.randint(0, len(reactions)) - 1]
    print(daMessageContent + ": " + list(filter)[0] + " -> " + daMessage)
    #print(emotion)
    # print(newemotion.prob("pos"))
    return daMessage
    #else:
        #return ""
    #del reactions[:]


while True:
    for channelID in list(channelIDtoMsg.keys()):
        conn = http.client.HTTPSConnection("discord.com")
        payload = ""

        headers = {
            'cookie': "__cfduid=d34b9649242049e3c95e9737b41c2bf4d1619142338; __dcfduid=327cde81d8964a30887a3d3d92b55dbf",
            'authorization': daToken,
            'Content-Type': "application/json"
        }

        conn.request("GET", "/api/v9/channels/" + channelID + "/messages", payload, headers)

        res = conn.getresponse()
        data = res.read()
        if json.loads(data.decode("utf-8"))[0] != channelIDtoMsg[channelID]:
            daMessageID = json.loads(data.decode("utf-8"))[0]["id"]
            daMessageContent = json.loads(data.decode("utf-8"))[0]["content"]
            # emotion = te.get_emotion(daMessageContent)
            # newemotion = cl.prob_classify(daMessageContent)
            # print(json.loads(data.decode("utf-8"))[0])
            channelIDtoMsg[channelID] = json.loads(data.decode("utf-8"))[0]
            if channelIDtoMsg[channelID]["author"]["id"] != reactTo:
                # print(daMessageID)
                if msgAsReply == True:
                    payload = "{\"content\": \"" + createCompliment() + "\",\n\"nonce\": " + str(
                        daCount) + ",\n\"tts\": false,\n\"message_reference\": {\"channel_id\": \"" + str(
                        channelID) + "\",\n\"guild_id\":\"" + str(daGuildID) + "\", \n \"message_id\": \"" + str(
                        daMessageID) + "\"}\n}"
                else:
                    payload = "{\"content\": \"" + createCompliment() + "\",\n\"nonce\": " + str(
                        daCount) + ",\n\"tts\": false}"
                # print("Payload:"+payload)
                payload = payload.encode(encoding='utf-8')
                conn.request("POST", "/api/v9/channels/" + channelID + "/messages", payload, headers)
                daCount += 1
    time.sleep(.25)
