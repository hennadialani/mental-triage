from say2 import txt
from google.cloud import language
from google.cloud.language import enums
import six

def sample_analyze_sentiment(content):

    client = language.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    print('Score: {}'.format(sentiment.score))
    print('Magnitude: {}'.format(sentiment.magnitude))

if __name__=="__main__":
    sample_analyze_sentiment("you are bad and bad and bad and not be trusted!")