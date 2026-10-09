import os
import sys
import json
import urllib.request
import pandas as pd

# Añadir el backend al path para importar los módulos de core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.core_alerta import cargar_diario, anomalia_diaria

# Token de Resend (Se recomienda pasarlo como variable de entorno)
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "re_123456789") # Token de prueba/placeholder
CORREO_DESTINO = os.environ.get("CORREO_DESTINO", "stardust.alx25@gmail.com")

def enviar_correo_resend(asunto, mensaje_html):
    if not RESEND_API_KEY or RESEND_API_KEY == "re_123456789":
        print("[Alerta] Simulando envío de correo (Falta configurar RESEND_API_KEY real)")
        print(f" -> Para: {CORREO_DESTINO}")
        print(f" -> Asunto: {asunto}")
        print(f" -> Cuerpo: {mensaje_html}")
        return

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "PULSO Alertas <onboarding@resend.dev>",
        "to": [CORREO_DESTINO],
        "subject": asunto,
        "html": mensaje_html
    }
    
    req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode("utf-8"))
    try:
        with urllib.request.urlopen(req) as response:
            print("[Resend] Correo enviado exitosamente:", response.read().decode())
    except Exception as e:
        print("[Resend] Error al enviar el correo:", e)

def main():
    print("Evaluando condiciones para alerta automatizada...")
    try:
        df = anomalia_diaria(cargar_diario())
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return

    # Evaluar los últimos 3 días
    ultimos_3_dias = df.tail(3)
    
    if len(ultimos_3_dias) < 3:
        print("No hay suficientes datos (mínimo 3 días) para evaluar la alerta.")
        return

    # Umbral crítico definido por el usuario: +1.5°C por 3 días seguidos
    UMBRAL_CRITICO = 1.5

    supera_umbral = all(ultimos_3_dias['precursor'] > UMBRAL_CRITICO)

    if supera_umbral:
        asunto = "⚠️ Alerta Temprana PULSO: Fase Crítica"
        mensaje = (
            "<h3>⚠️ Alerta Temprana PULSO</h3>"
            "<p>El océano frente a Piura ha entrado en fase crítica (<strong>+1.5°C</strong>). "
            "<strong>Etapa 1 activada.</strong></p>"
            "<p><em>Este es un mensaje automático del sistema de monitoreo satelital.</em></p>"
        )
        print("¡Condición crítica detectada! Disparando alerta por correo...")
        enviar_correo_resend(asunto, mensaje)
    else:
        print("Condiciones estables. No se requiere alerta.")

if __name__ == "__main__":
    main()
