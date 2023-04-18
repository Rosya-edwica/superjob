import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode

import aiohttp

def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')


async def aio_get_soup(url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            return BeautifulSoup(text, "lxml")

def get_vacancies_count(url: str):
    count = 0
    try:
        soup = get_soup(url)
        count_block = soup.find("div", class_="_3-q4I _4J5rK X5K3U _3lgWg")
        count = int(re.findall("\d+", count_block.text)[0])
    except BaseException as err:
        print(f"Ошибка при подсчете вакансий: {err}")
    finally:
        return count    
    

def create_query(positionName: str, cityAbbr: str = None) -> str:
    params = {
        "keywords": positionName,
        "profession_only": 1
    }
    match cityAbbr:
        case None: url = f"https://russia.superjob.ru/vakansii/?{urlencode(params)}"
        case "rabota": url = f"https://superjob.ru/vakansii/?{urlencode(params)}"
        case _: url = f"https://{cityAbbr}.superjob.ru/vakansii/?{urlencode(params)}"
    return url

def get_pages_count(url: str) -> int:
    count = 1
    try:
        soup = get_soup(url)
        count = int(soup.find("div", class_="_3-q4I _9mI07 oSSgx _3SNg7 _364xK _1ApxH _3ybL_").find_all("a")[-2].text)
    except BaseException as err:
        print(f"Ошибка при подсчете количества страниц: {err} {url}")
    finally:
        return count
    
def get_vacancy_urls_from_page(url: str) -> list[str]:
        urls = []
        soup = get_soup(url)
        for item in soup.find_all("div", class_='f-test-search-result-item'):
            block = item.find("div", class_="_3-q4I _4J5rK _2-wuk _3lgWg")
            if not block: continue
            urls.append("https://russia.superjob.ru" + block.find('a')["href"])
        return urls