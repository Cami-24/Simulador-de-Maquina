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
     
     print(f"{nombre} llega en {env.now}, necesita {memoria} RAM y {instrucciones} instrucciones")
     
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
         tiempos.append((nombre, tiempo_total))
         
         print(f"{nombre} terminó en {env.now}. Tiempo total: {tiempo_total}")



def generador(env, RAM, CPU, vel, tiempos, total_procesos, intervalo):

    for i in range(total_procesos):
        yield env.timeout(random.expovariate(1.0 / intervalo))
        env.process(proceso(env, f"Proceso {i}", RAM, CPU, vel, tiempos))
        

# Configuración de la simulación
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

env = simpy.Environment()
RAM = simpy.Container(env, init=100, capacity=100)
CPU = simpy.Resource(env, capacity=1)

tiempos = []

env.process(generador(env, RAM, CPU, vel=3, tiempos=tiempos,
                      total_procesos=25, intervalo=10))

env.run()

print("Promedio:", sum(tiempos)/len(tiempos))