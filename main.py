import json
from bs4 import BeautifulSoup
import requests
import schedule
from os.path import exists

url = "https://www.autovit.ro/"
today_list = {}


def check_file():
    file_exits = exists('')
    return file_exits


def create_file(json_obj):
    with open("List.json", "w+") as input_file:
        input_file.write(json_obj)


def update_data(json_obj):
    with open("List.json", "a") as input_file:
        input_file.write(json_obj)


def get_data():
    global url
    global today_list
    list_specs = {}
    page = requests.get(url).text
    file = BeautifulSoup(page, "html.parser")
    section2 = file.find_all(class_="ooa-78awi8 e1gbziix0")
    for car in section2:
        name = car.find(class_="ebw6llc0 ooa-16u688i er34gjf0").get_text()
        price = car.find(class_="ooa-80vtuv er34gjf0").get_text()
        list_specs["price"] = price
        details = file.find(class_="ooa-zzhv62 eknsrtg0").find_all('li')
        year = str(details[0])[10:15]
        list_specs["year"] = year
        km = str(details[1])[10:19]
        list_specs["km"] = km
        today_list[name] = list_specs
    json_obj = json.dumps(today_list, indent=4)
    print(json_obj)
    return json_obj


def main():
    json_obj = get_data()
    if check_file():
        update_data(json_obj)
    else:
        create_file(json_obj)


if __name__ == '__main__':
    main()
    schedule.every(1).day.do(main)
    while True:
        schedule.run_pending()
