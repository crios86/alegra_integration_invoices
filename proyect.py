import os

def imprimir_estructura_directorio(directorio, nivel=0):
    for elemento in os.listdir(directorio):
        ruta_completa = os.path.join(directorio, elemento)
        if os.path.isdir(ruta_completa):
            print("  " * nivel + "|_" + elemento + "/")
            imprimir_estructura_directorio(ruta_completa, nivel + 1)
        else:
            print("  " * nivel + "|_" + elemento)

directorio_proyecto = r"C:\Users\Cris Ríos\Desktop\alegra_integration_invoices"  # Nota el prefijo 'r' aquí
print("Estructura del proyecto:")
imprimir_estructura_directorio(directorio_proyecto)
