from flask import Flask, session, request, render_template, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime

def getConnectionToDB():
	client = MongoClient('localhost', 27017)
	return (client, client['DailyPlanet'])

def sortArticleByTime(var):
	return datetime.strptime(var['date'], "%d/%m/%Y - %I:%M%p")

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
		userType = 'reader' if db.User.count() else 'admin'
		db.User.insert_one({
			'name': name, 'email': email, 'password': password, 'type': userType
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
		"type": "aqui el tipo de usuario 'reader', 'author', 'editor', 'admin'"
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
			return jsonify({'status': 'error', 'errorMessage': 'Error #00005 / session[\'data\']', 'email': '', 'name': '', 'type': ''})

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
		# Buscamos si el nuevo email esta disponible.
		if db.User.find_one({'email': request.json['newEmail']}) == None and not theCurrentUser == None:
			# Asiganmos los nuevos valores a las variables.
			userToEdit['email'] = request.json['newEmail'] if request.json['newEmail'] else userToEdit['email']
			userToEdit['name'] = request.json['newName'] if request.json['newName'] else userToEdit['name']
			userToEdit['password'] = request.json['newPassword'] if request.json['newPassword'] else userToEdit['password']
			if theCurrentUser['type'] == 'admin':
				userToEdit['type'] = request.json['newType'] if request.json['newType'] else userToEdit['type']
			# Actualizamos la informacion en la base de datos.
			db.User.update_one({'email': emailModifyUser}, {"$set": userToEdit}, upsert=False)
			# Fijamos el mensaje de exito!
			stringErrorMessage = 'All is fine :P'
			stringStatus = 'success'
			# Si el usuario se esta editando a el mismo cerramos la sesion.
			if emailModifyUser == email:
				session.pop('data', None)
	# Cerramos la conexion con la base de datos.
	client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion edita una publicacion de la base de datos y si el campo de 'id'
	se encuentra 0 entonces crea el articulo.
	Parametro que resibe: {
		"articleContent": "aqui recibimos el texto del articulo en markdown",
		"articleAbstract": "aqui recibimos el resumen del articulo en markdown",
		"articleTitle": "aqui recibimos el titulo del articulo",
		"articleImage": "aqui la direccion a la imagen destacada del articulo",
		"articleCatgory": "aqui ponemos la categoria a la que pertenece el articulo",
		"articleId": "este es el id del articulo",
		"articlePosted": "aqui recibimos si este usuario aprobo el articulo (booleano)"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/article/post', methods=['POST'])
def post():
	stringErrorMessage = 'Error #00007 / session[\'data\']'
	stringStatus = 'error'
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Obtenemos los datos del articulo.
		article = request.json
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		# Verificamos que el usuario tenga los privilegios para crear el articulo.
		if theUser['type'] in ['author', 'admin'] and not article['articleId']:
			# Agregamos el articulo a la base de datos. 
			db.Article.insert_one({
				'content': article['articleContent'],
				'abstract': article['articleAbstract'],
				'title': article['articleTitle'],
				'image': article['articleImage'],
				'category': article['articleCatgory'],
				'time-create': datetime.now().strftime("%d/%m/%Y - %I:%M%p"),
				'time-edited': datetime.now().strftime("%d/%m/%Y - %I:%M%p"),
				'likes': 0,
				'coments': 0,
				'editors': [],
				'author' : email,
				'posted': False
			})
			# Establesemos el mensaje a retornar.
			stringErrorMessage = 'All is fine :P'
			stringStatus = 'success'
		# Verificamos que el usuario tenga los privilegios para editar el articulo.
		elif theUser['type'] in ['editor', 'author', 'admin'] and article['articleId']:
			# Buscamos el articulo enn la base de datos.
			dbArticle = db.Article.find_one(ObjectId(article['articleId']))
			if dbArticle:
				# Verificamos si el usuario tiene privilegios especiales para modificar valores protegidos.
				if theUser['type'] in ['editor', 'admin']:
					dbArticle['posted'] = article['posted']
					# Verificamos si este usuario ya esta en la lista de editores.
					if not theUser['email'] in dbArticle['editors']:
						dbArticle['editors'].append(theUser['email'])
				# Verificamos si el articulo esta publicado y el usuario es editor.
				if not theUser['type'] in ['editor', 'admin'] and dbArticle['posted']:
					client.close()
					return jsonify({'status': 'error', 'errorMessage': 'Error #00008 / Not user capable.'})
				# Fijamos el valor de los elementos modificados para el nuevo articulo.
				dbArticle['title'] = article['articleTitle'] if article['articleTitle'] else dbArticle['title']
				dbArticle['content'] = article['articleContent'] if article['articleContent'] else dbArticle['content']
				dbArticle['abstract'] = article['articleAbstract'] if article['articleAbstract'] else dbArticle['abstract']
				dbArticle['image'] = article['articleImage'] if article['articleImage'] else dbArticle['image']
				dbArticle['category'] = article['articleCatgory'] if article['articleCatgory'] else dbArticle['category']
				dbArticle['time-edited'] = datetime.now().strftime("%d/%m/%Y - %I:%M%p")
				# Actualizamos la informacion en la base de datos.
				db.Article.update_one({'_id': dbArticle['_id']}, {"$set": dbArticle}, upsert=False)
				# Establesemos el mensaje a retornar.
				stringErrorMessage = 'All is fine :P'
				stringStatus = 'success'
			else:
				stringErrorMessage = 'Error #00008 / dbArticle'
				stringStatus = 'error'
		# Cerramos la conexion con la base de datos.
		client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion retorna los articulos que se mostraan en el feed principal.
	Parametros que retorna: [
		{
			"src": "Ubicacion de la imagen.",
			"title": "Titulo del articulo.",
			"category": "Categorias a la que pertenece el articulo.",
			"date": "Fecha de publicacion del articulo.",
			"text": "Abstract del articulo.",
			"autorId": "E-Mail del autor del articulo.",
			"likes": "Cantidad de Likes.",
			"comments": "Cantidad de comentarios.",
			"id": "ID del articulo."
		}, 
		{ ... },
		{ ... }
	]
'''
@app.route('/article/feed', methods=['GET'])
def feed():
	# Creamos la conexion con la base de datos.
	(client, db) = getConnectionToDB()
	# Iniciamos sin un usuario.
	theUser = None
	# Verificamos si tenemos una sesion activa.
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
	# Asignamos donde vamos a obtener el resultado de la consulta.
	articleList = []
	# Verificamos si es un visitante o un usuario registado.
	if theUser :
		# Es un usuario registrado.
		# Obtenemos todos los articulos publicados.
		theArticleList = db.Article.find({'posted': True})
		# Cambiamos el formato de los atributos.
		for article in theArticleList:
			articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
			'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
			'likes': article['likes'], 'coments': article['coments']})
		# Ordenamos por fecha los articulos.
		articleList = sorted(articleList, key=sortArticleByTime, reverse=True)
	else:
		# Es un visitante.
		# Obtenemos todos los articulos publicados.
		theArticleList = db.Article.find({'posted': True})
		# Cambiamos el formato de los atributos.
		for article in theArticleList:
			if datetime.now().date() == datetime.strptime(article['time-create'], "%d/%m/%Y - %I:%M%p").date():
				articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
				'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
				'likes': article['likes'], 'coments': article['coments']})
		# Ordenamos por fecha los articulos.
		articleList = sorted(articleList, key=sortArticleByTime, reverse=True)
	# Cerramos la conexion con la base de datos.
	client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'articles': articleList})

'''
	Esta peticion retorna los articulos que no estan publicados.
	Parametros que retorna: [
		{
			"src": "Ubicacion de la imagen.",
			"title": "Titulo del articulo.",
			"category": "Categorias a la que pertenece el articulo.",
			"date": "Fecha de publicacion del articulo.",
			"text": "Abstract del articulo.",
			"autorId": "E-Mail del autor del articulo.",
			"likes": "Cantidad de Likes.",
			"comments": "Cantidad de comentarios.",
			"id": "ID del articulo."
		}, 
		{ ... },
		{ ... }
	]
'''
@app.route('/article/notposted', methods = ['GET'])
def notposted():
	# Asignamos donde vamos a obtener el resultado de la consulta.
	articleList = []
	# Verificamos si tenemos una sesion activa.
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		#Verificamos que el usuario pueda acceder a los articulos no publicados.
		if theUser['type'] in ['author', 'admin']:
			# Obtenemos todos los articulos no publicados.
			theArticleList = db.Article.find({'posted': False})
			# Cambiamos el formato de los atributos.
			for article in theArticleList:
				articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
				'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
				'likes': article['likes'], 'comments': article['coments']})
			# Ordenamos por fecha los articulos.
			articleList = sorted(articleList, key=sortArticleByTime, reverse=True)
		# Cerramos la conexion con la base de datos.
		client.close()
	# Retornamos la lista de articulos
	return jsonify({'articles': articleList})

'''
	Esta peticion agrega un comentario a la base de datos.
	Parametro que resibe: {
		"commentContent": "aqui recibimos el texto del comentario",
		"IDArticle": "aqui recibimos el id del articulo al que pertenece"
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/comment/post', methods = ['POST'])
def commpost():
	stringErrorMessage = 'Error #00007 / session[\'data\']'
	stringStatus = 'error'
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Obtenemos los datos del comentario.
		comment = request.json
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		# Agregamos el comentario a la base de datos.
		db.Comment.insert_one({
			'content': comment['commentContent'],
			'article': comment['IDArticle'],
			'user':  email,
			'date': datetime.now().strftime("%d/%m/%Y - %I:%M%p")
		})
		# Establesemos el mensaje a retornar.
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
		# Cerramos la conexion con la base de datos.
		client.close()
		# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion devuelve la lista de comentarios asociados al articulo seleccionado.
	Parametro que resibe: {
		"IDArticle": "aqui recibimos el id del articulo",
	}
	Parametros que retorna: [
		{
			"id": "id del comentario",
			"content": "Contenido del comentario",
			"article": "id del articulo al que pertenece",
			"user": "email del usuario que lo publico",
			"date": "fecha de publicacion del articulo."
		}, 
		{ ... },
		{ ... }
	]
'''
@app.route('/comment/get', methods = ['POST'])
def commget():
	# Creamos la conexion con la base de datos.
	(client, db) = getConnectionToDB()
	#Obtenemos el artículo del cual queremos mostrar sus comentarios.
	article = request.json
	# Asignamos donde vamos a obtener el resultado de la consulta.
	commentList = []
	# Obtenemos todos los comentarios publicados en el artículo.
	theCommentList = db.Comment.find({'article': article['IDArticle']})
	#Cambiamos el formato de los atributos.
	for comment in theCommentList:
		commentList.append({'id': str(comment['_id']), 'content': comment['content'], 'article': comment['article'], 'user': comment['user'], 'date': comment['date']})
	#Ordenamos los comentarios por fecha.
	commentList = sorted(commentList, key = sortArticleByTime)
	# Cerramos la conexion con la base de datos.
	client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'comments': commentList})

if __name__ == '__main__':
	app.run(host='localhost', port=80, debug=True)
