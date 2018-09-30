import pandas as pd
from itertools import islice
from convert_to_pdf import PDF

# Inspecting data
audio_transcript = pd.read_csv('resources/lecture_1.csv', sep=',', header=None,
                               names=['label', 'start', 'end', 'text'], converters={'label': str, 'text': str})
# print("Input data has {} rows and {} columns".format(len(audio_transcript), len(audio_transcript.columns)))
# print(audio_transcript.info())

lecture_titles = pd.read_csv('resources/lecture_1_titles.csv', sep=',', header=None, names=['time', 'text'])
# print("Input data has {} rows and {} columns".format(len(lecture_titles), len(lecture_titles.columns)))
# print(lecture_titles.info())

lecture_images = pd.read_csv('resources/lecture_1_images.csv', sep=',', header=None,
                             names=['label', 'start', 'image_name'], converters={'label': str, 'image_name': str})
# print("Input data has {} rows and {} columns".format(len(lecture_images), len(lecture_images.columns)))
# print(lecture_images.info())


# Acquiring the entire audio transcript
# lecture_text = ''
# for index, column in audio_transcript.iterrows():
#     # start = column[1]
#     text = column[2]
#     lecture_text = lecture_text + ' ' + text
# print(lecture_text)

# Aligning images to audio transcript
all_lecture_content = audio_transcript.merge(lecture_images, how='outer', on=['start', 'label'])
df = pd.DataFrame(all_lecture_content)
all_lecture_content_sorted = df.sort_values(by=['start'])
# print("Input data has {} rows and {} columns".format(len(all_lecture_content_sorted),
#                                                      len(all_lecture_content_sorted.columns)))
# print(all_lecture_content_sorted.info())
# print(df.sort_values(by=['start']))
# all_lecture_content_sorted.to_csv('resources/all_content.csv', header=None)

# Converting to PDF
pdf_doc = PDF()
pdf_doc.set_title('Theory of Computation' + '\n' + 'Chapter 1: Introduction')
pdf_doc.set_author('Prof. Somenath Biswas')

# The topic of the lecture
# print(lecture_titles.iloc[0]['text'] + '\n')

# First topic
# print(lecture_titles.iloc[1]['text'])

# Align text
# def segmenting_text():
#     return 0


# Align image
# def adding_images():
#     return 0


# Aligning content with topics
# def align_all_content(content_label):
#     return {
#         'text': segmenting_text(),
#         'image': adding_images()
#     }[content_label]

# General method for topic segmentation
upper_limit_time = 0
for index, column in islice(lecture_titles.iterrows(), 1, None):
    time = (int(column[0][1:3]) * 60 + int(column[0][4:6])) * 1000
    topic = column[1]
    topic_content = ''
    image_path = ''
    for index_content, column_content in all_lecture_content_sorted.iterrows():
        label = column_content[0]
        # align_all_content(label)
        if label == 'text':
            start_time = int(column_content[1])
            end_time = int(column_content[2])
            if end_time > time:
                upper_limit_time = time
                break
            elif start_time > upper_limit_time:
                topic_content = topic_content + column_content[3] + ' '
            else:
                continue
        elif label == 'image':
            image_name = str(column_content[4])
            image_path = 'resources/images/lecture_1/' + image_name
    print(topic_content) if topic_content != ' ' else print('')
    print(image_path)
    pdf_doc.print_chapter(index, topic, topic_content + '\n\n', image_path)
    print('\n')
    print(topic)

# Create a PDF file
pdf_doc.add_page()
pdf_doc.output('lecture_note.pdf', 'F')
