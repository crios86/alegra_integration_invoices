from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from form_login import LoginForm, verificar_credenciales
from customer_update import fetch_all_contacts, fetch_customer_names
from items_update import fetch_all_items, create_dataframe, create_sqlite_database, visualizar_productos
from invoice_send import invoces_send_alegra
import pandas as pd

app = Flask(__name__)
app.secret_key = 'crios86'  # Cambia esto a una clave segura

# Ruta para la página principal, redirige al formulario de inicio de sesión
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = verificar_credenciales(email, password)
        if user:
            # Autenticación exitosa, establece la sesión de usuario y redirige
            session['usuario_autenticado'] = True
            return redirect(url_for('formulario'))
        else:
            # Credenciales incorrectas, mostrar un mensaje de error
            return render_template('login.html', form=form, error='Credenciales incorrectas')
    return render_template('login.html', form=form)

# Ruta para el formulario, protegida con autenticación
@app.route('/formulario')
def formulario():
    if 'usuario_autenticado' in session:
        return render_template('formulario.html')
    else:
        return redirect(url_for('login'))

# Resto de tus rutas y funciones sin cambios
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

        return "Facturas procesadas correctamente"  # Devuelve un mensaje de éxito

    except Exception as e:
        return f"Error al procesar las facturas: {str(e)}"      

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
