import subprocess
from subprocess import PIPE
import requests
import json
from io import BytesIO
from PIL import Image
from multiprocessing import Pool as ProcessPool
from tqdm import tqdm
import numpy as np
import random
import time

NUM_IMAGES_KEEP = 3
err_urls = []


def get_keywords_all(urls, num_workers):

    random.shuffle(urls)
    workers = ProcessPool(num_workers)
    count = 0
    results = np.array([])
    with tqdm(total=len(urls)) as pbar:
        for result in tqdm(workers.imap_unordered(get_keywords, urls)):
            count += len(result)
            results = np.append(results, result)
            pbar.update()

    path = 'data/processed/img_data.npy'
    print('Processed %d urls.' % count)
    print('Saving results to {path}'.format(path=path))
    np.save(path, results)
    print('Done saving.')

def get_keywords(url):
    print('Starting url: {url}'.format(url=url))
    image_urls = scrap_image_urls(url)

    # Filter out SVGs and GIFs
    image_urls = filter(lambda url: not url.endswith('svg'), image_urls)
    image_urls = list(filter(lambda url: not url.endswith('gif'), image_urls))

    # Sort by size and take 3 biggest
    image_urls = sorted(image_urls, key=lambda url: get_min_dimension(url), reverse=True)[:NUM_IMAGES_KEEP]

    # Analyze images with azure
    data_points = map(lambda img: analyze_image(img), image_urls)
    data_points = list(map(lambda img: parse_data(img), data_points))
    data_points = [item for sublist in data_points for item in sublist]

    # If azure is full, wait and try again
    counter = 0
    while (len(image_urls) > 0 and len(data_points) == 0) and counter < 10:
        print('Azure full, waiting {counter}... ({url})'.format(counter=counter, url=url))
        counter += 1
        time.sleep(7)

        data_points = map(lambda img: analyze_image(img), image_urls)
        data_points = list(map(lambda img: parse_data(img), data_points))
        data_points = [item for sublist in data_points for item in sublist]

    if counter == 10:
        print('ERROR - Azure failed after {counter} tries: {url}'.format(counter=counter, url=url))

    if len(data_points) == 0:
        print('ERROR - URL failed: {url}.'.format(url=url, n=len(data_points)))
    else:
        print('Done with url: {url}. Got {n} keywords.'.format(url=url, n=len(data_points)))

    return {
        'img_train_data': data_points,
        'url': url
    }

def scrap_image_urls(url):
    proc = subprocess.Popen(['image-scraper --dump-urls {url}'.format(url=url)], shell=True, stdout=PIPE)
    if isinstance(proc, int):
        print('Really bad error with url: {url}'.format(url=url))
        return []

    output, err = proc.communicate()
    output = output.decode('utf-8')
    output_list = output.split('\n')
    return filter(lambda str: str.startswith('http'), output_list)

def get_size(url):
    try:
        data = requests.get(url).content
        im = Image.open(BytesIO(data))
        return im.size
    except Exception as e:
        print('Unable to get image size for url: {img}.'.format(img=url))
        return [-1, -1]

def get_min_dimension(url):
    xy = get_size(url)
    return min(xy[0], xy[1])

def analyze_image(image_url):
    url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/analyze?visualFeatures=Categories,Tags,Description&details=Landmarks&language=en"
    data = {
        "url": image_url
    }
    headers = {
        "Ocp-Apim-Subscription-Key": "fe06b4a3f2394b128be3686a3d72795c",
        "Content-Type": "application/json"
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return json.loads(r.content.decode('utf-8'))

def parse_data(img_json):
    result = []

    if 'categories' in img_json:
        for cat in img_json['categories']:
            name = cat['name']
            names = name.split('_')
            for n in names:
                result.append({
                    'name': n,
                    'score': cat['score']
                })

    if 'tags' in img_json:
        for tag in img_json['tags']:
            result.append({
                'name': tag['name'],
                'score': tag['confidence']
            })

    return result
