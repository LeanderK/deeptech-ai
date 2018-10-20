import subprocess
import requests
import json
import urllib
from PIL import ImageFile
from multiprocessing import Pool as ProcessPool
from tqdm import tqdm
import numpy as np

min_dim = 0

def get_keywords_all(urls, min_dim_l, num_workers):
    global min_dim

    workers = ProcessPool(num_workers)
    min_dim = min_dim_l
    count = 0
    results = np.array([])
    with tqdm(total=len(urls)) as pbar:
        for result in tqdm(workers.imap_unordered(get_keywords, urls)):
            count += len(result)
            results = np.append(results, result)
            pbar.update()

    path = 'data/processed/img_data.npz'
    print('Processed %d urls.' % count)
    print('Saving results to {path}'.format(path=path))
    np.save(path, results)
    print('Done saving.')

def get_keywords(url):
    image_urls = scrap_image_urls(url)
    image_urls = list(filter(lambda url: get_min_dimension(url) > min_dim, image_urls))
    data_points = list(map(lambda img: analyze_image(img), image_urls))
    data_points = list(map(lambda img: parse_data(img), data_points))
    data_points = [item for sublist in data_points for item in sublist]

    return {
        'img_train_data': data_points,
        'url': url
    }

def scrap_image_urls(url):
    proc = subprocess.run(['image-scraper --dump-urls {url}'.format(url=url)], shell=True, stdout=subprocess.PIPE)
    output = proc.stdout.decode('utf-8')
    output_list = output.split('\n')
    return filter(lambda str: str.startswith('http'), output_list)

def get_size(url):
    try:
        # get file size *and* image size (None if not known)
        file = urllib.request.urlopen(url)
        size = file.headers.get("content-length")
        if size:
            size = int(size)
        p = ImageFile.Parser()
        while True:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
                break
        file.close()
    except Exception as e:
        print('Unable to get image size for url: {img}.'.format(img=url))
        return -1, [-1, -1]

    return size, None

def get_min_dimension(url):
    fsize, xy = get_size(url)
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
