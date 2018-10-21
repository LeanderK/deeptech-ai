import os
import numpy as np
import functools
import glob

STOP_LIST = ['', 'text']

def process_words(urls):
    keywords = merge_image_data(urls)
    filter_words(keywords, 0.5)

def merge_image_data(urls):
    os.chdir("/mydir")
    for file in glob.glob("*.txt"):
        print(file)

    data = np.array([])
    for url in urls:
        batch_data = np.load(url)
        np.append(data, batch_data)

    return data


def filter_words(keywords, min_confidence):
    keywords = [{sublist['url']: [item for item in sublist['img_train_data'] if item['score'] > min_confidence
                       and not item['name'] in STOP_LIST ]} for sublist in keywords]

    keywords_dict = dict()
    for elem in keywords:
        for url, words in elem.items():
            words = sorted(words, key=lambda word: word['score'], reverse=True)
            words = list(map(lambda word: word['name'], words))
            keywords_dict[url] = list(set(words))

    return keywords_dict



process_words([''])