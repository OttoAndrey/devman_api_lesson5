from itertools import count

import requests

from common_tools import predict_salary


def predict_rub_salary_hh(vacancy):
    min_salary = vacancy['salary']['from']
    max_salary = vacancy['salary']['to']

    return predict_salary(min_salary, max_salary)


def vacancies_info_from_hh(prog_langs):
    prog_langs_info = {}

    for prog_lang in prog_langs[:1]:
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
            'vacancies_found': page_data['found'],
            'vacancies_processed': len(avg_salaries),
            'average_salary': avg_salary,
        }

    return prog_langs_info
