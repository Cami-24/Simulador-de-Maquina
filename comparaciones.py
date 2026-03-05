from SimuladorMaquina import correr_simulacion
import matplotlib.pyplot as plt

procesos_prueba = [25, 50, 100, 150, 200]
intervalos = [10, 5, 1]

for intervalo in intervalos:

    normal = []
    mas_ram = []
    cpu_rapido = []
    dos_cpu = []

    for n in procesos_prueba:

        p1, _ = correr_simulacion(n, intervalo=intervalo)
        normal.append(p1)

        p2, _ = correr_simulacion(n, intervalo=intervalo, RAM=200)
        mas_ram.append(p2)

        p3, _ = correr_simulacion(n, intervalo=intervalo, vel=6)
        cpu_rapido.append(p3)

        p4, _ = correr_simulacion(n, intervalo=intervalo, CPU=2)
        dos_cpu.append(p4)

    plt.figure()
    plt.plot(procesos_prueba, normal, marker='o', label="Normal")
    plt.plot(procesos_prueba, mas_ram, marker='o', label="RAM 200")
    plt.plot(procesos_prueba, cpu_rapido, marker='o', label="CPU más rápido")
    plt.plot(procesos_prueba, dos_cpu, marker='o', label="2 CPUs")

    plt.xlabel("Número de procesos")
    plt.ylabel("Tiempo promedio")
    plt.title(f"Comparación estrategias - Intervalo {intervalo}")
    plt.legend()
    plt.grid(True)
    plt.show()