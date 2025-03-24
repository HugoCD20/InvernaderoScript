import firebase_admin
from firebase_admin import credentials, firestore,db
import time
import datetime
cred = credentials.Certificate('credentials/credenciales.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://invernadero-90934-default-rtdb.firebaseio.com/' 
})

baseDatos = firestore.client()


while True:
    temperatura = db.reference('Temperatura')
    humedad = db.reference('Humedad')

    Temperatura = temperatura.get()
    Humedad = humedad.get()
    now = datetime.datetime.now()

    doc_ref = baseDatos.collection('Temperatura').document(str(now))

    # Establecer datos
    doc_ref.set({
        'temperatura': str(Temperatura),
        'humedad': str(Humedad),
        'fecha': str(now),
    })

    print(f"Documento creado con ID: {now}")

    time.sleep(60)

