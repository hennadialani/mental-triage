from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather, Record
import six
import time

import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

app = Flask(__name__)

#txt = ""
currentUsers = {}
idMaker = 0


@app.route("/intro", methods=['GET', 'POST'])
def voice():
    pasttime = time.time()
    global idMaker
    idMaker += 1
    myId = idMaker
    print("Responding to caller with ID "+str(myId))
    global currentUsers
    currentUsers[myId] = time.time()
    print(currentUsers)
    resp = VoiceResponse()
    gath = Gather(action = "/process/"+str(myId), input = "speech", method = "POST", partialResultCallback=("/partialTranOut/"+str(myId)), partialResultCallbackMethod="POST")
    gath.say("What to say?", voice="alice")
    resp.append(gath)
    #resp.say("What to say?", voice="alice")
    #resp.record(action="/process",timeout = 5,transcribe = True, transcribeCallback = "/transcribeOutput", playBeep = False)
    #resp.say("Sorry, I didn't get that. Please try calling again", voice = "alice")
    return str(resp)

@app.route("/partialTranOut/<int:myId>", methods=['POST'])
def pTranOut(myId):
    global currentUsers
    client = language.LanguageServiceClient()
    resp = VoiceResponse()
    if time.time() - currentUsers[myId] >= 10:
        currentUsers[myId] += 10
        txt = request.form.get("UnstableSpeechResult")
        print(txt)
        document = types.Document(
            content=txt,
            type=enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        magnitude = annotations.document_sentiment.magnitude
            #write txt to file
        file = open("result.txt", "w") 
        for index, sentence in enumerate(annotations.sentences):
            sentence_sentiment = sentence.sentiment.score
            file.write('Sentence {} has a sentiment score of {}'.format(
                index, sentence_sentiment))

        file.write('Overall Sentiment: score of {} with magnitude of {}'.format(
            score, magnitude))
        file.close() 

    return str(resp)

'''@app.route("/transcribeOutput", methods=['POST'])
def tranOut():
    resp = VoiceResponse()
    if request.form.get("TranscriptionStatus") == "completed":
        txt = request.form.get("TranscriptionText")
        print(txt)
        recUrl = request.form.get("RecordingUrl")
        print(recUrl)
        #write txt to file
        with open("full-transcription.txt","w+") as newfile:
            newfile.write(txt)

    return str(resp)'''

@app.route("/process/<int:myId>", methods=['POST'])
def proc(myId):
    global currentUsers
    del currentUsers[myId]
    resp = VoiceResponse()
    txt = request.form.get("SpeechResult")
    print(txt)
    #write txt to file
    with open("full-transcription-"+str(myId)+".txt","w+") as newfile:
        newfile.write(txt)
    #print(mySpeech)
    resp.say("Thank you for sharing your feelings. A mental health professional will review your call.", voice='alice')
    resp.hangup()
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
