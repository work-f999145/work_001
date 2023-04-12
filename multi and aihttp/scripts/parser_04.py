from config import *
from parsers import parsing_information_from_the_site



if __name__ == '__main__':
    change_current_dir()
    pages = load_pages()
    list_result = run_parser(parsing_information_from_the_site, pages)
    df = pd.concat(list_result, ignore_index=True, sort=False)
    # print(df.to_json())

    stdout.write(df.to_json())