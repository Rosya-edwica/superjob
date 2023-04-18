import aiomysql
from models import Vacancy
import yaml

async def connect():
    yml_data = get_yml_data()
    connection = await aiomysql.connect(
        host=yml_data["db"]["host"], 
        port=yml_data["db"]["port"], 
        user=yml_data["db"]["user"], 
        password=yml_data["db"]["password"], 
        db=yml_data["db"]["dbname"]
    )
    return connection

def get_yml_data() -> dict:
    with open("configs/config.yml", "r") as file:
        yml_data = yaml.safe_load(file)
    return yml_data


async def save_vacancy(v: Vacancy):
    query = f"""INSERT INTO h_vacancy(id, city_id, position_id, salary_from, salary_to, platform, url, name, specs, experience, key_skills, vacancy_date)
        VALUES({v.Id}, {v.City}, {v.PositionId}, {v.Salary.From}, {v.Salary.To}, 'superjob', '{v.Url}', '{v.Title}', '{v.Specialization}', '{v.Experience}', '{"|".join(v.Skills)}', '{v.DateUpdate}')"""
    try:
        connection = await connect()
        cursor = await connection.cursor()
        async with connection.cursor() as cursor:
            await cursor.execute(query)
            await connection.commit()
            print(f"Успешно сохранили вакансию: {v.Id}")
    except BaseException as err:
        print(f"Ошибка при сохранении вакансии: {err}")
    finally:
        connection.close()