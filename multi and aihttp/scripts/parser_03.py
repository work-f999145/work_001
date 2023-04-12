from config import *


def parser_03(page: str):
    text = str(argv[1])
    soup = BS(page, 'html.parser')
    card = soup.find('div', string=text)
    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_list = []
    else:
        out_list = list(card.stripped_strings)[1:]
    return out_list


if __name__ == '__main__':
    change_current_dir()
    pages = load_pages()
    list_ressult = run_parser(parser_03, pages)
    stdout.write(json.dumps(sum(list_ressult, [])))