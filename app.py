from flask import Flask, render_template, request, jsonify
from customer_update import fetch_all_contacts, fetch_customer_names,visualizar_clientes
from items_update import fetch_all_items, create_dataframe, create_sqlite_database,visualizar_productos
from invoice_send import invoces_send_alegra
import pandas as pd


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

        invoces_send_alegra(df=df)

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
