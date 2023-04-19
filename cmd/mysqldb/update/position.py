from mysqldb.config import connect


def update_position_status(positionId: int):
    query = f"UPDATE h_position SET parsed=true WHERE position_id={positionId}"

    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(f"Спарсили профессию {positionId}")
    except BaseException as err:
        print(f"Ошибка при обновлении статуса профессии: {err}")
    finally:
        connection.close()