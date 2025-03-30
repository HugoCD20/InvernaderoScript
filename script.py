from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, db
import pytz
import threading
import time
from datetime import datetime

# Inicializar Firebase
cred = credentials.Certificate('credentials/credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invernadero-90934-default-rtdb.firebaseio.com/'
})

baseDatos = firestore.client()
tz = pytz.timezone('America/Mexico_City')

app = Flask(__name__)

def actualizar_datos():
    """Función que corre en segundo plano y actualiza los datos cada 5 minutos."""
    while True:
        try:
            temperatura = db.reference('Temperatura').get()
            humedad = db.reference('Humedad').get()
            now = datetime.now(pytz.utc).astimezone(tz)

            # Convertir a float si los valores no son None
            temperatura = float(temperatura) if temperatura is not None else None
            humedad = float(humedad) if humedad is not None else None

            # Guardar los datos en Firestore con un ID automático
            baseDatos.collection('Temperatura').add({
                'temperatura': temperatura,
                'humedad': humedad,
                'fecha': now.isoformat(),  # Guardamos la fecha en formato ISO
            })

            print(f"Documento agregado en Firestore: {now}")
            time.sleep(3600)  # Esperar una hora

        except Exception as e:
            print(f"Error detectado: {e}")
            time.sleep(10)  # Esperar 10 segundos antes de intentar de nuevo

# Iniciar la función en un hilo separado
threading.Thread(target=actualizar_datos, daemon=True).start()

@app.route('/ping', methods=['GET'])
def ping():
    """Ruta para evitar que Render detenga el servicio."""
    return jsonify({"status": "activo"}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
