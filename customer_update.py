import sqlite3
import requests
import os
import pandas as pd

def fetch_contacts(start_index):
    url = f"https://api.alegra.com/api/v1/contacts?metadata=false&start={start_index}&order_direction=ASC"
    headers = {
        "accept": "application/json",
        "authorization": "Basic bWVyY2Fkb2Fncmljb2xhZGVsYXNpZXJyYTNAZ21haWwuY29tOjI0MTFmYTQ3NzUyMjRjYTkyNWNk"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch contacts from start index {start_index}. Status code: {response.status_code}")
        return []

def create_database():
    if not os.path.exists('clientes.db'):
        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE clientes
                     (ID TEXT, Name TEXT, NIT TEXT, PhonePrimary TEXT, KindOfPerson TEXT, Email TEXT, Regime TEXT, Address TEXT)''')
        conn.commit()
        conn.close()

def fetch_all_contacts():
    create_database()  
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    all_contacts = []
    start_index = 0
    while True:
        contacts = fetch_contacts(start_index)
        if not contacts:
            break
        all_contacts.extend(contacts)
        start_index += len(contacts)
    for customer in all_contacts:
        c.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (customer.get('id', ''),
                   customer.get('name', ''),
                   customer.get('identification', ''),
                   customer.get('phonePrimary', ''),
                   customer.get('kindOfPerson', ''),
                   customer.get('email', ''),
                   customer.get('regime', ''),
                   customer.get('address', {}).get('address', '')))
    conn.commit()
    conn.close()
    return all_contacts

def fetch_customer_names():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute("SELECT Name FROM clientes")
    names = [row[0] for row in c.fetchall()]
    conn.close()
    return names

def visualizar_clientes():
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect('clientes.db')
        
        # Leer los datos en un DataFrame
        df = pd.read_sql_query("SELECT * FROM clientes", conexion)

        return df

    except sqlite3.Error as error:
        print("Error al conectar a la base de datos:", error)
    finally:
        # Cerrar la conexión
        if conexion:
            conexion.close()