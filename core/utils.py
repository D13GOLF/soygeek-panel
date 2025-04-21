# core/utils.py
import datetime

def obtener_fecha_actual():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def formatear_telefono(chileno_numero):
    """Agrega formato a +56 9 XXXX XXXX"""
    if chileno_numero.startswith("+569") and len(chileno_numero) == 12:
        return f"{chileno_numero[:3]} {chileno_numero[3:4]} {chileno_numero[4:8]} {chileno_numero[8:]}"
    return chileno_numero

def es_email_valido(email):
    import re
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
