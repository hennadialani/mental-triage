import dash
import dash_core_components as dcc
import dash_html_components as html
import re
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

text = 'Sentence 0 has a sentiment score of 0.8 Sentence 1 has a sentiment score of 0.9 Sentence 2 has a sentiment score of 0.8 Sentence 3 has a sentiment score of 0.2 Sentence 4 has a sentiment score of 0.1 Sentence 5 has a sentiment score of 0.4 Sentence 6 has a sentiment score of 0.3 Sentence 7 has a sentiment score of 0.4 Sentence 8 has a sentiment score of 0.2 Sentence 9 has a sentiment score of 0.9'
sentiment_scores = re.findall('score of [0-9].[0-9]', text)
sentiment_scores = [w[-3:] for w in sentiment_scores]
sentence_no = re.findall('Sentence \d', text)
sentence_no = [w[-1:] for w in sentence_no]
overall_sentiment = re.findall('Sentiment: score of [0-9].[0-9]', text)
#overall_sentiment = [w[-3:] for w in overall_sentiment]
#overall_sentiment = overall_sentiment*len(sentence_no)
#overall_sentiment
overall_sentiment = ['0.5']*len(sentence_no) #struggling to make the commented code a horizontal line :(

app.layout = html.Div(children=[
    html.H1(children='Mental Triage',
        style={
            'textAlign': 'center',
            'font-family': 'sans-serif',
            'images':[dict(
        source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
        xref="paper", yref="paper",
        x=1, y=1.05,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom"
      )]
        }),
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
                {'x': sentence_no, 'y': overall_sentiment, 'type': 'line', 'name': 'Overall sentiment'}
            ],
            'layout': {
                'title': 'Sentiment Analyzed Over Call',
                'xaxis': {'title': 'Sentence Number'},
                'yaxis': {'title': 'Sentiment Score'}
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
