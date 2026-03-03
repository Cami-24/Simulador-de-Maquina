from SimuladorMaquina import correr_simulacion
import matplotlib.pyplot as plt

procesos_lista = []
promedios = []

for n in [25, 50, 100, 150, 200]:
    promedio, _ = correr_simulacion(n, intervalo=10)
    procesos_lista.append(n)
    promedios.append(promedio)

plt.plot(procesos_lista, promedios, marker='o')
plt.xlabel("Número de procesos")
plt.ylabel("Tiempo promedio")
plt.title("Procesos vs Tiempo promedio")
plt.grid(True)
plt.show()