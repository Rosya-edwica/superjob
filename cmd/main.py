from mysqldb import get_cities, get_positions, update_position_status
from models import City, Position

from scraper.tools import get_vacancies_count, create_query
from scraper import Scraper
import logging


logging.basicConfig(filename="info.log", filemode='w', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

VACANCY_ON_CITY_LIMIT = 2_000

def main():
    positions = get_positions()
    if len(positions) == 0: logging.fatal("Профессий для парсинга нет")
    for position in positions:
        find_position(position)
        update_position_status(position.Id)

def find_position(position: Position):
    url = create_query(position.Title)
    vacancies_count = get_vacancies_count(url)
    logging.info(f"Для профессии - {position.Title} найдено {vacancies_count} вакансий")
    if vacancies_count > VACANCY_ON_CITY_LIMIT:
        find_position_in_cities(position)
    else: 
        find_position_in_russia(position)

def find_position_in_cities(position: Position):
    for city in cities:
        if city.Name == "Россия": continue
        find_position_in_current_city(position, city, cities)

def find_position_in_russia(position: Position):
    logging.info(f"Ищем профессию - {position.Title} по всей России")
    default_city = City(IdEdwica=0, Abbr="russia", Name="Россия")
    find_position_in_current_city(position, default_city, cities)
    
def find_position_in_current_city(position: Position, city: City, all_cities: list[City]):
    logging.info(f"Ищем профессию - {position.Title} в городе - {city.Name}")
    parser = Scraper(position, city, all_cities)
    parser.start()
    

if __name__ == "__main__":
    cities = get_cities()   
    main()    
    