from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore, db
import pytz
from datetime import datetime

# Inicializar Firebase
cred = credentials.Certificate('credentials/credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invernadero-90934-default-rtdb.firebaseio.com/'
})

baseDatos = firestore.client()
tz = pytz.timezone('America/Mexico_City')

app = Flask(__name__)

@app.route('/datos', methods=['GET'])
def obtener_datos():
    temperatura = db.reference('Temperatura').get()
    humedad = db.reference('Humedad').get()
    now = datetime.now(pytz.utc).astimezone(tz)

    return jsonify({
        'temperatura': temperatura,
        'humedad': humedad,
        'fecha': str(now)
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
