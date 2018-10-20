from features import build_features
from features import score_images
from data import load_data
from util import init

# Init project
init.init()

urls = load_data.load_pickle('/Users/julianbrendl/Projects/deeptech-ai/data/raw/companies.pickle')
build_features.build_img_data(urls)

#score_images.get_keywords('www.kurz-recycling.de')
#score_images.get_keywords('www.kautex.de')
#score_images.get_min_dimension('https://baubeconstadtsanierung.de/wp-content/uploads/2018/06/Bild_Tag-der-Städtebauförderung-680x400.jpg.')