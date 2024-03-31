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
    "https://ru.wikipedia.org/wiki/%D0%A1%D1%83%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B_%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D0%B9%D1%81%D0%BA%D0%BE%D0%B9_%D0%A4%D0%B5%D0%B4%D0%B5%D1%80%D0%B0%D1%86%D0%B8%D0%B8"
)
crest_page = wikipedia.page(title="Субъекты_Российской_Федерации")
page_urls = crest_page.images

soup = BeautifulSoup(contents.content, "html.parser")
crest_table = soup.find_all("table")[2]


total = []
ind = 0
for crest_line in crest_table.find_all("tr")[1:]:
    ind += 1
    crest_tds = crest_line.find_all("td")

    image = crest_tds[2]
    name = crest_tds[1]

    state_name = name.text

    print(f"{ind}:{state_name}")
    state_article = unquote(name.find(href=True)["href"]).replace("/wiki/", "")

    images = crest_page.images
    try:
        image_href = image.find(href=True)["href"].split(":")[-1]
    except Exception as e:
        print(f"FAILED: {e}")
        continue

    image_prefix = image_href[: image_href.find("(")]

    coa_urls = [url for url in images if image_prefix in url]
    if len(coa_urls) == 0:
        print(f"SKIP: {state_name}")
        continue

    else:
        image_url = coa_urls[0]

    try:
        city_page = wikipedia.page(title=state_article)
        description = city_page.summary
        borders_img = [
            img
            for img in city_page.images
            if "Map_of_Russia" in img or "in_Russia" in img
        ][0]
        coordinates = (float(city_page.coordinates[0]), float(city_page.coordinates[1]))

    except Exception as e:
        print(f"FAILED TO RETRIVE DESCRIPTION:{e}")
        continue

    data = {
        "title": state_name,
        "crest_url": image_url,
        "bordrs_img": borders_img,
        "description": description,
        "coordinates": coordinates,
    }

    total.append(data)

json.dump(
    total, open("data/crest_states.json", "w", encoding="utf-8"), ensure_ascii=False
)
