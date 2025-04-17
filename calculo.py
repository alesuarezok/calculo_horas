from datetime import datetime
from datetime import timedelta
from datetime import date
import sqlite3


class Calculo:
    def __init__(self):
        self.conn = sqlite3.connect('horas_trabajadas.db')
        self.cur = self.conn.cursor()
#        self.execute = self.conn.execute()
        self.fecha = date.today()

    def inicializar_base_datos(self):
        conn = self.conn
        cur = self.cur
        execute = cur.execute
        execute("""
            CREATE TABLE IF NOT EXISTS horas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                hora_inicio TEXT,
                hora_fin TEXT,
                horas_trabajadas TEXT
            )
        """)
        conn.commit()
#        conn.close()


    def calculo_horas(self):
        self.inicializar_base_datos() # Se inicializa la base de datos (se crea la tabla)
        """
        Calcula la diferencia de horas entre dos momentos del día.

        :param hora_inicio: Hora de inicio en formato "HH:MM"
        :param hora_fin: Hora de fin en formato "HH:MM"
        :return: Diferencia de horas como un objeto timedelta
        """
        self.hora_inicio = input("Introduce la hora de inicio (HH:MM): ")
        self.hora_fin = input("Introduce la hora de fin (HH:MM): ")
        fecha = str(self.fecha)
        inicio = self.hora_inicio
        fin = self.hora_fin
        hora_inicio = datetime.strptime(inicio, "%H:%M")
        hora_fin = datetime.strptime(fin, "%H:%M")
        if hora_fin < hora_inicio:
            hora_fin += timedelta(days=1)
        diferencia = hora_fin - hora_inicio

        # Guardar en la base de datos
        conn = self.conn
        cur = self.cur
        execute = cur.execute
        execute("""
            INSERT INTO horas (fecha, hora_inicio, hora_fin, horas_trabajadas)
            VALUES (?, ?, ?, ?)
        """, (fecha, inicio, fin, str(diferencia)))
        conn.commit()
        conn.close()

        return diferencia

    def mostrar_horas_trabajadas(self):
        conn = self.conn
        cur = self.cur
        execute = cur.execute
        execute("SELECT * FROM horas")
        rows = cur.fetchall()
        conn.close()
        print(rows)
        return rows
    def mostrar_horas_trabajadas_por_fecha(self):
        conn = self.conn
        cur = self.cur
        fecha = input("Ingresa la fecha que queres consultar (YYYY-MM-DD): ")
        execute = cur.execute
        execute("SELECT * FROM horas WHERE fecha=?", (fecha,))
        rows = cur.fetchall()
        conn.close()
        print(rows)
        return rows
