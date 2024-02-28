import simpy
import random

#Andrés Mazariegos 

# Definición del entorno de simulación
amb = simpy.Environment()

# Definición de la memoria memoria como un contenedor con capacidad limitada
memoria = simpy.Container(amb, init=100, capacity=100)

# Definición de la CPU como un recurso con capacidad limitada
cpu = simpy.Resource(amb, capacity=1)

# Semilla para el generador de números aleatorios
random.seed(42)

# Lista para 
listadeProcesss = []

# Clase para representar un Process
class Process:
    # Constructor de un Process
    def __init__(self, id, cantmemoria, to_do_int):
        self.id = id
        self.cantmemoria = cantmemoria
        self.to_do_int = to_do_int

# Función para agregar un Process al inicio de la lista con su tiempo de llegada
def Processi(lista, id, tiempo):
    lista.insert(0, (id, tiempo))

# Función para agregar un Process al final de la lista con su tiempo de llegada
def Processf(lista, id, tiempo):
    lista.append((id, tiempo))

# Función para crear y ejecutar listadeProcesss
def ejecutar(cantlistadeProcesss, intervalo, amb):
    # Creación de listadeProcesss
    for i in range(cantlistadeProcesss):
        amb.process(nuevoProcess(i, intervalo, amb))

# Función para crear un Process
def nuevoProcess(i, intervalo, amb):
    # Retardo aleatorio antes de la creación del Process
    yield amb.timeout(random.expovariate(1.0 / intervalo))

    # Creación del Process
    Process = Process(i, random.randint(1, 10), random.randint(1, 10))

    # Registrar el inicio del Process
    Processi(listadeProcesss, Process.id, amb.now)

    print(f"Process {Process.id} creado en el tiempo {amb.now}")

    # Ejecutar el Process
    yield amb.process(new(Process))

# Función para ejecutar un Process
def new(current):
    print(f"Process {current.id} pasa al estado 'new'")

    # Solicitar memoria memoria
    with memoria.get(current.cantmemoria) as req:
        yield req

        print(f"Process {current.id} pasa al estado 'ready'")

        # Bucle principal del Process
        while current.to_do_int > 0:

            # Ejecutar una instrucción
            yield amb.process(ready(current))

            # Generar un número aleatorio para determinar la siguiente acción
            numr = random.randint(1, 2)

            # Si el número aleatorio es 1, el Process se coloca en la cola de espera
            if numr == 1:
                # Devolver la memoria memoria
                memoria.put(current.cantmemoria)

                # Esperar un tiempo aleatorio
                yield amb.timeout(2)

                print(f"Process {current.id} pasa al estado 'waiting'")

            # Si el número aleatorio es 2, el Process se coloca en la cola de CPU
            elif numr == 2:
                # Solicitar CPU
                with cpu.request() as req:
                    yield req

                    # Esperar a que la CPU esté disponible
                    yield amb.process(ejecuntando(current))

# Función para ejecutar una instrucción del Process
def ready(current):
    print(f"Process {current.id} pasa al estado 'ready'")
    # Simular la ejecución de una instrucción
    yield amb.timeout(1)

    # Actualizar la cantidad de instrucciones restantes
    current.to_do_int -= 1

# Función para ejecutar el Process en la CPU
def ejecuntando(current):
    print(f"Process {current.id} pasa al estado 'ejecuntando'")

    # Simular la ejecución de tres instrucciones
    for _ in range(3):
        # Verificar si quedan instrucciones por ejecutar
        if current.to_do_int > 0:
            yield amb.timeout(1)
            current.to_do_int -= 1
        else:
            # Si no quedan instrucciones, salir del bucle
            break

