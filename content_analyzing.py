import nltk

from time_aligning import aligning_content
from content_features import content_features_extraction
import pandas as pd

lecture_content = aligning_content()
print(lecture_content['bigrams'])

features_for_topic = content_features_extraction()
# print(features_for_topic[0])

# def extract_sentences(content):
#
#
# basic_lecture_content = aligning_content()
# bigrams_for_sentence = list(nltk.bigrams(basic_lecture_content))
#
# content_sentences = pd.DataFrame(columns=['start', 'end', 'topic', 'content', 'images'])
# # content_sentences = pd.DataFrame(columns=['start', 'content'])
# content_sentences['start'] = lecture_content['start']
# content_sentences['end'] = lecture_content['end']
# content_sentences['topic'] = lecture_content['topic']
# content_sentences['content'] = lecture_content['content'].apply(lambda content: extract_sentences(content))
# content_sentences['images'] = lecture_content['images']
# print(content_sentences['content'])
# print(content_sentences)
