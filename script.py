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

# Iniciar la función en un hilo separado
threading.Thread(target=actualizar_datos, daemon=True).start()

@app.route('/datos', methods=['GET'])
def obtener_datos():
    """API para obtener los últimos datos almacenados en Firestore."""
    docs = baseDatos.collection('Temperatura').order_by("fecha", direction=firestore.Query.DESCENDING).limit(1).stream()
    data = next(docs, None)
    
    if data:
        return jsonify(data.to_dict())
    else:
        return jsonify({"mensaje": "No hay datos disponibles"}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
