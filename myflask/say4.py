from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather, Record
import six

app = Flask(__name__)

txt = ""

@app.route("/intro", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    #gath = Gather(action = "/part2", input = "speech", method = "GET")
    #gath.say("Recording 1 start!", voice="alice")
    #resp.append(gath)
    resp.say("What to say?", voice="alice")
    resp.record(action="/process",timeout = 5,transcribe = True, transcribeCallback = "/transcribeOutput", playBeep = False)
    resp.say("Sorry, I didn't get that. Please try calling again", voice = "alice")
    return str(resp)

@app.route("/transcribeOutput", methods=['POST'])
def tranOut():
    resp = VoiceResponse()
    if request.form.get("TranscriptionStatus") == "completed":
        txt = request.form.get("TranscriptionText")
        print(txt)
        recUrl = request.form.get("RecordingUrl")
        print(recUrl)
        #write txt to file
        with open("transcription.txt","w+") as newfile:
            newfile.write(txt)

    return str(resp)

@app.route("/process", methods=['POST'])
def proc():
    resp = VoiceResponse()
    mySpeech = request.args.get("SpeechResult")
    #print(mySpeech)
    resp.say("Thank you for sharing your feelings. A mental health professional will review your call.", voice='alice')
    resp.hangup()
    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
