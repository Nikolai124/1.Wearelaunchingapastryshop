import datetime
import pandas
import collections


from pprint import pprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_write_year(year):
    last_number = year % 10
    prelast_number = year // 10 % 10
    if 9 >= last_number >= 5 or last_number == 0:
        write_year = "лет"
    elif last_number == 1:
        if prelast_number == 1: 
            write_year = "лет"
        else:
            write_year = "год"
    elif 4 >= last_number >= 2:
        if prelast_number == 1:
            write_year = "лет"
        else:
            write_year = "года"
    return write_year

def get_year():
    now = datetime.datetime.now()
    year = now.year - 2010
    return year


def main(): 
    cakes = pandas.read_excel('cakes3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict('records')
    cakes_collection = collections.defaultdict(list)
    for cake in cakes:
        cakes_collection[cake['Категория']].append(cake)
    print(cakes_collection)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    year = get_year()
    write_year = get_write_year(year)
    rendered_page = template.render(
    year=year,
    write_year=write_year,
    cakes=cakes_collection
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    main()