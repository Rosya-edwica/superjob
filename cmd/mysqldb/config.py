import pymysql
import yaml


with open("configs/config.yml", "r") as file:
    yml_data = yaml.safe_load(file)


def connect():
    connection = pymysql.connect(
        host=yml_data["db"]["host"], 
        port=yml_data["db"]["port"], 
        user=yml_data["db"]["user"], 
        password=yml_data["db"]["password"], 
        database=yml_data["db"]["dbname"]
    )
    connection.ping()
    return connection
