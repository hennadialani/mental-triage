import re
text = 'Sentence 0 has a sentiment score of 0.8 Sentence 1 has a sentiment score of 0.9 Sentence 2 has a sentiment score of 0.8 Sentence 3 has a sentiment score of 0.2 Sentence 4 has a sentiment score of 0.1 Sentence 5 has a sentiment score of 0.4 Sentence 6 has a sentiment score of 0.3 Sentence 7 has a sentiment score of 0.4 Sentence 8 has a sentiment score of 0.2 Sentence 9 has a sentiment score of 0.9 Overall Sentiment: score of 0.5 with magnitude of 5.5'
sentiment_scores = re.findall('score of [0-9].[0-9]', text)
sentiment_scores = [w[-3:] for w in sentiment_scores]
sentence_no = re.findall('Sentence \d', text)
sentence_no = [w[-1:] for w in sentence_no]
overall_sentiment = re.findall('Sentiment: score of [0-9].[0-9]', text)
overall_sentiment = [w[-3:] for w in overall_sentiment]
overall_sentiment = overall_sentiment*len(sentence_no)
print(overall_sentiment == ['0.5']*len(sentence_no))
