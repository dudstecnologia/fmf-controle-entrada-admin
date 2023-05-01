import eel
import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='controle_entrada',
)

cursor = conexao.cursor()

"""
select r.id, r.plate, r.date_entry, r.status_delivery, r.status_deliveryman, u.name, u.tower, u.apartment from registers r join users u on r.user_id = u.id where r.status_deliveryman in (1, 2);
"""

@eel.expose
def get_registers():
    global cursor
    registers = []

    cursor.execute("""
    select r.id, r.plate, r.date_entry, r.status_delivery, r.status_deliveryman, u.name, u.tower, u.apartment 
    from registers r join users u on r.user_id = u.id 
    where r.status_deliveryman in (1, 2)
    """)

    for r in cursor.fetchall():
        register = {
            "id": r[0],
            "plate": r[1],
            "date_entry": r[2].strftime("%m/%d/%Y, %H:%M:%S"),
            "status_delivery": r[3],
            "status_deliveryman": r[4],
            "name": r[5],
            "tower": r[6],
            "apartment": r[7]
        }
        registers.append(register)

    return registers

eel.init('web')
eel.start('index.html')
