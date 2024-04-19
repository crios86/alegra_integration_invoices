from flask import Flask, render_template, request, jsonify
from customer_update import fetch_all_contacts, fetch_customer_names,visualizar_clientes
from items_update import fetch_all_items, create_dataframe, create_sqlite_database,visualizar_productos
import pandas as pd
from datetime import datetime
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/customer_names')
def get_customer_names():
    names = fetch_customer_names()
    return jsonify(names)

@app.route('/product_names')
def get_product_names():
    all_items = fetch_all_items()
    product_names = [item.get('name', '') for item in all_items]
    return jsonify(product_names)

@app.route('/procesar_facturas', methods=['POST'])
def procesar_facturas():
    try:

        # Obtener los datos del formulario
        razones_sociales = request.form.getlist('razon_social')
        nombres_productos = request.form.getlist('nombre_producto')
        cantidades = request.form.getlist('cantidad')
        nombres_establecimientos = request.form.getlist('nombre_establecimiento')
        numeros_orden = request.form.getlist('num_orden')

        # Crear un DataFrame con los datos
        data = {

                'razon_social': razones_sociales,
                'nombre_producto': nombres_productos,
                'cantidad': cantidades,
                'nombre_establecimiento': nombres_establecimientos,
                'numero_orden': numeros_orden
                
                }

        df = pd.DataFrame(data)
        print(df)

        clientes = visualizar_clientes().drop_duplicates()
        nuevos_nombres = {'ID': 'codigo_cliente', 'Name': 'nombre_cliente'}
        clientes = clientes.rename(columns=nuevos_nombres)
        productos = visualizar_productos().drop_duplicates()
        nuevos_nombres = {'ID': 'codigo_producto', 'Name': 'nombre', 'UnitCost':'precio_unitario'}
        productos = productos.rename(columns=nuevos_nombres)
        pedidos_df = df.copy()

        cod_cliente = []
        for razon_social in list(pedidos_df['razon_social']):
            resultado_loc = clientes.loc[clientes['nombre_cliente'] == razon_social]
            cod_cliente.append(resultado_loc['codigo_cliente'].iloc[0])

        cod_producto = []
        for nombre_producto in list(pedidos_df['nombre_producto']):
            resultado_loc = productos.loc[productos['nombre'] == nombre_producto]
            cod_producto.append(resultado_loc['codigo_producto'].iloc[0])

        unit_price = []
        for nombre_producto in list(pedidos_df['nombre_producto']):
            resultado_loc = productos.loc[productos['nombre'] == nombre_producto]
            unit_price.append(resultado_loc['precio_unitario'].iloc[0])

        df_codigos = {
                        'codigo_cliente' :cod_cliente,
                        'codigo_producto' : cod_producto,
                        'precio_unitario' :unit_price,
                        'fecha_creacion'  : datetime.now().strftime('%Y-%m-%d')
                    }
        
        df_codigos = pd.DataFrame(df_codigos)
        pedidos_df = pd.concat([pedidos_df, df_codigos], axis=1)

        # Eliminar filas con valores NaN
        pedidos_df.dropna(inplace=True)

        # Conversión de tipos de datos
        pedidos_df = pedidos_df.dropna().astype({'codigo_cliente': int, 'codigo_producto': int, 'cantidad': int, 'precio_unitario': int})

        for codigo_cliente in pedidos_df['codigo_cliente'].unique():
            df = pedidos_df[pedidos_df['codigo_cliente'] == codigo_cliente]
            items = []
            for _, row in df.iterrows():
                id_item = str(row['codigo_producto'])
                quantity = row['cantidad']
                url = f"https://api.alegra.com/api/v1/items/{id_item}"
                headers = {
                    "accept": "application/json",
                    "authorization": "Basic your_api_key"
                }
                response_item = requests.get(url, headers=headers).json()
                item = {
                    "id": int(response_item['id']),
                    "quantity": int(row['cantidad']),
                    "price": int(response_item['price'][0]['price'])
                }
                items.append(item)

            payload = {
                "status": "open",
                "paymentForm": "CASH",
                "paymentMethod": "CASH",
                "client": {"id": int(df['codigo_cliente'].iloc[0])},
                "date": df['fecha_creacion'].iloc[0],
                "dueDate": df['fecha_creacion'].iloc[0],
                "items": items,
                "anotation": df['nombre_establecimiento'].iloc[0] + ', ' + df['numero_orden'].iloc[0]
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Basic your_api_key"
            }
            response = requests.post("https://api.alegra.com/api/v1/invoices", json=payload, headers=headers)
            response_json = response.json()
            
            id = int(response_json['id'])

            url = "https://api.alegra.com/api/v1/invoices/stamp"
            payload = { "ids": [id] }
            headers = {
                        "accept": "application/json",
                        "authorization": "Basic your_api_key",
                        "content-type": "application/json"
                    }
            
            response = requests.post(url, json=payload, headers=headers)
            response_invoice = response.json()
            print(response_invoice)

        return "facturas electrónicas de venta han sido emitidas exitosamente"
    except:
        return "Error  al enviar las Facturas, intente de nuevo"

@app.route('/actualizar_clientes')
def actualizar_clientes():
    # Ejecutar el script Python para actualizar la base de datos de clientes
    try:
        fetch_all_contacts()
        return "Base de datos de clientes actualizada correctamente"
    
    except Exception as e:
        return f"Error al actualizar la base de datos de clientes: {str(e)}"

@app.route('/actualizar_productos')
def actualizar_productos():
    # Ejecutar el script Python para actualizar la base de datos de productos
    try:
        all_items = fetch_all_items()
        items_df = create_dataframe(all_items)
        create_sqlite_database(items_df)
        return "Base de datos de productos actualizada correctamente"
    except Exception as e:
        return f"Error al actualizar la base de datos de productos: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
