from dotenv import load_dotenv

from common_tools import get_table_data, create_table
from fetch_hh import vacancies_info_from_hh
from fetch_sj import vacancies_info_from_sj


def main():
    load_dotenv()
    print('Выполняется..')

    prog_langs = ['Программист JavaScript',
                  'Программист Java',
                  'Программист Python',
                  'Программист Ruby',
                  'Программист PHP',
                  'Программист C++',
                  'Программист C#',
                  'Программист C',
                  'Программист Go',
                  'Программист Objective-C',
                  'Программист Scala',
                  'Программист Swift',
                  'Программист TypeScript', ]

    hh_info = vacancies_info_from_hh(prog_langs)
    sj_info = vacancies_info_from_sj(prog_langs)

    hh_table_data = get_table_data(hh_info)
    sj_table_data = get_table_data(sj_info)

    hh_table = create_table(hh_table_data, 'HeadHunter Moscow')
    sj_table = create_table(sj_table_data, 'SuperJob Moscow')

    print(hh_table.table)
    print()
    print(sj_table.table)


if __name__ == '__main__':
    main()
