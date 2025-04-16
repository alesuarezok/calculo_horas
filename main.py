from calculo import Calculo
from datetime import datetime
from datetime import timedelta

def opciones():
    print("INGRESA UNA OPCIÓN")
    print("1. Ingresar fecha inicio y fecha fin")
    print("2. Ver las horas trabajadas de una fecha particular")
    print("3. Ver historial de horas trabajadas")
    opcion = input("Opción: ")
    return opcion

def principal():
    opcion = opciones()
    calculo = Calculo()
    if opcion == "1":
        calculo.calculo_horas()
    elif opcion == "2":
        calculo.mostrar_horas_trabajadas_por_fecha()
    elif opcion == "3":
        calculo.mostrar_horas_trabajadas()
    else:
        print("Opción no válida. Intente nuevamente.")
    return opcion


if __name__ == "__main__":
    principal()
