from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
import sqlite3
import hashlib


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Verificar credenciales de usuario en la base de datos
def verificar_credenciales(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Cifrar la contraseña antes de verificarla
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM login WHERE email = ? AND password = ?", (email, password_hash))
    user = cursor.fetchone()
    conn.close()
    return user
