import time
import json
import requests
from bs4 import BeautifulSoup
import multiprocessing

NB_CPU = multiprocessing.cpu_count()
NB_PROCESSES = 4




def make_request(url):
    # Make request to server
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Error while making request to {url}")
    else:
        return req



# partie B-1
def extract_beer_infos(url):
    beer_infos = {
        'Nom': None,
        'Style': None,
        'Contenu': None,
        'Degré d’alcool': None,
        'Origine': None,
        'Brasseur': None
    }
    
    # Make request
    req = make_request(url)
    
    # Retrieve whole content
    soup = BeautifulSoup(req.content, "html.parser")
    
    # Retrieve specific information
    soup_info = soup.find('div', class_='small-12 content-column')
    beer_infos['Nom'] = soup_info.find('h1').text.strip()
    beer_infos['Style'] = soup_info.find('dd', class_='small-6 medium-9 columns').find('a').text.strip()
    beer_infos['Contenu'] = int(soup_info.find('dd', class_='small-6 medium-9 columns js-beer-volume').text.strip().split()[0])
    beer_infos['Degré d’alcool'] = float(soup_info.find('dd', class_='small-6 medium-9 columns').find_next('dd', class_='small-6 medium-9 columns').text.strip().replace(',', '.').replace('%', ''))
    beer_infos['Origine'] = soup_info.find('dd', class_='small-6 medium-9 columns js-beer-country').text.strip()
    beer_infos['Brasseur'] = soup_info.find('dd', class_='small-6 medium-9 columns').find_next('dd', class_='small-6 medium-9 columns').find_next('dd', class_='small-6 medium-9 columns').text.strip()
    
    return beer_infos





# partie B-2

def apply_sequential(beer_pages):
    st = time.time()
    beers = [extract_beer_infos(url=beer_page) for beer_page in beer_pages]
    et = time.time()
    elapsed_time = et - st
    return elapsed_time, beers


def apply_parallel(beer_pages, processes=NB_PROCESSES):
    st = time.time()
    beers = []
    with multiprocessing.Pool(processes=processes) as pool: 
        beers += list(pool.map(extract_beer_infos, beer_pages))
    et = time.time()
    elapsed_time = et - st
    return elapsed_time, beers

    
def extract_beer_list_infos(url, URL_HOME='https://www.beerwulf.com/', mode='sequential'):
    # Collecter les pages de bières à partir du JSON
    req = make_request(url)
    soup = req.json()
    beer_pages = [f"{URL_HOME}{beer_info['contentReference']}" for beer_info in soup['items']]
    
    if mode == 'sequential':
        # Sequential version (slow):
        elapsed_time, beers = apply_sequential(beer_pages)

    elif mode == 'parallel':
        # Facultatif - Parallel version (faster):
        elapsed_time, beers = apply_parallel(beer_pages)
    else:
        raise ValueError("Unknown mode. Please select a mode between 'sequential' and 'parallel'")
    return elapsed_time, beers




if __name__ == "__main__":
    print("Number of cpu:", NB_CPU)

    URL_BEERLIST_FRANCE = "https://www.beerwulf.com/fr-FR/api/search/searchProducts?country=France&container=Bouteille"
    modes = ['sequential', 'parallel']
    
    for mode in modes:
        elapsed_time, beer_list_infos = extract_beer_list_infos(url=URL_BEERLIST_FRANCE, mode=mode)
        print(f"Mode '{mode}' took {elapsed_time} seconds")