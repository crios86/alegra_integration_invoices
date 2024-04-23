import sqlite3
import hashlib

def crear_tabla():
    # Conectar con la base de datos (si no existe, se creará automáticamente)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Crear la tabla login
    cursor.execute('''CREATE TABLE IF NOT EXISTS login (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )''')

    # Cerrar la conexión
    conn.commit()
    conn.close()

def insertar_usuario(email, password):
    # Conectar con la base de datos
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        # Calcular el hash de la contraseña
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Insertar usuario si el correo electrónico no existe
        cursor.execute("INSERT INTO login (email, password) VALUES (?, ?)", (email, password_hash))
        print("Usuario insertado correctamente.")
    except sqlite3.IntegrityError:
        print("El correo electrónico ya está en uso.")

    # Guardar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

def mostrar_usuarios():
    # Conectar con la base de datos
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Obtener todos los registros de la tabla login
    cursor.execute("SELECT * FROM login")
    usuarios = cursor.fetchall()

    if not usuarios:
        print("No hay usuarios registrados.")
    else:
        print("Usuarios registrados:")
        # Usar un conjunto para almacenar correos electrónicos únicos
        emails_unicos = set()
        for usuario in usuarios:
            if usuario[1] not in emails_unicos:
                emails_unicos.add(usuario[1])
                print(f"ID: {usuario[0]},email: {usuario[1]}, password: {usuario[2]}")

    # Cerrar la conexión
    conn.close()

# Crear la tabla si no existe
crear_tabla()

# # Insertar usuario
# insertar_usuario('crios@unal.edu.co', 'carnifice86')

# # Llamar a la función para mostrar usuarios
# mostrar_usuarios()
