from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather, Record
import time

app = Flask(__name__)
timeSinceRecordingStart = 0


@app.route("/intro", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    
    #resp.say("What to say?", voice="alice")
    #resp.record(action="/process",timeout = 5,transcribe = True, transcribeCallback = "/transcribeOutput", playBeep = False)
    gath = Gather(partialResultCallback = "/partial", input = "speech", method = "GET")
    gath.say("Recording 1 start!", voice="alice")
    resp.append(gath)

    resp.say("Sorry, I didn't get that. Please try calling again", voice = "alice")
    timeSinceRecordingStart = time.time()
    return str(resp)

@app.route("/partial", methods=['GET', 'POST'])
def tranOut():
    resp = VoiceResponse()
    if time.time() - timeSinceRecordingStart >= 10:
        txt = request.args.get("UnstableSpeechResult")
        timeSinceRecordingStart += 10
        #write txt to file
        #with open("transription.txt","w") as newfile:
        #    newfile.write(txt)
        #    newfile.close()

    return str(resp)

@app.route("/process", methods=['GET', 'POST'])
def proc():
    resp = VoiceResponse()
    mySpeech = request.args.get("SpeechResult")
    print(mySpeech)
    resp.say("Thank you for sharing your feelings. A mental health professional will review your call.", voice='alice')
    resp.hangup()
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
