import eel
import serial
import mysql.connector
import serial.tools.list_ports

conSerial = None
ports = []
portsSerial = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(portsSerial):
        ports.append({ "port": port, "description": desc })

conn_mysql = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='controle_entrada',
)

cursor = conn_mysql.cursor()

"""
select r.id, r.plate, r.date_entry, r.status_delivery, r.status_deliveryman, u.name, u.tower, u.apartment from registers r join users u on r.user_id = u.id where r.status_deliveryman in (1, 2) order by r.status_deliveryman;
"""

@eel.expose
def get_ports():
    return ports

@eel.expose
def connection(port_con):
    global conSerial
    conSerial = serial.Serial(port_con, 9600)
    print(f'Conectou com sucesso: {port_con}')

@eel.expose
def disconnect():
    conSerial.close()
    print(f'Desconectou com sucesso')

@eel.expose
def open(id):
    cursor.execute(f"UPDATE registers SET status_deliveryman=2 WHERE id = {id}")
    conn_mysql.commit()
    conSerial.write(b'open')

@eel.expose
def close():
    conSerial.write(b'close')

@eel.expose
def get_registers():
    registers = []

    cursor.execute("""
    select r.id, r.plate, r.date_entry, r.status_delivery, r.status_deliveryman, u.name, u.tower, u.apartment 
    from registers r join users u on r.user_id = u.id 
    where r.status_deliveryman in (1, 2) 
    order by r.status_deliveryman
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

    conn_mysql.commit()

    return registers

eel.init('web')
eel.start('index.html')
