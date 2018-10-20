from features import build_features
from data import load_data
from util import init

# Init project
init.init()

urls = load_data.load_pickle('/Users/julianbrendl/Projects/deeptech-ai/data/raw/companies.pickle')
build_features.build_img_data(urls)