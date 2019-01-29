import nltk

from content_preprocessing import preprocessing_content
from time_aligning import aligning_content


# Topic-wise content
basic_lecture_content = aligning_content()
# print(basic_lecture_content)

# Pre-processing content
lecture_analyzing = preprocessing_content(basic_lecture_content)
# print(lecture_analyzing['content'])


# Extracting features i.e. n-grams in each topic
def feature_extraction(preprocessed_text):
    bigrams = []
    unigrams_lists = []
    # adding end of and start of a message
    # msg = '<s> ' +msg + ' </s>'
    unigrams_lists.append(preprocessed_text.split())
    unigrams = [uni_list for sub_list in unigrams_lists for uni_list in sub_list]
    bigrams.extend(nltk.bigrams(unigrams))
    return bigrams


# removing bigrams only with stop words
stopwords = nltk.corpus.stopwords.words('english')


def filter_stopwords_bigrams(bigram_list):
    filtered_bigrams = []
    for bigram in bigram_list:
        if bigram[0] in stopwords and bigram[1] in stopwords:
            continue
        # if an integer
        elif (bigram[0] == '1') or (bigram[0] == '0'):
            continue
        elif bigram[0] == bigram[1]:
            # print(bigram)
            continue
        filtered_bigrams.append(bigram)
    return filtered_bigrams


# Acquiring frequencies of features
def bigram_feature_frequency(bigrams):
    # features frequencies
    bigram_frequency = nltk.FreqDist(bigrams)
    return bigram_frequency


topic_features = lecture_analyzing['topic'].apply(lambda topic: feature_extraction(topic))
if topic_features is not None:
    topic_features = topic_features.apply(lambda topic: filter_stopwords_bigrams(topic))
# topic_frequency = topic_features.apply(lambda bigrams: bigram_feature_frequency(bigrams))

content_features = lecture_analyzing['content'].apply(lambda content: feature_extraction(content))
if content_features is not None:
    content_features = content_features.apply(lambda bigrams: filter_stopwords_bigrams(bigrams))
content_frequency = content_features.apply(lambda bigrams: bigram_feature_frequency(bigrams))

# print(topic_frequency)
print(content_frequency)

