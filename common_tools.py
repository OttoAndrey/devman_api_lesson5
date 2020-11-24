from terminaltables import AsciiTable


def predict_salary(salary_from, salary_to):
    avg_salary = None

    if salary_from and salary_to:
        avg_salary = (salary_from + salary_to) / 2
    elif salary_from:
        avg_salary = salary_from * 1.2
    elif salary_to:
        avg_salary = salary_to * 0.8

    return avg_salary


def get_table_data(data):
    table_data = []

    for lang, info in data.items():
        row = [lang, info['vacancies_found'], info['vacancies_processed'], info['average_salary']]
        table_data.append(row)

    return table_data


def create_table(table_data, title):
    header = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    table_data.insert(0, header)
    table = AsciiTable(table_data)
    table.title = title

    return table