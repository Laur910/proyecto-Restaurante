import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Deja esto vacío si estás usando XAMPP sin contraseña
        database="alamesa"
    )

# Crear las tablas si no existen
def inicializar_bd():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mesas (
        id INT AUTO_INCREMENT PRIMARY KEY,
        numero INT UNIQUE,
        disponible BOOLEAN
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredientes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100),
        cantidad INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pedidos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        mesa_id INT,
        estado VARCHAR(50),
        fecha DATETIME,
        FOREIGN KEY (mesa_id) REFERENCES mesas(id)
    )
    ''')

    conn.commit()
    conn.close()

inicializar_bd()

# Aplicación principal
class ALaMesaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A la Mesa - Gestión de Restaurante")
        self.root.geometry("600x500")
        self.root.configure(bg="#f4f4f4")

        self.estilizar_interfaz()

        tab_control = ttk.Notebook(root)
        self.tab_mesas = ttk.Frame(tab_control)
        self.tab_pedidos = ttk.Frame(tab_control)
        self.tab_inventario = ttk.Frame(tab_control)

        tab_control.add(self.tab_mesas, text='Mesas')
        tab_control.add(self.tab_pedidos, text='Pedidos')
        tab_control.add(self.tab_inventario, text='Inventario')
        tab_control.pack(expand=1, fill='both')

        self.crear_tab_mesas()
        self.crear_tab_pedidos()
        self.crear_tab_inventario()

    def estilizar_interfaz(self):
        style = ttk.Style()
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        else:
            style.theme_use('default')

        style.configure("TNotebook", background="#f4f4f4", padding=10)
        style.configure("TNotebook.Tab", background="#e0e0e0", padding=10, font=('Arial', 10, 'bold'))
        style.configure("TFrame", background="#f4f4f4")
        style.configure("TLabel", background="#f4f4f4", font=('Arial', 10))
        style.configure("TButton", background="#4CAF50", foreground="white", padding=6, font=('Arial', 10, 'bold'))
        style.map("TButton", background=[("active", "#45a049")])

    def crear_tab_mesas(self):
        frame = ttk.Frame(self.tab_mesas, padding=20)
        frame.pack(pady=40)

        ttk.Label(frame, text="Número de Mesa:").grid(row=0, column=0, padx=5, pady=5)
        self.num_mesa = ttk.Entry(frame)
        self.num_mesa.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Agregar Mesa", command=self.agregar_mesa).grid(row=1, column=0, columnspan=2, pady=10)

    def agregar_mesa(self):
        numero = self.num_mesa.get()
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mesas (numero, disponible) VALUES (%s, %s)", (numero, True))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Mesa {numero} agregada.")
            self.num_mesa.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la mesa: {e}")

    def crear_tab_pedidos(self):
        frame = ttk.Frame(self.tab_pedidos, padding=20)
        frame.pack(pady=40)

        ttk.Label(frame, text="ID Mesa:").grid(row=0, column=0, padx=5, pady=5)
        self.mesa_id = ttk.Entry(frame)
        self.mesa_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Estado:").grid(row=1, column=0, padx=5, pady=5)
        self.estado = ttk.Combobox(frame, values=["pendiente", "servido"])
        self.estado.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Registrar Pedido", command=self.registrar_pedido).grid(row=2, column=0, columnspan=2, pady=10)

    def registrar_pedido(self):
        mesa = self.mesa_id.get()
        estado = self.estado.get()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pedidos (mesa_id, estado, fecha) VALUES (%s, %s, %s)", (mesa, estado, fecha))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Pedido registrado para mesa {mesa}.")
            self.mesa_id.delete(0, tk.END)
            self.estado.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el pedido: {e}")

    def crear_tab_inventario(self):
        frame = ttk.Frame(self.tab_inventario, padding=20)
        frame.pack(pady=40)

        ttk.Label(frame, text="Ingrediente:").grid(row=0, column=0, padx=5, pady=5)
        self.ingrediente = ttk.Entry(frame)
        self.ingrediente.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.cantidad = ttk.Entry(frame)
        self.cantidad.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Agregar Ingrediente", command=self.agregar_ingrediente).grid(row=2, column=0, columnspan=2, pady=10)

    def agregar_ingrediente(self):
        nombre = self.ingrediente.get()
        cantidad = self.cantidad.get()

        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO ingredientes (nombre, cantidad) VALUES (%s, %s)", (nombre, cantidad))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"{nombre} agregado al inventario.")
            self.ingrediente.delete(0, tk.END)
            self.cantidad.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el ingrediente: {e}")

# Ejecutar la app
if __name__ == "__main__":
    root = tk.Tk()
    app = ALaMesaApp(root)
    root.mainloop()
