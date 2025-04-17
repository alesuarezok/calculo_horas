"""
App para registrar y calcular horas trabajadas
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from datetime import timedelta
from datetime import date
import sqlite3
import time


class HorasTrabajadas(toga.App):
    def startup(self):
        self.conn = sqlite3.connect('horas_trabajadas.db')
        self.cur = self.conn.cursor()
        self.fecha = date.today()


        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.hora_inicio_input = toga.TextInput(placeholder='Hora inicio (HH:MM)', style=Pack(padding=5))
        self.hora_fin_input = toga.TextInput(placeholder='Hora fin (HH:MM)', style=Pack(padding=5))

        self.result_label = toga.Label("Horas trabajadas: ", style=Pack(padding=5))
        self.result_label_historial = toga.Label("Horas trabajadas en el mes: ", style=Pack(padding=5))
        self.resultado_por_fecha = toga.Label("Horas trabajadas en la fecha: ", style=Pack(padding=5))

        calcular_button = toga.Button(
            'Calcular y guardar',
            on_press=self.calculo_horas,
            style=Pack(padding=5)
        )
        historial_button = toga.Button(
            'Historial',
            on_press=self.mostrar_horas_trabajadas,
            style=Pack(padding=5)
        )
        historial_fecha_button = toga.Button(
            'Historial por fecha',
            on_press=self.fecha_particular,
            style=Pack(padding=5)
        )

        self.main_box.add(self.hora_inicio_input)
        self.main_box.add(self.hora_fin_input)
        self.main_box.add(calcular_button)
        self.main_box.add(self.result_label)
        self.main_box.add(historial_button)
        self.main_box.add(self.result_label_historial)
        self.main_box.add(historial_fecha_button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()                

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


    def calculo_horas(self,widget):
        self.inicializar_base_datos() # Se inicializa la base de datos (se crea la tabla)
        """
        Calcula la diferencia de horas entre dos momentos del día.

        :param hora_inicio: Hora de inicio en formato "HH:MM"
        :param hora_fin: Hora de fin en formato "HH:MM"
        :return: Diferencia de horas como un objeto timedelta
        """
        self.hora_inicio = self.hora_inicio_input.value
        self.hora_fin = self.hora_fin_input.value
        fecha = str(self.fecha)
        inicio = self.hora_inicio
        fin = self.hora_fin
        hora_inicio = datetime.strptime(inicio, "%H:%M")
        hora_fin = datetime.strptime(fin, "%H:%M")
        if hora_fin < hora_inicio:
            hora_fin += timedelta(days=1)
        diferencia = hora_fin - hora_inicio
        self.result_label.text = f"Horas trabajadas: {diferencia}"

        # Guardar en la base de datos
        conn = self.conn
        cur = self.cur
        execute = cur.execute
        execute("""
            INSERT INTO horas (fecha, hora_inicio, hora_fin, horas_trabajadas)
            VALUES (?, ?, ?, ?)
        """, (fecha, inicio, fin, str(diferencia)))
        conn.commit()
        #conn.close()
        return diferencia
    



    def mostrar_horas_trabajadas(self, widget):
        """
        Muestra todas las horas trabajadas en un mes registradas en la base de datos.
        :return: Lista de horas trabajadas
        """
        conn = self.conn
        cur = self.cur
        execute = cur.execute
        execute("""SELECT sum(horas_trabajadas) FROM horas
                WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
                GROUP BY strftime('%Y-%m', fecha)        
                """)
        rows = cur.fetchall()
        rows = rows[0]
        print(rows)
        self.result_label_historial.text = f"Horas trabajadas en el mes: {rows[0]}"
        return rows
    
    def mostrar_horas_trabajadas_por_fecha(self, widget):
        fecha = self.str_fecha
        

        conn = self.conn
        cur = self.cur
#        fecha = input("Ingresa la fecha que queres consultar (YYYY-MM-DD): ")
        execute = cur.execute
        execute(f"SELECT * FROM horas WHERE fecha='{fecha}'")
        rows = cur.fetchall()

        print(rows)
        self.resultado_por_fecha.text = f"Horas trabajadas en la fecha {fecha}: {rows}"
        self.main_box.add(self.resultado_por_fecha)        
        return
    
    def fecha_particular(self, widget):
#        self.por_fecha_title = toga.Label("Ingresa la fecha que quieres consultar en formato (YYYY-MM-DD): ", style=Pack(padding=5))
        self.por_fecha = toga.TextInput(placeholder="Ingresa la fecha que quieres consultar en formato (YYYY-MM-DD): ", style=Pack(padding=7))
#        self.main_box.add(self.por_fecha_title)
        self.main_box.add(self.por_fecha)
        fecha = self.por_fecha.value
        self.str_fecha = str(fecha)
        horas_trabajadas_button = toga.Button(
            'Buscar',
            on_press=self.mostrar_horas_trabajadas_por_fecha,
            style=Pack(padding=5)
        )
        self.main_box.add(horas_trabajadas_button)        
        return 
    
def main():
    return HorasTrabajadas()
