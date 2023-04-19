from mysqldb import get_cities, get_positions, update_position_status
from models import City, Position

from scraper.tools import get_vacancies_count, create_query
from scraper import Scraper

VACANCY_ON_CITY_LIMIT = 2_000

def main():
    positions = get_positions()
    if len(positions) == 0: exit("Профессий для парсинга нет")
    for position in positions:
        find_position(position)
        update_position_status(position.Id)

def find_position(position: Position):
    url = create_query(position.Title)
    print(url)
    vacancies_count = get_vacancies_count(url)
    if vacancies_count > VACANCY_ON_CITY_LIMIT:
        find_position_in_cities(position)
    else: 
        find_position_in_russia(position)

def find_position_in_cities(position: Position):
    for city in cities:
        if city.Name == "Россия": continue
        print("Ищем в ", city.Name)
        find_position_in_current_city(position, city, cities)

def find_position_in_russia(position: Position):
    print("Ищем в России")
    default_city = City(IdEdwica=0, Abbr="russia", Name="Россия")
    find_position_in_current_city(position, default_city, cities)
    
def find_position_in_current_city(position: Position, city: City, all_cities: list[City]):
    parser = Scraper(position, city, all_cities)
    parser.start()
    

if __name__ == "__main__":
    cities = get_cities()   
    main()    
    