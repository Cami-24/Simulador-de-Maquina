import simpy
import random

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

def proceso(env, nombre, RAM, CPU, vel, tiempos):
     
     #Tiempo en que el proceso llega al sistema
     tiempo_inicio = env.now
     
     # ESTADO NEW
     memoria =random.randint(1,10) #asignacion de memoria ram
     instrucciones = random.randint(1,10) #cant de instrucciones del proceso
     
     print(f"{nombre:10} | llega en {env.now:6.2f}, necesita {memoria} RAM y {instrucciones} instrucciones")
     
     #Pedir memoria RAM
     yield RAM.get(memoria) #si hay memoria continua
                            #si no haym queda detenido hasta que haya memoria disponible
                            
     # ESTADO READY
     while instrucciones > 0:
         
         with CPU.request() as req: #pide CPU
             yield req #espera que el cpu este libre, si esta libre entras, sino espera
             
             # ESTADO RUNNING
             ejecutar = min(vel, instrucciones)
             
             yield env.timeout(1) #1 unidad de tiempo de CPU
             
             instrucciones -= ejecutar #resta las instrucciones ejecutadas
             
             print(f"{nombre} ejecuta {ejecutar} instrucciones; faltan {instrucciones} instrucciones")
             
         #si ya terminó
         if instrucciones <= 0:
            break
        
         #Waiting o ready
         decision = random.randint(1, 21)
        
         if decision == 1:
             #WAITING (simula I/O)
             print(f"{nombre} entra en WAITING")
             yield env.timeout(1) #tiempo de I/O
             
         elif decision == 2:
             #ready
             print(f"{nombre} regresa a ready")
         
         else:
             #tambien vuelve ready
             pass
        
     # ESTADO TERMINATED
     yield RAM.put(memoria) #devuelve la memoria
         
     tiempo_total = env.now - tiempo_inicio
     tiempos.append(tiempo_total)
         
     print(f"{nombre} termina en {env.now}. Tiempo total: {tiempo_total}")



def generador(env, RAM, CPU, vel, tiempos, total_procesos, intervalo):

    for i in range(total_procesos):
        yield env.timeout(random.expovariate(1.0 / intervalo))
        env.process(proceso(env, f"Proceso {i}", RAM, CPU, vel, tiempos))
        

# Configuración de la simulación
import simpy
import random
import statistics

def correr_simulacion(total_procesos, intervalo,
                      RAM=100,
                      vel=3,
                      CPU=1,
                      seed=42):

    # Semilla para reproducibilidad
    random.seed(seed)

    # Crear entorno
    env = simpy.Environment()
    RAM = simpy.Container(env, init=RAM, capacity=RAM)
    CPU = simpy.Resource(env, capacity=CPU)

    tiempos = []

    # Lanzar generador
    env.process(generador(env, RAM, CPU,
                          vel=vel,
                          tiempos=tiempos,
                          total_procesos=total_procesos,
                          intervalo=intervalo))

    # Visual bonito - inicio
    print("="*60)
    print("INICIO DE SIMULACIÓN")
    print("="*60)
    print(f"Procesos: {total_procesos}")
    print(f"Intervalo llegada: {intervalo}")
    print(f"RAM: {RAM.capacity}")
    print(f"CPUs: {CPU.capacity}")
    print(f"Velocidad CPU: {vel} instrucciones/unidad")
    print("="*60)

    env.run()

    # Visual bonito - final
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)

    promedio = statistics.mean(tiempos)
    desviacion = statistics.stdev(tiempos) if len(tiempos) > 1 else 0

    print("\nRESULTADOS FINALES")
    print("-"*40)
    print(f"Procesos simulados : {len(tiempos)}")
    print(f"Tiempo promedio    : {promedio:.2f}")
    print(f"Desviacion estandar: {desviacion:.2f}")
    print("-"*40)

    return promedio, desviacion