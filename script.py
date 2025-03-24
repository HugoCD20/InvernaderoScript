import firebase_admin
from firebase_admin import credentials, firestore,db
import time
from datetime import datetime
import pytz
cred = credentials.Certificate('credentials/credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invernadero-90934-default-rtdb.firebaseio.com/' 
})

baseDatos = firestore.client()
tz = pytz.timezone('America/Mexico_City')


while True:
    temperatura = db.reference('Temperatura')
    humedad = db.reference('Humedad')

    Temperatura = temperatura.get()
    Humedad = humedad.get()
    now = datetime.now(pytz.utc).astimezone(tz)

    doc_ref = baseDatos.collection('Temperatura').document(str(now))

    # Establecer datos
    doc_ref.set({
        'temperatura': str(Temperatura),
        'humedad': str(Humedad),
        'fecha': str(now),
    })

    print(f"Documento creado con ID: {now}")

    time.sleep(60)

