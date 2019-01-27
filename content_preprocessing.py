import pandas as pd
import string
import re

from nltk import WordNetLemmatizer


# Removing punctuation
def removing_punctuation(content):
    punctuation_removed_content = "".join([word for word in content if word not in string.punctuation])
    return punctuation_removed_content


# Converting to lowercase and word tokenizing
def tokenize_into_words(content):
    tokens_lowercase = " ".join(x.lower() for x in content.split())
    tokens = re.split('\W+', tokens_lowercase)
    return tokens


# Lemmatizing
word_lemmatizer = WordNetLemmatizer()


def lemmatization(tokenized_words):
    lemmatized_text = [word_lemmatizer.lemmatize(word)for word in tokenized_words]
    return ' '.join(lemmatized_text)


# Applying pre-processing
def preprocessing_content(lecture_content):
    # df for text analyzing
    lecture_text = pd.DataFrame(columns=['start', 'end', 'topic', 'content', 'images'])
    lecture_text['start'] = lecture_content['start']
    lecture_text['end'] = lecture_content['end']
    lecture_text['images'] = lecture_content['images']

    lecture_text['topic'] = lecture_content['topic'].apply(lambda topic: removing_punctuation(topic))
    lecture_text['topic'] = lecture_text['topic'].apply(lambda topic: tokenize_into_words(topic))
    lecture_text['topic'] = lecture_text['topic'].apply(lambda topic: lemmatization(topic))

    lecture_text['content'] = lecture_content['content'].apply(lambda content: removing_punctuation(content))
    lecture_text['content'] = lecture_text['content'].apply(lambda content: tokenize_into_words(content))
    lecture_text['content'] = lecture_text['content'].apply(lambda content: lemmatization(content))

    # print(lecture_text['topic'])
    # print(lecture_text['content'])
    return lecture_text
