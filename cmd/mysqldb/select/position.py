from models import Position

from mysqldb.config import connect

def get_positions() -> list[Position]:
    connection = connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT position_id, name, other_names FROM h_position WHERE parsed = false")
        positions = [Position(*item) for item in cursor.fetchall()]
    connection.close()
    
    return positions