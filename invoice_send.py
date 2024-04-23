import requests
import pandas as pd
from datetime import datetime
from customer_update import visualizar_clientes
from items_update import visualizar_productos


def invoces_send_alegra(df):
    try:
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
            
            # enviar por correo
            url = "https://api.alegra.com/api/v1/invoices/"+ str(id) +"/email"

            payload = {
                "emailMessage": { "subject": "Factura Johan R" },
                "emails": ["criosriosm86@gmail.com"]
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Basic your_api_key"
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.text)

        return "facturas electrónicas de venta han sido emitidas exitosamente"
    except:
        return 'Error al procesar facturas'
