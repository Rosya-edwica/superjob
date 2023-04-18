import re
from bs4 import BeautifulSoup

import asyncio

import scraper.tools as tools
from models import *
from mysqldb.insert.vacancy import save_vacancy


class Scraper:
    def __init__(self, position: Position, city: City, all_cities: list[City]):
        self.position = position
        self.defaultCity = city
        self.all_cities = all_cities
    
    def start(self):
        url = tools.create_query(self.position.Title, self.defaultCity.Abbr)    
        pages_count = tools.get_pages_count(url)
        for page in range(pages_count):
            asyncio.run(self.parse_page(f"{url}&page={page}"))


    async def parse_page(self, url: str):
        urls = tools.get_vacancy_urls_from_page(url)
        tasks = [self.parse_vacancy(url) for url in urls]
        await asyncio.gather(*tasks)
    
    async def parse_vacancy(self, url: str):
        soup = await tools.aio_get_soup(url)
        try:
            
            vacancy = Vacancy(
                Id=int(re.findall("\d+", url)[0]),
                Title=soup.find("h1", class_="_1c5Bu Qtbsi PZF7Y _2MAQA _1m76X _3UZoC _1_71a").text,
                Skills=self.get_skills(soup),
                DateUpdate=soup.title.text.split("опубликована")[-1].strip(),
                Url=url,
                City=self.get_city(soup),
                PositionId=self.position.Id,
                Experience=self.get_experience(soup),
                Specialization=soup.find("span", class_="RRZVI _3UZoC _3zdq9 _3iH_l").text.split("/")[2].strip(),
                Salary=self.get_salary(soup)
            )
            await save_vacancy(vacancy)

        except BaseException as err:
            print(f"Ошибка при разборе вакансии:\nUrl:{url}\nErr:{err}")
            return None
        return vacancy
    
    def get_city(self, soup: BeautifulSoup) -> int:
        cityName = soup.find("div", class_="f-test-address _3hvu1 _PIrV _2L8th").text.split(",")[0]
        try:
            city_id = next(city.IdEdwica for city in self.all_cities if city.Name == cityName.strip().lower())
        except StopIteration:
            city_id = self.defaultCity.IdEdwica
        return city_id
        
    def get_experience(self, soup: BeautifulSoup) -> str:
        for i in soup.find_all("span", class_="_2Ltia _3UZoC _3iH_l"):
            if "Опыт" in i.text:
                return i.text.replace("Опыт работы ", "")

    def get_skills(self, soup: BeautifulSoup) -> list[str]:
        try:
            skills = [skill.text for skill in soup.find("span", class_="_39I1Z RRZVI _3UZoC _3zdq9 _3iH_l _3u9kN").find_all("ul")[1].find_all("li")]
        except:
            skills = []
        finally:
            return skills

    def get_salary(self, soup: BeautifulSoup) -> Salary:
        text = re.sub(u"\u00A0", u"", soup.find("span", class_="_2eYAG _1m76X _3UZoC _3iH_l").text)
        digits = re.findall("\d+", text)
        if digits:
            if len(digits) == 2:
                return Salary(To=int(digits[1]), From=int(digits[0]))
            return Salary(To=int(digits[0]), From=0)
        return Salary(0, 0)