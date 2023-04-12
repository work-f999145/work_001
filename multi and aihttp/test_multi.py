#  Первый тест запуска многопроцессорного скрипта из Юпитера


import requests
from bs4 import BeautifulSoup as BS
import json
from tqdm import tqdm
from zipfile import ZipFile, ZIP_DEFLATED
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import time
import os
from multiprocessing import Pool
import sys

file_name = os.path.basename(__file__)
cwd = os.path.abspath(__file__).replace(file_name, '')
os.chdir(cwd)


def _get_number(text: str) -> str:
    soup = BS(text, 'html.parser')
    complaint = soup.find('div', class_='sectionMainInfo borderRight col-9')
    number_complaint = complaint.find('div', class_='cardMainInfo__status').find('a').get_text()[2:]
    return number_complaint

with ZipFile('data/pages.zip') as zip_file:
    pages = list()
    for item in zip_file.filelist:
        with zip_file.open(item.filename) as file:
            pages.append(file.read())


def _get_number_th(lst:list[str]):
    with ThreadPool(16) as pool:
        out = pool.map(_get_number, lst)
        return out

def _get_number_mp(lst:list[str]):
    with Pool(16) as pool:
        out = pool.map(_get_number, lst)
        return out

if __name__ == '__main__':
    start = time.time()
    with ZipFile('data/pages_test.zip', 'w', compression=ZIP_DEFLATED, compresslevel=1) as zip_file:
        numbers = _get_number_mp(pages)
        for number, page in zip(numbers, pages):
        # for number, page in enumerate(pages):
            zip_file.writestr(f'{number}.html', page)
    sys.stdout.write(json.dumps((time.time() - start)))