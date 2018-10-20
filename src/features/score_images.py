import subprocess

def scrap_image_urls(url):
    proc = subprocess.run(['image-scraper --dump-urls {url}'.format(url=url)], shell=True, stdout=subprocess.PIPE)
    output = proc.stdout.decode('utf-8')
    output_list = output.split('\n')
    return list(filter(lambda str: str.startswith('http'), output_list))

scrap_image_urls('https://www.baeckerei-sand.de/')