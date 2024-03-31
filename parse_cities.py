import json
import time
from urllib.parse import unquote

import lxml.html.clean
import pandas as pd
import requests
import wikipedia
from bs4 import BeautifulSoup

wikipedia.set_lang("ru")

contents = requests.get(
    "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BE%D0%B2_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B8"
)
crest_page = wikipedia.page(title="Список_городов_России")
page_urls = crest_page.images

soup = BeautifulSoup(contents.content, "html.parser")
crest_table = soup.find("table")


total = []
ind = 0
for crest_line in crest_table.find_all("tr")[1:]:
    ind += 1
    crest_tds = crest_line.find_all("td")

    image = crest_tds[1]
    name = crest_tds[2]

    city_name = name.text
    print(f"{ind}:{city_name}")
    city_article = unquote(name.find(href=True)["href"]).replace("/wiki/", "")

    images = crest_page.images
    image_href = image.find(href=True)["href"].split(":")[-1]

    image_prefix = image_href[: image_href.find("(")]

    coa_urls = [url for url in images if image_prefix in url]
    if len(coa_urls) == 0:
        print(f"SKIP: {city_name}")
        continue

    else:
        image_url = coa_urls[0]

    try:
        city_page = wikipedia.page(title=city_article)
        description = city_page.summary

        coordinates = (float(city_page.coordinates[0]), float(city_page.coordinates[1]))

    except Exception as e:
        print(f"FAILED TO RETRIVE DESCRIPTION:{e}")
        continue

    data = {
        "title": city_name,
        "crest_url": image_url,
        "description": description,
        "coordinates": coordinates,
    }

    total.append(data)

json.dump(total, open("data/crest.json", "w", encoding="utf-8"), ensure_ascii=False)
