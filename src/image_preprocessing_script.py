from src.features import build_features, score_images
from src.data import load_data
from src.util import init
import click

# Init project
init.init()

#urls = load_data.load_pickle('/Users/julianbrendl/Projects/deeptech-ai/data/raw/companies.pickle')
#build_features.build_img_data(urls)

#score_images.get_keywords('www.vobadirekt.de')
#score_images.get_keywords('www.treureal.de')
#score_images.get_min_dimension('http://bsv-bauservice.de/media/banner_C_final.jpg')


@click.command()
@click.option("--companies-pickle-path", default=r'/home/sandro/Projekte/github_projects/deeptech-ai/data/raw/companies.pickle')
@click.option("--start-index", default=0)
@click.option("--end-index", default=-1)
@click.option("--azure-key", default='efdb6416d7d34344b01f7fe6eec963d5')
@click.option("--num-workers", default=3)
def main(companies_pickle_path, start_index, end_index, num_workers, azure_key):
    urls = load_data.load_pickle(companies_pickle_path)
    if end_index == -1:
        end_index = len(urls)
    url_batch = urls[start_index:end_index]
    build_features.build_img_data(url_batch, num_workers=num_workers, azure_key=azure_key)


if __name__ == '__main__':
    main()



