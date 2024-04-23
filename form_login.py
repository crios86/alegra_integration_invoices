from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email ,InputRequired
import sqlite3

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),InputRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(),InputRequired()])
    submit = SubmitField('Iniciar sesión')


def users_credentials():
    try:
        # Conectar con la base de datos
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Obtener todas las filas de la tabla login
        cursor.execute("SELECT email, password FROM login")
        users_rows = cursor.fetchall()

        # Cerrar la conexión
        conn.close()

        # Crear un diccionario para almacenar las credenciales de los usuarios
        users_dict = {}
        for row in users_rows:
            email = row[0]
            password = row[1]
            users_dict[email] = password

        return users_dict

    except sqlite3.Error as error:
        print("Error de base de datos:", error)
        return None




