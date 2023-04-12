# Тест асинхронного парсинга
# Как выяснилось он не намного быстрее многопоточного парсинга из юпитера
# Однако оставил схему работы на тот случай если понадобится асихронная функция
# 
# Стоит отметить что при использовании очереде, оптимальное количество задач колеблится от 8 до 16.


import json
from tqdm import tqdm
import pandas as pd
import time
import os

import aiohttp, asyncio

# Так как функция открывается не из корня рабочей директории, 
# требуется переназначить текущую директорию на место расположения исполняемого файла
file_name = os.path.basename(__file__)
cwd = os.path.abspath(__file__).replace(file_name, '')
os.chdir(cwd)


proxy_url = '45.81.76.252'
proxy_port = '8000'

proxy = {
    'https': f'http://{proxy_url}:{proxy_port}'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

params = {
    'searchString': '',
    'morphology': 'on',
    'search-filter': 'Дате обновления',
    'savedSearchSettingsIdHidden': '',
    'fz94': 'on',
    'fz223': 'on',
    'published': 'on',
    'regarded': 'on',
    'considered': 'on',
    'decisionOnTheComplaintTypeResult': '',
    'receiptDateStart': '',
    'receiptDateEnd': '',
    'updateDateFrom': '',
    'updateDateTo': '',
    'sortBy': 'UPDATE_DATE',
    'pageNumber': '',
    'sortDirection': 'false',
    'recordsPerPage': '_10',
    'showLotsInfoHidden': 'false',
}

url = """

https://zakupki.gov.ru/epz/complaint/search/search_eis.html

""".strip()
host = '/'.join(url.split('/', maxsplit=3)[:3])


# Загрузка из файла списка со ссылками.
with open('data/links_list.json', 'r', encoding='utf-8') as file:
    tmp = file.read()
    links_list = json.loads(tmp)
    

async def _worker(queue: asyncio.Queue[tuple[str, tqdm]]):
    # корутина которая берет задание из очереди и выполняет его
    
    # лист который будет возвращет по выполнению задачи
    reponse_async_list = list()
    
    # Не совсем понятно как работает таймоут здесь
    timeout = aiohttp.ClientTimeout(total=60)
    while True:
        # В бесконечном цикле будет выполняться эта функция.
        # она каждый раз берет задачу из очереди, и выполняет ее.
        link, pbar = await queue.get()
        # Создается сессия
        async with aiohttp.ClientSession(headers=headers) as session:
            # Получаем ответ //непонятно как работает таймаут
            response = await session.get(url=link, proxy=proxy.get('https', ''), timeout=timeout)
            # Получаем текст
            text = await response.text()
        # Добавляем результат в возращаемый список
        reponse_async_list.append(text)
        
        # подтверждаем выполнение задачи.
        # ???Нужно проверить как подвердить что задача не выполнена и вернуть ее в очередь
        queue.task_done()
        pbar.update(1)
        
        # Если очередь опустела прекращаем цикл
        if queue.empty():
            break
    return reponse_async_list

def _queue(input_url_list: list[str], pbar: tqdm) -> asyncio.Queue[tuple[str, tqdm]]:
    # Создание очереди. // тут так же указывается что будет передаваться в рабочую функцию
    queue: asyncio.Queue[tuple[str, tqdm]] = asyncio.Queue()
    for link in input_url_list:
        queue.put_nowait((link, pbar))
    return queue

async def get_pages_tasks(input_url_list: list[str], n_tasks: int):
    # Пустой список с задачами
    tasks: list[asyncio.Task] = []
    with tqdm(total=len(input_url_list)) as pbar:
        # Получаем очередь задач
        queue = _queue(input_url_list, pbar)
        # Содаем Н-ое количество задач/функций которые будет черпать задачи из очереди
        for _ in range(n_tasks):
            one_task = asyncio.create_task(_worker(queue))
            tasks.append(one_task)
        
        # Указываем в необходимости дождаться выполнения всей очереди задач
        await queue.join()
        
        # Завершаем все задачи/функции
        for one_task in tasks:
            one_task.cancel()
    
    # не знаю что это, но так нужно
    return  await asyncio.gather(*tasks, return_exceptions=True)
    

    
    
if __name__ == '__main__':
    ntask = 8
    
    if os.path.isfile('data/async_test.csv'):
        df = pd.read_csv('data/async_test.csv')
    else:
        df = pd.DataFrame()
    # Количество тестов
    for _ in range(4):
        start = time.time()
        try:
            # Здесь мы запускаем асихронный скрипт, и получаем результат.
            list_pages = asyncio.run(get_pages_tasks(links_list, ntask))
        except Exception as ex:
            print(ex)
        else:
            delta = time.time() - start
            
            df_temp = pd.DataFrame(
                {
                    'Count_task': [ntask],
                    'Time': [delta]
                }
            )
            df = pd.concat([df, df_temp], ignore_index=True, sort=False)
            
    df.to_csv('data/async_test.csv', index=False)