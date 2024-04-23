from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email ,InputRequired
import hashlib
import sqlite3

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(),InputRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(),InputRequired()])
    submit = SubmitField('Iniciar sesión')


def verificar_credenciales(email, password):
    try:
        # Conectar con la base de datos
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Calcular el hash de la contraseña ingresada
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Buscar el usuario en la base de datos por email y contraseña hash
        cursor.execute("SELECT * FROM login WHERE email = ? AND password = ?", (email, password_hash))
        user = cursor.fetchone()

        # Cerrar la conexión
        conn.close()

        return user

    except sqlite3.Error as error:
        print("Error de base de datos:", error)
        return None



print(verificar_credenciales('crios@unal.edu.co', 'carnifice86'))