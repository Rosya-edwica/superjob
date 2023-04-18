from models import City

from mysqldb.config import connect

def get_cities() -> list[City]:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_edwica, id_rabota_ru, name FROM h_city WHERE id_rabota_ru != ''")
        cities = [City(*item) for item in cursor.fetchall()]
    connection.close()
    
    return cities


