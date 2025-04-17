"""
App para registrar y calcular horas trabajadas
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from datetime import datetime, timedelta, date
import sqlite3


class HorasTrabajadas(toga.App):
    def startup(self):
        self.conn = sqlite3.connect('horas_trabajadas.db')
        self.cur = self.conn.cursor()
        self.fecha = date.today()

        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.reiniciar_pantalla()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

    def reiniciar_pantalla(self, widget=None):
        
        self.main_box.children.clear()

        self.hora_inicio_input = toga.TextInput(placeholder='Hora inicio (HH:MM)', style=Pack(padding=5))
        self.hora_fin_input = toga.TextInput(placeholder='Hora fin (HH:MM)', style=Pack(padding=5))

        self.result_label = toga.Label("Horas trabajadas: ", style=Pack(padding=5))
        self.result_label_historial = toga.Label("Horas trabajadas en el mes: ", style=Pack(padding=5))

        calcular_button = toga.Button('Calcular y guardar', on_press=self.calculo_horas, style=Pack(padding=5))
        historial_button = toga.Button('Historial', on_press=self.mostrar_horas_trabajadas, style=Pack(padding=5))
        historial_fecha_button = toga.Button('Historial por fecha', on_press=self.fecha_particular, style=Pack(padding=5))

        self.main_box.add(self.hora_inicio_input)
        self.main_box.add(self.hora_fin_input)
        self.main_box.add(calcular_button)
        self.main_box.add(self.result_label)
        self.main_box.add(historial_button)
        self.main_box.add(self.result_label_historial)
        self.main_box.add(historial_fecha_button)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box


    def inicializar_base_datos(self):
        cur = self.cur
        cur.execute("""
            CREATE TABLE IF NOT EXISTS horas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                hora_inicio TEXT,
                hora_fin TEXT,
                horas_trabajadas TEXT
            )
        """)
        self.conn.commit()

    def calculo_horas(self, widget):
        self.inicializar_base_datos()
        inicio = self.hora_inicio_input.value
        fin = self.hora_fin_input.value
        fecha = str(self.fecha)

        try:
            hora_inicio = datetime.strptime(inicio, "%H:%M")
            hora_fin = datetime.strptime(fin, "%H:%M")
        except ValueError:
            self.result_label.text = "Formato inválido. Usá HH:MM"
            return

        if hora_fin < hora_inicio:
            hora_fin += timedelta(days=1)
        diferencia = hora_fin - hora_inicio
        self.result_label.text = f"Horas trabajadas: {diferencia}"

        self.cur.execute("""
            INSERT INTO horas (fecha, hora_inicio, hora_fin, horas_trabajadas)
            VALUES (?, ?, ?, ?)
        """, (fecha, inicio, fin, str(diferencia)))
        self.conn.commit()

    def mostrar_horas_trabajadas(self, widget):
        self.cur.execute("""
            SELECT sum(horas_trabajadas) FROM horas
            WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now')
        """)
        rows = self.cur.fetchall()
        result = rows[0][0]
#        total = timedelta()

#        for row in rows:
#            try:
#                h, m, s = map(int, row[0].split(":"))
#                total += timedelta(hours=h, minutes=m, seconds=s)
#            except Exception:
#                continue

        self.result_label_historial.text = f"Horas trabajadas en el mes: {result} horas"



    def mostrar_horas_trabajadas_por_fecha(self, widget):
        fecha = self.por_fecha.value.strip()
        if not fecha:
            self.resultado_por_fecha.text = "Ingresá una fecha válida."
            return

        self.cur.execute("SELECT hora_inicio, hora_fin, horas_trabajadas FROM horas WHERE fecha=?", (fecha,))
        rows = self.cur.fetchall()

        if not rows:
            self.resultado_por_fecha.text = f"No hay registros para {fecha}"
            return

        total = timedelta()
        detalle = ""

        for inicio, fin, duracion in rows:
            try:
                h, m, s = map(int, duracion.split(":"))
                total += timedelta(hours=h, minutes=m, seconds=s)
                detalle += f"{inicio} - {fin} ({duracion})\n"
            except Exception:
                continue

        self.resultado_por_fecha.text = f"Horas trabajadas el {fecha}: {total}\n\n{detalle}"
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box

    def fecha_particular(self, widget):
        # Crea un nuevo contenedor en vez de reutilizar el viejo
        self.main_box.children.clear()

        # Reemplazamos la box por una completamente nueva (opcional pero más seguro)
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        self.main_window.content = self.main_box

        self.por_fecha = toga.TextInput(
            placeholder="Ingresa la fecha que quieres consultar (YYYY-MM-DD)",
            style=Pack(padding=7)
        )
        buscar_button = toga.Button('Buscar', on_press=self.mostrar_horas_trabajadas_por_fecha, style=Pack(padding=5))
        volver_button = toga.Button('Volver al inicio', on_press=self.reiniciar_pantalla, style=Pack(padding=5))
        self.resultado_por_fecha = toga.Label("", style=Pack(padding=5))

        self.main_box.add(self.por_fecha)
        self.main_box.add(buscar_button)
        self.main_box.add(volver_button)
        self.main_box.add(self.resultado_por_fecha)



def main():
    return HorasTrabajadas()
