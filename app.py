from flask import Flask, session, request, render_template, jsonify
from pymongo import MongoClient

def getConnectionToDB():
	client = MongoClient('localhost', 27017)
	return (client, client['DailyPlanet'])

app = Flask(__name__)
app.secret_key = 'VanfH8STX0i0a6I0a4CYF93LoM1Eh6ST6gOa08mio0GrVdU3xYR3Vtfj9kkpj8p5'

'''
	Esta es la peticion encargada de cargar la pagina WEB.
'''
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

'''
	Esta peticion agrega un nuevo usuario en la base de datos
	por defecto el tipo de usuario es 'user'.
	Parametro que resibe: {
		"email": "aqui el correo electronico",
		"name": "aqui el nombre del usuario",
		"password": "aqui la contrasena"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/sigin', methods=['POST'])
def sigin():
	# Creamos la conexxion con la base de datos.
	(client, db) = getConnectionToDB()
	# Obtenemos los datos de la peticion.
	name = request.json['name']
	email = request.json['email']
	password = request.json['password']
	# Buscamos al usuario en la base de datos.
	userExist = db.User.find_one({'email': email})
	# Preparamos los mensajes que va a retornar la peticion.
	stringStatus = stringErrorMessage = ''
	# Verificamos si el usuario ya existe en la base de datos.
	if userExist == None:
		# El usuario no existe en la base de datos.
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
		# Agregamos al usuario a la base de datos.
		db.User.insert_one({
			'name': name, 'email': email, 'password': password, 'type':'user'
			})
	else:
		# El usuario ya existe, preparamos los mensajes de error.
		stringErrorMessage = 'Error #00001 / userExist'
		stringStatus = 'error'
	# Cerramos la conexion con la base de datos.
	client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion autentica al usuario de la solicitud en
	la base de datos y de coincidir crea la sesion.
	Parametro que resibe: {
		"email": "aqui el correo electronico",
		"password": "aqui la contrasena"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/login', methods=['POST'])
def login():
	# Creamos la conexion con la base de datos.
	(client, db) = getConnectionToDB()
	# Obtenemos los datos de la peticion.
	email = request.json['email']
	password = request.json['password']
	# Buscamos al usuario en la base de datos.
	theUser = db.User.find_one({'email': email, 'password': password})
	# Cerramos la conexion con la base de datos.
	client.close()
	# Preparamos los mensajes que va a retornar la peticion.
	stringStatus = stringErrorMessage = ''
	if 'data' in session:
		# Ya el usuario tiene una sesion activa.
		stringErrorMessage = 'Error #00002 / session[\'data\']'
		stringStatus = 'error'
	elif not theUser == None:
		# Encontramos al usuario, sus credenciales son corectas, creamos la sesion.
		session['data'] = {'email': theUser['email'], 'password': theUser['password']}
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
	else:
		# No encontramos al usuario en la base de datos.
		stringErrorMessage = 'Error #00003 / login()'
		stringStatus = 'error'
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion borra la sesion de usuario.
	Parametros que retorna: {
		"status": "success",
		'errorMessage': "All is fine :P"
	}
'''
@app.route('/logout', methods=['GET'])
def logout():
	# Borramos la informacion de la cookies del usuario.
	session.pop('data', None)
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': 'success', 'errorMessage': 'All is fine :P'})

'''
	[GET]
	Esta peticion obtiene la informacion del usuario actual.
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
		"email": "aqui el correo electronico",
		"name": "aqui el nombre del usuario",
		"type": "aqui el tipo de usuario"
	}
	[POST]
	Esta peticion obtiene la informacion del usuario indicado.
	Parametro que resibe: {
		"email": "aqui el correo electronico"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
		"email": "aqui el correo electronico",
		"name": "aqui el nombre del usuario",
		"type": "aqui el tipo de usuario"
	}
'''
@app.route('/user/info', methods=['GET', 'POST'])
def info():
	if request.method == 'GET':
		stringErrorMessage = 'Error #00004 / session[\'data\']'
		stringStatus = 'error'
		email = name = UserType = ''
		if 'data' in session:
			# El usuario tiene una sesion activa.
			# Creamos la conexion con la base de datos.
			(client, db) = getConnectionToDB()
			# Obtenemos los datos de la sesion.
			email = session['data']['email']
			password = session['data']['password']
			# Buscamos al usuario en la base de datos.
			theUser = db.User.find_one({'email': email, 'password': password})
			# Cerramos la conexion con la base de datos.
			client.close()
			# Asignamos los valores de las variables.
			email = theUser['email']
			name = theUser['name']
			UserType = theUser['type']
			stringErrorMessage = 'All is fine :P'
			stringStatus = 'success'
		# Devolvemos el resultado de la peticion.
		return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage, 'email': email, 'name': name, 'type': UserType})
	if request.method == 'POST':
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la peticion.
		email = request.json['email']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email})
		# Cerramos la conexion con la base de datos.
		client.close()
		# Verificamos si encontramos al usuario en la base de datos.
		if not theUser == None:
			# Asignamos los valores de las variables.
			email = theUser['email']
			name = theUser['name']
			UserType = theUser['type']
			# Devolvemos el resultado de la peticion.
			return jsonify({'status': 'success', 'errorMessage': 'All is fine :P', 'email': email, 'name': name, 'type': UserType})
		else:
			return jsonify({'status': 'success', 'error': 'Error #00005 / theUser'})

'''
	Esta peticion modifica la informacion del usuario.
	Parametro que resibe: {
		"email": "aqui el correo electronico",
		"newEmail": "aqui el correo electronico",
		"newName": "aqui el nombre del usuario",
		"newPassword": "aqui la contrasena",
		"newType": "aqui el tipo de usuario"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/user/edit', methods=['POST'])
def edit():
	stringErrorMessage = 'Error #00006 / session[\'data\']'
	stringStatus = 'error'
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Obtenemos los datos del usuario a modificar.
		emailModifyUser = request.json['email']
		# Buscamos al usuario en la base de datos.
		theCurrentUser = db.User.find_one({'email': email, 'password': password})
		# Buscamos al usuario que queremos editar.
		userToEdit = db.User.find_one({'email': emailModifyUser})
		# Asiganmos los nuevos valores a las variables.
		userToEdit['email'] = request.json['newEmail'] if request.json['newEmail'] else userToEdit['email']
		userToEdit['name'] = request.json['newName'] if request.json['newName'] else userToEdit['name']
		userToEdit['password'] = request.json['newPassword'] if request.json['newPassword'] else userToEdit['password']
		if theCurrentUser['type'] == 'admin':
			userToEdit['type'] = request.json['newType'] if request.json['newType'] else userToEdit['type']
		# Actualizamos la informacion en la base de datos.
		db.User.update_one({'email': emailModifyUser}, {"$set": userToEdit}, upsert=False)
		# Cerramos la conexion con la base de datos.
		client.close()
		# Fijamos el mensaje de exito!
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
		# Devolvemos el resultado de la peticion.
		return jsonify({'status': stringStatus, 'error': stringErrorMessage})

if __name__ == '__main__':
	app.run(port=80, debug=True)