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

            doc_ref = baseDatos.collection('Temperatura').document(str(now))
            doc_ref.set({
                'temperatura': str(temperatura),
                'humedad': str(humedad),
                'fecha': str(now),
            })

            print(f"Documento actualizado en Firestore: {now}")
            time.sleep(300)  # Esperar 5 minutos

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
