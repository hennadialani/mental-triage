from flask import Flask
from flask import request
from twilio.twiml.voice_response import VoiceResponse, Gather, Record
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import Flask, send_from_directory
from dash.dependencies import Input, Output

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
import six
import argparse


server = Flask(__name__)
app = dash.Dash(server=server)

txt = ""

@server.route("/intro", methods=['GET', 'POST'])
def voice():
    resp = VoiceResponse()
    #gath = Gather(action = "/part2", input = "speech", method = "GET")
    #gath.say("Recording 1 start!", voice="alice")
    #resp.append(gath)
    resp.say("Welcome to mental triage. How have you been feeling lately?", voice="alice")
    resp.record(action="/process",timeout = 5,transcribe = True, transcribeCallback = "/transcribeOutput", playBeep = False)
    resp.say("Sorry, I didn't get that. Please try calling again", voice = "alice")
    return str(resp)

@server.route("/transcribeOutput", methods=['POST'])
def tranOut():
    resp = VoiceResponse()
    if request.form.get("TranscriptionStatus") == "completed":
        txt = request.form.get("TranscriptionText")
        print(txt)
        recUrl = request.form.get("RecordingUrl")
        print(recUrl)
        client = language.LanguageServiceClient()
        document = types.Document(
            content=txt,
            type=enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        magnitude = annotations.document_sentiment.magnitude

        for index, sentence in enumerate(annotations.sentences):
            sentence_sentiment = sentence.sentiment.score
            answer += str('Sentence {} has a sentiment score of {}'.format(
                index, sentence_sentiment))


        sentence_no = re.findall('Sentence \d', )
        sentence_no = [w[-1:] for w in sentence_no]

        overall_sentiment = re.findall('Sentiment: score of [0-9].[0-9]', text)
        overall_sentiment = [w[-3:] for w in overall_sentiment]
        overall_sentiment = overall_sentiment*len(sentence_no)

    return str(resp)

@server.route("/process", methods=['POST'])
def proc():
    resp = VoiceResponse()
    mySpeech = request.args.get("SpeechResult")
    #print(mySpeech)
    resp.say("Thank you for sharing your feelings. A mental health professional will review your call.", voice='alice')
    resp.hangup()
    return str(resp)


app.layout = html.Div(children=[
    html.Div([
        html.Img(
            src='https://github.com/hennadialani/hennadialani.github.io/blob/master/MENTAL%20TRIAGE.png?raw=true',
            style={
                'height': '230px',
                'width': '230px'
            })
], style={'textAlign': 'center'}),
    html.Div(children='''
        An NLP assistant for therapists to determine urgency of psychological intervention after a patient's phone call. Mediates the ongoing mental health crisis on college campuses by analyzing sentiment from a person's response to a freeform question standard on psychological screening questionnaires.
    ''',
        style={
            'margin-top': '5px',
            'margin-bottom': '5px',
            'padding-left': '50px',
            'padding-right': '50px',
            'textAlign': 'center',
            'font-weight': 'bold',
            'font-family': 'sans-serif',
            'font-size': '20px',
            'color': 'white',
            'background-color': '#38B6FF'
        }),
##Different font - probably try font family
##Potentially something to show a phone number so that we can identify which patient this is
##Something to identify what magnitude means 
##Play with the colors of the lines 
##Maybe background color change
dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': sentence_no, 'y': sentiment_scores, 'type': 'line', 'name': 'Sentence sentiment', 'color': '#38B6FF'},
                {'x': sentence_no, 'y': overall_sentiment, 'type': 'line', 'name': 'Overall sentiment', }
            ],
            'layout': {
                'title': 'Sentiment Analyzed Over Call',
                'font-family': 'sans-serif',
                'font-weight': 'bold',
                'xaxis': {'title': 'Sentence Number','font-family': 'Trebuchet MS'},
                'yaxis': {'title': 'Sentiment Score','font-family': 'Trebuchet MS'}
            }
        }
    ),
    html.Div([
        html.P('The overall sentiment score of this caller is '+score+'. Meanwhile, the magnitude of this call indicates how much of the phone call was emotional, at '+magnitude+'.', style={
            'textAlign': 'center',
            'margin-top':'10px',
            'padding-top': '10px',
            'padding-bottom': '10px',
            'padding-left': '50px',
            'padding-right': '50px',
            'font-family': 'sans-serif',
            'font-size': '22px',
            'font-weight': 'bold',
            'color':'white',
            'background-color': '#38B6FF'

        })])
])

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
