from config import *


def parser_02(page: str):
    soup = BS(page, 'html.parser')
    cards = soup.find('div', class_='card-common').find_all('section', class_='common-text b-bottom pb-3')
    out_list = []
    for card in cards:
        tmp = list(card.stripped_strings)[0]
        out_list.append(tmp)
    return out_list


if __name__ == '__main__':
    change_current_dir()
    pages = load_pages()
    list_ressult = run_parser(parser_02, pages)
    stdout.write(json.dumps(sum(list_ressult, [])))