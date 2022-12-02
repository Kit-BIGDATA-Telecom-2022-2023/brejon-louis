import os
import shutil
import requests
import pandas as pd
import uuid
import xlwings as xw

from shutil import copyfileobj
from urllib import request
from matplotlib.cm import get_cmap



def make_request(url, verbose=True):
    """ Make request to server 
    Args:
        url (String): web page url
    Returns;
        req (BeautifulSoup object): request objetc
    """
    req = requests.get(url)
    if req.status_code != 200:
        raise ValueError(f"Error while making request to {url}")
    else:
        if verbose:
            print(f"Request url {url}")
        return req
    
    
def download_file(url, filename_dst):
    """ Download data from url and to local filename 
    Args:
        url (String): web page url
        filename_dst (String): filename destination path
    Returns:
        None
    """
    with request.urlopen(url) as response, open(filename_dst, 'wb') as out_file:
        copyfileobj(response, out_file)
        
        
def create_dir(dir_path):
    """ Create directory if does not exist 
    Args:
        dir_path (String): directory path
    Returns:
        None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory '{dir_path.split('/', maxsplit=1)[-1]}' created at '{dir_path.split('/', maxsplit=1)[0]}/' path")
        
        
def remove_file(filename):
    """ Remove file
    Args:
        filename (String): filename
    Returns:
        None
    """
    os.remove(filename)
    
    
def remove_dir(dir_path):
    """ Remove directory
    Args:
        dir_path (String): directory path
    Returns:
        None
    """
    shutil.rmtree(dir_path)
    
    
###### Load/Save functions
def load_csv(csv_path, verbose=False):
    """ Load data from csv file
    Args:
        csv_path (String): csv path
    Returns:
        df (Dataframe): csv data loaded
    """
    df = pd.read_csv(csv_path)
    if verbose:
        print(f"Csv file successfully loaded from '{csv_path}'")
    return df



def save_csv(df, csv_path, verbose=False):
    """ Save data to csv file
    Args:
        df (Dataframe): Dataframe
        csv_path (String): csv path
    Returns:
        None
    """
    df.to_csv(csv_path, index=False)
    if verbose:
        print(f"Dataframe successfully saved to '{csv_path}'")

    
def save_with_xlwings(file, dir_dst=''):
    """ Save file using XLWINGS for reading/writing Excel file
    Args:
        file (String): filename
        dir_dst (String, optional): directory destination path
    Returns:
        tempfile (String): uuid filename
    """
    tempfile = dir_dst + '{uuid.uuid1()}.xlsx'
    excel_app = xw.App(visible=False)
    excel_book = excel_app.books.open(file)
    excel_book.save(tempfile)
    excel_book.close()
    excel_app.quit()
    return tempfile



def generate_color_categories(categories, rgb=True):
    """ Generate n colors, useful for coloring different categories 
    Args:
        categories (Array of strings): categories to process
    Returns:
        color_map (Dictionary): contains color for each category
    """
    ncol = len(categories)
    if ncol <= 50:
        colors = [i for i in get_cmap('tab20b').colors]
        colors += [i for i in get_cmap('tab20c').colors]
        colors += [i for i in get_cmap('tab20c_r').colors]
        colors = colors[:ncol]
    elif 50 < ncol <= 256:
        cmap = get_cmap(name='viridis')
        cmap = get_cmap(name='rainbow')
        colors = cmap(np.linspace(0, 1, ncol))
    else:
        raise ValueError('Maximum 256 categories')
    
    color_map = {}
    for i, key in enumerate(categories):
        if rgb:
            color_map[key] = 'rgb({r},{g},{b})'.format(r=colors[i][0], g=colors[i][1], b=colors[i][2])
        else:
            color_map[key] = colors[i][:3]
    return color_map
