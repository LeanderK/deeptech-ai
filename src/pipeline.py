import sys

sys.path.append('/Users/julianbrendl/Projects/deeptech-ai/infersent')

from features.gather_seo_data import extract_metadata
from features.score_images import get_keywords
from features.quality_image_tags import filter_words
from infersent import infersent
import numpy as np
import pickle

labels = {
    0: 'LAND- UND FORSTWIRTSCHAFT, FISCHEREI',
    1: 'BERGBAU UND GEWINNUNG VON STEINEN UND ERDENBERGBAU UND GEWINNUNG VON STEINEN UND ERDEN',
    2: 'ÖFFENTLICHE VERWALTUNG, VERTEIDIGUNG; SOZIALVERSICHERUNG',
    3: 'KUNST, UNTERHALTUNG UND ERHOLUNG',
    4: 'WASSERVERSORGUNG; ABWASSER- UND ABFALLENTSORGUNG UND BESEITIGUNG VON UMWELTVERSCHMUTZUNGEN',
    5: 'GASTGEWERBE',
    6: 'ENERGIEVERSORGUNG',
    7: 'ERZIEHUNG UND UNTERRICHT',
    8: 'GRUNDSTÜCKS- UND WOHNUNGSWESEN',
    9: 'ERBRINGUNG VON SONSTIGEN DIENSTLEISTUNGEN',
    10: 'ERBRINGUNG VON FINANZ- UND VERSICHERUNGSDIENSTLEISTUNGEN',
    11: 'VERKEHR UND LAGEREI',
    12: 'INFORMATION UND KOMMUNIKATION',
    13: 'GESUNDHEITS- UND SOZIALWESEN',
    14: 'BAUGEWERBE',
    15: 'ERBRINGUNG VON SONSTIGEN WIRTSCHAFTLICHEN DIENSTLEISTUNGEN',
    16: 'ERBRINGUNG VON FREIBERUFLICHEN, WISSENSCHAFTLICHEN UND TECHNISCHEN DIENSTLEISTUNGEN',
    17: 'HANDEL; INSTANDHALTUNG UND REPARATUR VON KRAFTFAHRZEUGEN',
    18: 'VERARBEITENDES GEWERBE'
}

from sklearn.externals import joblib
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
    mean_embbedding = np.mean(embeddings, axis=0)

    # Predict
    model2 = joblib.load(r'02-SB-SVM.joblib')
    clazz = model2.predict(mean_embbedding.reshape(1, -1))[0]
    clazz = labels[clazz]
    print('Predicted class: {cls}'.format(cls=clazz))
    return clazz


classify('www.hackundsoehne.de')