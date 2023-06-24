import fake_headers
import requests
import bs4
import lxml
import re
from pprint import pprint
import black
import csv
import json

data = {}
data["vacancy"] = []

headers = fake_headers.Headers(browser="firefox", os="win")
headers_dict = headers.generate()
pages_count = range(0, 40)
for i in pages_count:
    main_html = requests.get(
        f"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={i}",
        headers=headers_dict,
    )
    html = main_html.text
    main_soup = bs4.BeautifulSoup(html, "lxml")
    main_content = main_soup.find_all("div", class_="serp-item")

    vacancy_list = []
    link_list = []
    django_str = "Django"
    flask_str = "Flask"

    for vacancy in main_content:
        vacancy_body = vacancy.find("div", class_="vacancy-serp-item-body")
        title_tag = vacancy_body.find("a", class_="serp-item__title")

        link = title_tag["href"]
        link_list.append(link)

        title = title_tag.text

        company_city = vacancy_body.find_all("div", class_="bloko-text")
        company = company_city[0].text
        city = company_city[1].text

        salary = vacancy_body.find("span", class_="bloko-header-section-3")

        # вариант с зарплатой в рублях
        if django_str in title or flask_str in title:
            if salary == None:
                data["vacancy"].append(
                    {
                        "link": str(link),
                        "salary": str(salary),
                        "company": str(company),
                        "city": str(city),
                    }
                )
                print("ok")
            else:
                data["vacancy"].append(
                    {
                        "link": str(link),
                        "salary": str(salary.text),
                        "company": str(company),
                        "city": str(city),
                    }
                )
                print("ok")

        # # Вариант с зарплатой в долларах
        if django_str in title or flask_str in title:
            if salary == None:
                pass
            elif "$" in salary:
                data["vacancy"].append(
                    {
                        "link": str(link),
                        "salary": str(salary.text),
                        "company": str(company),
                        "city": str(city),
                    }
                )


with open("data.json", "w") as f:
    json.dump(data, f)
