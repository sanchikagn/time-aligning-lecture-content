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


topic_features = lecture_analyzing['topic'] = lecture_analyzing['topic'].apply(lambda topic: feature_extraction(topic))
content_features = lecture_analyzing['content'] = lecture_analyzing['content'].apply(lambda content:
                                                                                     feature_extraction(content))
print(topic_features)
