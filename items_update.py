import requests
import pandas as pd
import sqlite3
import pandas as pd

def fetch_items(start_index):
    url = f"https://api.alegra.com/api/v1/items?metadata=false&start={start_index}&order_direction=ASC"
    headers = {
        "accept": "application/json",
        "authorization": "Basic bWVyY2Fkb2Fncmljb2xhZGVsYXNpZXJyYTNAZ21haWwuY29tOjI0MTFmYTQ3NzUyMjRjYTkyNWNk"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch items from start index {start_index}. Status code: {response.status_code}")
        return []

def fetch_all_items():
    all_items = []
    start_index = 0
    while True:
        items = fetch_items(start_index)
        if not items:
            break
        all_items.extend(items)
        start_index += len(items)
    return all_items

def create_dataframe(all_items):
    # Extract the data of each item and store them in a list of lists
    items = []
    for item in all_items:
        item_id = item.get('id', '')
        item_name = item.get('name', '')
        # Extract unit cost from the price object
        unit_cost = None
        price_info = item.get('price', [{}])[0]  # Get the first price object or an empty dictionary if no price is available
        if price_info:
            unit_cost = price_info.get('price', '')
        items.append([item_id, item_name, unit_cost])

    # Define the column names
    columns = ['ID', 'Name', 'UnitCost']

    # Create the DataFrame
    items_df = pd.DataFrame(items, columns=columns)
    return items_df

def create_sqlite_database(items_df, db_name='productos.db'):
    # Create SQLite database if not exists
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Check if table already exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
    table_exists = c.fetchone()

    if not table_exists:
        # Create table if not exists
        c.execute('''CREATE TABLE productos
                     (ID TEXT, Name TEXT, UnitCost REAL)''')

    # Insert DataFrame into SQLite
    items_df.to_sql('productos', conn, if_exists='append', index=False)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' created and data inserted successfully")


def update_products_db():
    # Actualizar la base de datos de productos
    all_items = fetch_all_items()
    items_df = create_dataframe(all_items)
    create_sqlite_database(items_df)

def visualizar_productos():
    try:
        # Conectar a la base de datos
        conexion = sqlite3.connect('productos.db')
        
        # Leer los datos en un DataFrame
        df = pd.read_sql_query("SELECT * FROM productos", conexion)

        # Imprimir el DataFrame
        return df

    except sqlite3.Error as error:
        print("Error al conectar a la base de datos:", error)
    finally:
        # Cerrar la conexión
        if conexion:
            conexion.close()
