import eel
import serial
import mysql.connector
import serial.tools.list_ports

conSerial = None
ports = []
portsSerial = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(portsSerial):
        ports.append({ "port": port, "description": desc })

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='controle_entrada',
)

cursor = conexao.cursor()

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
    global conSerial
    conSerial.close()
    print(f'Desconectou com sucesso')

@eel.expose
def send_command(id):
    global conSerial
    print(f'Passou em sendcommand: {id}')

@eel.expose
def get_registers():
    global cursor
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

    return registers

eel.init('web')
eel.start('index.html')
