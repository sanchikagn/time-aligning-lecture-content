import pandas as pd
from title_duration import converting_to_topic_classes
from convert_to_pdf import PDF


def aligning_content():
    converting_to_topic_classes()
    # Inspecting data
    audio_transcript = pd.read_csv('resources/lecture_1.csv', sep=',', header=None,
                                   names=['label', 'start', 'end', 'text'], converters={'label': str, 'text': str})
    # print("Input data has {} rows and {} columns".format(len(audio_transcript), len(audio_transcript.columns)))
    # print(audio_transcript.info())

    lecture_titles = pd.read_csv('resources/title_duration.csv', sep=',', header=None,
                                 names=['start', 'end', 'text'])
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
    all_lecture_content_sorted = entire_lecture(audio_transcript, lecture_images)

    # The topic of the lecture
    # print(lecture_titles.iloc[0]['text'])

    lecture, pdf_doc = topic_segmentation(lecture_titles, all_lecture_content_sorted, create_pdf())

    # Create a PDF file
    pdf_doc.add_page()
    pdf_doc.output('lecture_note.pdf', 'F')

    # print(lecture)
    return lecture


# Aligning images to audio transcript
def entire_lecture(audio_transcript, lecture_images):
    all_lecture_content = audio_transcript.merge(lecture_images, how='outer', on=['start', 'label'])
    df = pd.DataFrame(all_lecture_content)
    all_lecture_content_sorted = df.sort_values(by=['start'])
    # print("Input data has {} rows and {} columns".format(len(all_lecture_content_sorted),
    #                                                      len(all_lecture_content_sorted.columns)))
    # print(all_lecture_content_sorted.info())
    # print(df.sort_values(by=['start']))
    # all_lecture_content_sorted.to_csv('resources/all_content.csv', header=None)
    return all_lecture_content_sorted


# General method for topic segmentation
def topic_segmentation(lecture_titles, all_lecture_content_sorted, pdf_doc):
    lecture = pd.DataFrame(columns=['start', 'end', 'topic', 'content'])
    for index, column in lecture_titles.iterrows():
        start = int(column[0])
        end = int(column[1])
        topic = column[2]
        # pre_topic = topic
        topic_content = ''
        image_path = ''
        for index_content, column_content in all_lecture_content_sorted.iterrows():
            label = column_content[0]
            # align_all_content(label)
            if label == 'text':
                start_time = int(column_content[1])
                end_time = int(column_content[2])
                if end_time >= end:
                    topic_content = topic_content + column_content[3] + ' '
                    break
                elif start_time >= start:
                    topic_content = topic_content + column_content[3] + ' '
                else:
                    continue
            elif label == 'image':
                image_name = str(column_content[4])
                image_path = 'resources/images/lecture_1/' + image_name

        # adding to lecture df
        lecture = lecture.append({'start': start, 'end': end, 'topic': topic, 'content': topic_content,
                                  'image': image_path}, ignore_index=True)

        # creating the pdf
        pdf_doc.print_chapter(index, topic, topic_content + '\n', image_path)
        # print(topic)
        # print(topic_content) if topic_content != '' else print('')
        # print(image_path)
        # print('\n')
    return lecture, pdf_doc


def create_pdf():
    # Converting to PDF
    pdf_doc = PDF()
    pdf_doc.set_title('Theory of Computation' + '\n' + 'Chapter 1: Introduction')
    pdf_doc.set_author('Prof. Somenath Biswas')
    return pdf_doc
