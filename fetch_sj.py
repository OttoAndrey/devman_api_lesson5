import os
from itertools import count

import requests

from common_tools import predict_salary


def predict_rub_salary_sj(vacancy):
    min_salary = vacancy['payment_from']
    max_salary = vacancy['payment_to']

    if min_salary == 0:
        min_salary = None
    if max_salary == 0:
        max_salary = None

    return predict_salary(min_salary, max_salary)


def vacancies_info_from_sj(prog_langs):
    secret_key = os.getenv("SUPERJOB_SECRET_KEY")

    prog_langs_info = {}
    headers = {'X-Api-App-Id': secret_key}

    for prog_lang in prog_langs[:1]:
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
            'vacancies_found': page_data['total'],
            'vacancies_processed': len(avg_salaries),
            'average_salary': avg_salary,
        }

    return prog_langs_info
