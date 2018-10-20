from src.features import score_images

def build_img_data(urls, output_path, num_workers=9, azure_key="fe06b4a3f2394b128be3686a3d72795c"):
    score_images.get_keywords_all(urls, num_workers, output_path, azure_key)
