"""
Este programa va a crear procesos, va a simularlo con memoria ram, usara cpu
manejara los estados y calculará el tiempo total de cada proceso e el sistema.

env: entorno simpy
nombre: identificar el proceso
RAM: pide y devuelve memoria
CPU: solicitar uso de procesador
vel: velocidad del proceso (instrucciones por unidad de Tiempo)
tiempos: guarda el registro de tiempos del proceso
"""

def proceso(env, nombre, RAM, CPU):
    