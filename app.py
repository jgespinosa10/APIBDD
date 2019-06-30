from flask import Flask, request, json
from pymongo import MongoClient
from json import dumps
import os
import atexit
import subprocess

USER_KEYS = ['name', 'last_name', 'occupation', 'follows', 'age']
MESS_KEYS = ['id', 'message', 'sender', 'receptant', 'lat', 'long', 'date']
texto = ["incluye", "opcion", "no"]


# Levantamos el servidor de mongo. Esto no es necesario, puede abrir
# una terminal y correr mongod. El DEVNULL hace que no vemos el output
mongod = subprocess.Popen('mongod', stdout=subprocess.DEVNULL)
# Nos aseguramos que cuando el programa termine, mongod no quede corriendo
uri = "mongodb://grupo39:grupo39@146.155.13.149/grupo39?authSource=admin"
atexit.register(mongod.kill)

# El cliente se levanta en localhost:5432
client = MongoClient(uri)
# Utilizamos la base de datos 'api'
db = client["grupo39"]
# # Seleccionamos la colección de usuarios
messages = db.messages
users = db.usuarios

# for i in list(messages.find({}, {"_id":0})):
#     print(str(i).encode("utf-8"))

# Iniciamos la aplicación de flask
app = Flask(__name__)


@app.route("/")
def home():
    str = "<h1>Bienvenido a la API</h1>" \
          "<h3>Para obtener todos los mensajes, entrar a /messages<h3>" \
          "<h3>Para obtener la información del mensaje con id x entrar a /messages/x<h3>" \
          "<h3>Para obtener los mensajes entre dos usuarios de id x e y entrar a /messages/x/y<h3>" \
          "<h3>Para obtener la información del usuario de id x entrar a /user/x<h3>" \
          "<h3>El resto de las consultas deben realizarse mediante PostMan<h3>"
    return str


@app.route("/messages/<int:id>")
def get_messages(id):
    mensaje = list(messages.find({"id": id}, {"_id": 0}))
    return json.jsonify(mensaje)


@app.route("/messages/<int:uid1>/<int:uid2>")
def get_user_mensaje(uid1, uid2):
    mensajes1 = list(messages.find({"$and": [{"sender": uid1}, {"receptant": uid2}]}, {"_id": 0}))
    mensajes2 = list(messages.find({"$and": [{"sender": uid2}, {"receptant": uid1}]}, {"_id": 0}))
    return json.jsonify(mensajes1 + mensajes2)


@app.route("/user/<int:uid>")
def get_user(uid):
    usuario = list(users.find({"usuid": uid}, {"_id": 0}))
    emitidos = list(messages.find({"sender": uid}, {"_id": 0}))
    return json.jsonify(usuario + emitidos)


@app.route("/messages")
def get_message():
    message = list(messages.find({}, {"_id": 0}))
    return json.jsonify(message)


@app.route("/messages", methods=['POST'])
def create_message():
    data = {key: request.json[key] for key in MESS_KEYS}
    count = messages.count_documents({})
    data["id"] = count + 1
    result = messages.insert_one(data)
    if result:
        message = "1 mensaje creado"
        success = True
    else:
        message = "No se pudo crear el mensaje"
        success = False
    return json.jsonify({'success': success, 'message': message})


@app.route('/messages', methods=['DELETE'])
def delete_message():
    _id = {'id': request.json['id']}
    messages.delete_one({"id": _id["id"]})
    message = 'Mensaje con id={} ha sido eliminado.'.format(_id)
    return json.jsonify({'result': 'success', 'message': message})


@app.route('/search')
def buscar():
    text = {key: request.json[key] for key in texto}

    # Esto borra todos los usuarios con el id dentro de la lista4
    incluir = text["incluye"].split("/")

    search = []

    for i in incluir:
        search.append('\"' + i + '\"')

    opcion = text["opcion"].split("/")

    for i in opcion:
        search.append(i)

    no = text["no"].split("/")
    for i in no:
        search.append('-' + i)

    result = dumps(messages.find({"$text": {"$search": ' '.join(search)}}))

    # Retorno el texto plano de un json
    return result


if os.name == '__main__':
    app.run()
