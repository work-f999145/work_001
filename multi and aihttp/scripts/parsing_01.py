from bs4 import BeautifulSoup as BS
import json
from zipfile import ZipFile, ZIP_DEFLATED
import os
from multiprocessing import Pool
from sys import stdout
import pandas as pd

def change_current_dir() -> None:
    file_name = os.path.basename(__file__)
    cwd = os.path.abspath(__file__).replace(file_name, '')
    os.chdir(cwd)

def load_pages()-> list:
    with ZipFile('../data/pages.zip') as zip_file:
        pages = list()
        for item in zip_file.filelist:
            with zip_file.open(item.filename) as file:
                pages.append(file.read().decode('utf-8'))
        return pages



def _parser_01(page: str):
    soup = BS(page, 'html.parser')
    cards = soup.find('div', class_='card-common').find_all('section', class_='common-text b-bottom pb-3')
    return list(map(str, cards))


def run_parser_01(lst:list[str]):
    with Pool(16) as pool:
        out = pool.map(_parser_01, lst)
        return out

# ---------------------------------------

def _convert_to_data_frame(lst: list):
    out_list = list()
    for item in lst[1:]:
        item = BS(item, 'html.parser')
        out_list.extend(list(item.stripped_strings)) 
    return out_list

def run_convert_to_data_frame(lst: list):
    with Pool(16) as pool:
        out_list = pool.map(_convert_to_data_frame, lst)
        return sum(out_list, [])

if __name__ == '__main__':
    change_current_dir()
    pages = load_pages()
    out_list = run_parser_01(pages)
    out = run_convert_to_data_frame(out_list)
    stdout.write(json.dumps(out))

