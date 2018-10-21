import sys

sys.path.append('/Users/julianbrendl/Projects/deeptech-ai/infersent')

from features.gather_seo_data import extract_metadata
from features.score_images import get_keywords
from features.quality_image_tags import filter_words
from infersent import infersent

def classify(url):

    # Get SEO keywords
    seo_keywords = extract_metadata(url)

    # Get image based keywords
    img_keywords = get_keywords(url)['img_train_data']
    img_keywords = filter_words([{'url': url, 'img_train_data': img_keywords}], 0.9).values()
    img_keywords = [item for sublist in img_keywords for item in sublist]

    # Combine keywords
    keywords = img_keywords + seo_keywords

    # Calculate embeddings
    embeddings = list(map(infersent.get_embedding, keywords))


classify('www.opencodes.io')