# Entrega 4

###### Integrantes:

1. Nicolás Azócar
2. Macarena Concha
3. Juan Guillermo Espinoza
4. Michel Magna
5. Daniela Oteiza

Para hacer funcionar la api (suponiendo que las bases de datos ya están importadas, si no lo están, seguir instrucciones de la guía de Mongo del curso. Para importar usuarios usamos la colección -usuarios-  y para mensajes usamos la colección -messages-):

1.- Crear VirtualEnviroment en la carpeta Entrega4 mediante pipenv install (entrar a la carpeta en la terminal y usar ese comando)

2.- Instalar los paquetes flask, pymongo, pandas, matplotlib, gunicorn, mediante:

- pipenv install flask
- pipenv install pymongo
- pipenv install pandas
- pipenv install matplotlib
- pipenv install gunicorn

3.- Correr gunicorn - en caso de Mac- :

- gunicorn main:app --workers=3 --reload

4.- Entrar a localhost



**En <main.py> están todos los comandos necesarios para correr las consultas.** 

Respecto a main.py tenemos lo siguiente: 

1. Decoradores del tipo @app.route: Abajo de éstos aparecen otras funciones como def home. Para acceder a ellas hay que ir a la ruta que aparece en paréntesis:
   Ej: @app.route("/users"), hay que ir a localhost:8000/users

2. Además tenemos distintas funciones, dentro de cada función se define lo que va a aparecer en la página, y se pueden usar búsquedas y comandos de pymongo con las bases que ya se tienen instaladas. Hay que hacer esto con todos los querys que pide el enunciado. A continuación el detalle de cada una:
   - def home():  Muestra básicamente el inicio de nuestra API. La usamos para ver si la conexión fue realizada correctamente. Además de indicar las rutas de las otras funciones. 
   - def get_messages(id): Se obtienen todos los mensajes con un id específico. Para esto tuvimos que pasar primero la base de datos -en formato json- por un código python para que agregue un id. 
   - def get_user_mensaje(uid1, uid2): Entrega todos los mensajes enviados entre dos uid's de usuarios, tanto de remitente como emisor.
   - def get_user(uid): Se obtiene la información tanto del usuario como de los mensajes enviados por este. *La base de datos usuarios la pasamos de csv a json con un convertidor online antes de cargarla*
   - def get_message(): Se obtiene todos los mensajes de la base de datos. Función que utilizamos para corroborar que las otras funciones están correctas.  
   - def create_message(): Se crea un mensaje entre dos usuarios. Es necesario utilizar Postman. 
   - def delete_message(): Borra un mensaje de la id ingresada. Es necesario utilizar Postman.
   - def buscar(): Función encargada de text-search. Es necesario que las palabras o frases esten separadas por /, ya que usamos split de este. Además dentro de esta misma función, esta la posibilidad de incluir, opción y no, que se refiere a cada pedido de la entrega 4. 