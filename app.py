import dash
import dash_core_components as dcc
import dash_html_components as html
import re
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#text = 'Sentence 0 has a sentiment score of 0.8 Sentence 1 has a sentiment score of 0.9 Sentence 2 has a sentiment score of 0.8 Sentence 3 has a sentiment score of 0.2 Sentence 4 has a sentiment score of 0.1 Sentence 5 has a sentiment score of 0.4 Sentence 6 has a sentiment score of 0.3 Sentence 7 has a sentiment score of 0.4 Sentence 8 has a sentiment score of 0.2 Sentence 9 has a sentiment score of 0.9 Overall Sentiment: score of 0.5 with magnitude of 5.5'
text = open(“result.text”, “r”) 
text = text.read()
sentiment_scores = re.findall('score of [0-9].[0-9]', text)
sentiment_scores = [w[-3:] for w in sentiment_scores]
sentence_no = re.findall('Sentence \d', text)
sentence_no = [w[-1:] for w in sentence_no]
overall_sentiment = re.findall('Sentiment: score of [0-9].[0-9]', text)
overall_sentiment = [w[-3:] for w in overall_sentiment]
overall_sentiment = overall_sentiment*len(sentence_no)
magnitude = re.findall('magnitude of [0-9].[0-9]', text)
magnitude = [w[-3:] for w in overall_sentiment]
magnitude = magnitude*len(sentence_no)

app.layout = html.Div(children=[
    html.Div([
        html.Img(
            src='https://github.com/hennadialani/hennadialani.github.io/blob/master/MENTAL%20TRIAGE.png?raw=true',
            style={
                'height': '200px',
                'width': '200px'
            })
], style={'textAlign': 'center'}),
    html.Div(children='''
        An NLP assistant for therapists to determine urgency of psychological intervention after a patient's phone call. Mediates the ongoing mental health crisis on college campuses by analyzing sentiment from a person's response to a freeform question standard on psychological screening questionnaires.
    ''',
        style={
            'textAlign': 'center',
            'font-family': 'sans-serif'
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
                'xaxis': {'title': 'Sentence Number'},
                'yaxis': {'title': 'Sentiment Score'}
            }
        }
    ),
    html.Div([
        html.P('The overall sentiment score of this caller is '+overall_sentiment[1]+'. Meanwhile, the magnitude of this call indicates how much of the phone call was emotional, at '+magnitude[1]+'.', style={
            'textAlign': 'center',
            'font-family': 'sans-serif'
        })])
])

if __name__ == '__main__':
    app.run_server(debug=True)
