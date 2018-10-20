from src.features import score_images

def build_img_data():
    score_images.get_keywords_all(['https://www.klinikum-karlsruhe.de', 'https://www.baeckerei-sand.de'], 200, 24)


build_img_data()