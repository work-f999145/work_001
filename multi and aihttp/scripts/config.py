from bs4 import BeautifulSoup as BS
import json
from zipfile import ZipFile, ZIP_DEFLATED
import os
from multiprocessing import Pool
from multiprocessing import cpu_count
from sys import stdout, argv
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

def run_parser(func, lst:list[str]) -> list:
    with Pool(cpu_count()) as pool:
        out = pool.map(func=func, iterable=lst)
        return out

if __name__ == '__main__':
    pass