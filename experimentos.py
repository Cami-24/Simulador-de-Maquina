from SimuladorMaquina import correr_simulacion
import matplotlib.pyplot as plt

intervalos = [10, 5, 1]
procesos_prueba = [25, 50, 100, 150, 200]

for intervalo in intervalos:

    procesos_lista = []
    promedios = []

    for n in procesos_prueba:
        promedio, _ = correr_simulacion(n, intervalo=intervalo)
        procesos_lista.append(n)
        promedios.append(promedio)

    plt.figure()
    plt.plot(procesos_lista, promedios, marker='o')
    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promedio")
    plt.title(f"Intervalo = {intervalo}")
    plt.grid(True)
    plt.show()