import requests
import os

from dotenv import load_dotenv
from terminaltables import AsciiTable
from itertools import count


def predict_salary(salary_from, salary_to):
    avg_salary = None

    if salary_from and salary_to:
        avg_salary = (salary_from + salary_to) / 2
    elif salary_from:
        avg_salary = salary_from * 1.2
    elif salary_to:
        avg_salary = salary_to * 0.8

    return avg_salary


def predict_rub_salary_sj(vacancy):
    min_salary = vacancy['payment_from']
    max_salary = vacancy['payment_to']

    if min_salary == 0:
        min_salary = None
    if max_salary == 0:
        max_salary = None

    return predict_salary(min_salary, max_salary)


def predict_rub_salary_hh(vacancy):
    min_salary = vacancy['salary']['from']
    max_salary = vacancy['salary']['to']

    return predict_salary(min_salary, max_salary)


def vacancies_info_from_hh(prog_langs):
    prog_langs_info = {}

    for prog_lang in prog_langs:
        avg_salaries = []

        for page in count(0):
            params = {'text': prog_lang, 'period': 30, 'area': 1}
            response = requests.get('https://api.hh.ru/vacancies/', params=params)
            response.raise_for_status()
            page_data = response.json()

            if page >= page_data['pages']:
                break

            for item in page_data['items']:
                if not item['salary']:
                    continue

                if not item['salary']['currency'] == 'RUR':
                    continue

                avg_salaries.append(predict_rub_salary_hh(item))

        avg_salary = int(sum(avg_salaries) / len(avg_salaries))

        prog_langs_info[prog_lang] = {
            'vacancies_found': response.json()['found'],
            'vacancies_processed': len(avg_salaries),
            'average_salary': avg_salary,
        }

    return prog_langs_info


def vacancies_info_from_sj(prog_langs):
    secret_key = os.getenv("SUPERJOB_SECRET_KEY")

    prog_langs_info = {}
    headers = {'X-Api-App-Id': secret_key}

    for prog_lang in prog_langs:
        avg_salaries = []

        for page in count(0):
            params = {'town': 4, 'keyword': prog_lang, 'page': page}
            response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
            response.raise_for_status()
            page_data = response.json()

            total = page_data['total']
            pages = int(total / 20)

            if page >= pages:
                break

            for item in page_data['objects']:
                salary = predict_rub_salary_sj(item)
                if not predict_rub_salary_sj(item):
                    continue
                avg_salaries.append(salary)

        avg_salary = int(sum(avg_salaries) / len(avg_salaries))

        prog_langs_info[prog_lang] = {
            'vacancies_found': response.json()['total'],
            'vacancies_processed': len(avg_salaries),
            'average_salary': avg_salary,
        }

    return prog_langs_info


def dict_to_table_data(data):
    table_data = []

    for lang, info in data.items():
        row = [lang, info['vacancies_found'], info['vacancies_processed'], info['average_salary']]
        table_data.append(row)

    return table_data


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

    hh_table_data = dict_to_table_data(hh_info)
    sj_table_data = dict_to_table_data(sj_info)

    header = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']

    hh_table_data.insert(0, header)
    hh_table = AsciiTable(hh_table_data)
    hh_table.title = 'HeadHunter Moscow'
    print(hh_table.table)
    print()

    sj_table_data.insert(0, header)
    sj_table = AsciiTable(sj_table_data)
    sj_table.title = 'SuperJob Moscow'
    print(sj_table.table)


if __name__ == '__main__':
    main()
