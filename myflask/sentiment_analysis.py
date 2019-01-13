import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
# [END language_sentiment_tutorial_imports]


# [START language_sentiment_tutorial_print_result]
def create_ouput(annotations):
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    file = open("result.txt", "w") 
    for index, sentence in enumerate(annotations.sentences):
        sentence_sentiment = sentence.sentiment.score
        file.write('Sentence {} has a sentiment score of {}'.format(
            index, sentence_sentiment))

    file.write('Overall Sentiment: score of {} with magnitude of {}'.format(
        score, magnitude))
    file.close() 
    return 0
# [END language_sentiment_tutorial_print_result]


# [START language_sentiment_tutorial_analyze_sentiment]
def analyze(file):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(file, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    create_ouput(annotations)
# [END language_sentiment_tutorial_analyze_sentiment]


# [START language_sentiment_tutorial_run_application]
if __name__ == '__main__':

    analyze("transcription.txt")