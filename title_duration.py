import pandas as pd
from itertools import islice


def converting_to_topic_classes():
    lecture_titles = pd.read_csv('resources/lecture_1_titles.csv', sep=',', header=None, names=['time', 'text'])
    # print("Input data has {} rows and {} columns".format(len(lecture_titles), len(lecture_titles.columns)))
    # print(lecture_titles.info())

    title_duration = pd.DataFrame(columns=['start', 'end', 'text'])

    start_time = lecture_titles['time'].iloc[0]
    topic = lecture_titles['text'].iloc[0]
    # start time in seconds
    start = int(start_time[1:3]) * 60 + int(start_time[4:6]) * 1000
    # print(start)
    for index, column in islice(lecture_titles.iterrows(), 1, None):
        time = (int(column[0][1:3]) * 60 + int(column[0][4:6])) * 1000
        # time in seconds
        end = time
        # creating topic categories
        title_duration = title_duration.append({'start': start, 'end': end, 'text': topic}, ignore_index=True)
        topic = column[1]
        start = time

    title_duration_sorted = title_duration.sort_values(by=['start'])
    # print("Input data has {} rows and {} columns".format(len(title_duration_sorted),
    #                                                      len(title_duration_sorted.columns)))
    # print(title_duration_sorted.info())
    # print(title_duration.sort_values(by=['start']))
    title_duration_sorted.to_csv('resources/title_duration.csv', header=None)
