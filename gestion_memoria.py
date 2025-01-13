import tkinter as tk
from tkinter import messagebox


class Particion:
    def __init__(self, tamaño, id_particion):
        self.tamaño = tamaño
        self.libre = True
        self.proceso = None
        self.id = id_particion


class Proceso:
    def __init__(self, tamaño, id_proceso):
        self.tamaño = tamaño
        self.id = id_proceso


class GestionMemoria:
    def __init__(self, particiones):
        self.particiones = particiones

    def asignar_proceso(self, proceso, algoritmo):
        if algoritmo == "Primer Ajuste":
            return self.primer_ajuste(proceso)
        elif algoritmo == "Mejor Ajuste":
            return self.mejor_ajuste(proceso)
        elif algoritmo == "Peor Ajuste":
            return self.peor_ajuste(proceso)
        else:
            return f"Algoritmo {algoritmo} no reconocido."

    def liberar_proceso(self, id_proceso):
        for particion in self.particiones:
            if particion.proceso and particion.proceso.id == id_proceso:
                particion.libre = True
                particion.proceso = None
                return f"Proceso {id_proceso} liberado de la partición {particion.id}."
        return f"No se encontró el proceso {id_proceso}."

    def primer_ajuste(self, proceso):
        for particion in self.particiones:
            if particion.libre and particion.tamaño >= proceso.tamaño:
                particion.libre = False
                particion.proceso = proceso
                return f"Proceso {proceso.id} asignado a partición {particion.id}."
        return f"No hay partición disponible para el proceso {proceso.id}."

    def mejor_ajuste(self, proceso):
        mejor_particion = None
        for particion in self.particiones:
            if particion.libre and particion.tamaño >= proceso.tamaño:
                if mejor_particion is None or particion.tamaño < mejor_particion.tamaño:
                    mejor_particion = particion

        if mejor_particion:
            mejor_particion.libre = False
            mejor_particion.proceso = proceso
            return f"Proceso {proceso.id} asignado a partición {mejor_particion.id}."
        return f"No hay partición disponible para el proceso {proceso.id}."

    def peor_ajuste(self, proceso):
        peor_particion = None
        for particion in self.particiones:
            if particion.libre and particion.tamaño >= proceso.tamaño:
                if peor_particion is None or particion.tamaño > peor_particion.tamaño:
                    peor_particion = particion

        if peor_particion:
            peor_particion.libre = False
            peor_particion.proceso = proceso
            return f"Proceso {proceso.id} asignado a partición {peor_particion.id}."
        return f"No hay partición disponible para el proceso {proceso.id}."


class InterfazGrafica:
    def __init__(self, root, gestion):
        self.gestion = gestion
        self.root = root
        self.root.title("Gestión de Memoria")

        # Widgets
        self.titulo = tk.Label(root, text="Simulación de Gestión de Memoria JulianDev", font=("Arial", 16))
        self.titulo.pack(pady=10)

        self.frame_opciones = tk.Frame(root)
        self.frame_opciones.pack()

        self.label_proceso = tk.Label(self.frame_opciones, text="Tamaño del proceso (KB):")
        self.label_proceso.grid(row=0, column=0, padx=5, pady=5)
        self.entry_proceso = tk.Entry(self.frame_opciones)
        self.entry_proceso.grid(row=0, column=1, padx=5, pady=5)

        self.label_id = tk.Label(self.frame_opciones, text="ID del proceso:")
        self.label_id.grid(row=1, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(self.frame_opciones)
        self.entry_id.grid(row=1, column=1, padx=5, pady=5)

        self.label_algoritmo = tk.Label(self.frame_opciones, text="Algoritmo:")
        self.label_algoritmo.grid(row=2, column=0, padx=5, pady=5)
        self.algoritmo = tk.StringVar(value="Primer Ajuste")
        self.dropdown_algoritmo = tk.OptionMenu(
            self.frame_opciones, self.algoritmo, "Primer Ajuste", "Mejor Ajuste", "Peor Ajuste"
        )
        self.dropdown_algoritmo.grid(row=2, column=1, padx=5, pady=5)

        self.btn_asignar = tk.Button(root, text="Asignar Proceso", command=self.asignar_proceso)
        self.btn_asignar.pack(pady=5)

        self.btn_liberar = tk.Button(root, text="Liberar Proceso", command=self.liberar_proceso)
        self.btn_liberar.pack(pady=5)

        self.btn_mostrar = tk.Button(root, text="Mostrar Estado", command=self.mostrar_estado)
        self.btn_mostrar.pack(pady=5)

        self.salida = tk.Text(root, height=15, width=50)
        self.salida.pack(pady=10)

    def asignar_proceso(self):
        try:
            tamaño = int(self.entry_proceso.get())
            id_proceso = self.entry_id.get()
            algoritmo = self.algoritmo.get()

            if not id_proceso:
                raise ValueError("Debe ingresar un ID para el proceso.")

            proceso = Proceso(tamaño, id_proceso)
            resultado = self.gestion.asignar_proceso(proceso, algoritmo)
            self.mostrar_mensaje(resultado)
        except ValueError as e:
            self.mostrar_mensaje(f"Error: {str(e)}")

    def liberar_proceso(self):
        id_proceso = self.entry_id.get()
        if not id_proceso:
            self.mostrar_mensaje("Debe ingresar el ID del proceso a liberar.")
            return

        resultado = self.gestion.liberar_proceso(id_proceso)
        self.mostrar_mensaje(resultado)

    def mostrar_estado(self):
        self.salida.delete("1.0", tk.END)
        for particion in self.gestion.particiones:
            estado = "Libre" if particion.libre else f"Ocupada por Proceso {particion.proceso.id}"
            self.salida.insert(tk.END, f"Partición {particion.id} ({particion.tamaño}KB): {estado}\n")

    def mostrar_mensaje(self, mensaje):
        messagebox.showinfo("Resultado", mensaje)


# Configuración inicial
particiones = [
    Particion(100, 1),
    Particion(200, 2),
    Particion(300, 3),
    Particion(400, 4),
]
gestion = GestionMemoria(particiones)

# Crear la interfaz gráfica
root = tk.Tk()
app = InterfazGrafica(root, gestion)
root.mainloop()
