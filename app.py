from flask import Flask, session, request, render_template, jsonify, url_for
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'VanfH8STX0i0a6I0a4CYF93LoM1Eh6ST6gOa08mio0GrVdU3xYR3Vtfj9kkpj8p5'
app.config['UPLOAD_FOLDER'] = './static/upload/'

def getConnectionToDB():
	client = MongoClient('localhost', 27017)
	return (client, client['DailyPlanet'])

def sortByTime(var):
	return datetime.strptime(var['date'], "%d/%m/%Y - %I:%M%p")

def sortByFav(var):
	return var['likes']

def sortByComment(var):
	return var['comments']

def simpleSearch(db, article, query):
	if not article['title'].lower().find(query.lower()) == -1:
		return True
	if not article['key-words']. lower().find(query.lower()) == -1:
		return True
	author = db.User.find_one({'email': article['author']})
	if author and not author['name'].lower().find(query.lower()) == -1:
		return True
	if author and not author['email'].lower().find(query.lower()) == -1:
		return True
	return False

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
			'name': name, 'email': email, 'password': password, 'type': userType, 'favorites': [], 'image': '', 'description': ''
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
		"type": "aqui el tipo de usuario",
		"favorites": [arreglo con los ids de los articulos favoritos]
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
			favorites = theUser['favorites']
			image = theUser['image']
			description = theUser['description']
			stringErrorMessage = 'All is fine :P'
			stringStatus = 'success'
		# Devolvemos el resultado de la peticion.
		return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage, 'email': email, 'name': name, 'type': UserType, 'favorites': favorites, 'image': image, 'description': description})
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
			image = theUser['image']
			favorites = theUser['favorites']
			description = theUser['description']
			# Devolvemos el resultado de la peticion.
			return jsonify({'status': 'success', 'errorMessage': 'All is fine :P', 'email': email, 'name': name, 'type': UserType, 'favorites': favorites, 'image': image, 'description': description})
		else:
			return jsonify({'status': 'error', 'errorMessage': 'Error #00005 / session[\'data\']', 'email': '', 'name': '', 'type': '', 'favorites': [], 'image': '', 'description': ''})

'''
	Esta peticion modifica la informacion del usuario y cierra la session
	Parametro que resibe: {
		"email": "aqui el correo electronico",
		"newName": "aqui el nombre del usuario",
		"newPassword": "aqui la contrasena",
		"newType": "aqui el tipo de usuario",
		"newImage: "aqui la url de la nueva imagen",
		"newDescription": "aqui la descripcion del usuario"
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
		# Buscamos al usuario en la base de datos.
		theCurrentUser = db.User.find_one({'email': email, 'password': password})
		# Buscamos al usuario que queremos editar.
		userToEdit = db.User.find_one({'email': request.json['email']})
		# Buscamos si el nuevo email esta disponible.
		if not theCurrentUser == None:
			print(userToEdit)
			# Asiganmos los nuevos valores a las variables.
			userToEdit['name'] = request.json['newName'] if request.json['newName'] else userToEdit['name']
			userToEdit['password'] = request.json['newPassword'] if request.json['newPassword'] else userToEdit['password']
			userToEdit['image'] = request.json['newImage'] if request.json['newImage'] else userToEdit['image']
			userToEdit['description'] = request.json['newDescription'] if request.json['newDescription'] else userToEdit['description']
			if theCurrentUser['type'] == 'admin':
				userToEdit['type'] = request.json['newType'] if request.json['newType'] else userToEdit['type']
			# Actualizamos la informacion en la base de datos.
			db.User.update_one({'email': request.json['email']}, {"$set": userToEdit}, upsert=False)
			# Fijamos el mensaje de exito!
			stringErrorMessage = 'All is fine :P'
			stringStatus = 'success'
			# Si el usuario se esta editando a el mismo cerramos la sesion.
			if request.json['email'] == email:
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
		"articlePosted": "aqui recibimos si este usuario aprobo el articulo (booleano)",
		"articleKeyWords": "aqui ponemos las palabras claves del articulo"
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
				'posted': False,
				'key-words': article['articleKeyWords']
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
				dbArticle['key-words'] = article['articleKeyWords'] if article['articleKeyWords'] else dbArticle['key-words']
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
			'likes': article['likes'], 'coments': article['coments'], 'title': article['title']})
		# Ordenamos por fecha los articulos.
		articleList = sorted(articleList, key=sortByFav, reverse=True)
	else:
		# Es un visitante.
		# Obtenemos todos los articulos publicados.
		theArticleList = db.Article.find({'posted': True})
		# Cambiamos el formato de los atributos.
		for article in theArticleList:
			if datetime.now().date() == datetime.strptime(article['time-create'], "%d/%m/%Y - %I:%M%p").date():
				articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
				'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
				'likes': article['likes'], 'coments': article['coments'], 'title': article['title']})
		# Ordenamos por fecha los articulos.
		articleList = sorted(articleList, key=sortByFav, reverse=True)
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
		if theUser['type'] in ['author', 'admin', 'editor']:
			#Verificamos si es un autor.
			if theUser['type'] == 'author':
				# Obtenemos todos los articulos no publicados creados por ese autor.
				theArticleList = db.Article.find({'posted': False, 'autorID': email})
				# Cambiamos el formato de los atributos.
				for article in theArticleList:
					articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
					'date': article['time-create'], 'text': article['abstract'], 'author': article['author'],
					'likes': article['likes'], 'comments': article['coments'], 'title': article['title']})
				# Ordenamos por fecha los articulos.
				articleList = sorted(articleList, key=sortByTime, reverse=True)
			else:
				# Obtenemos todos los articulos no publicados.
				theArticleList = db.Article.find({'posted': False})
				# Cambiamos el formato de los atributos.
				for article in theArticleList:
					articleList.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
					'date': article['time-create'], 'text': article['abstract'], 'author': article['author'],
					'likes': article['likes'], 'comments': article['coments'], 'title': article['title']})
				# Ordenamos por fecha los articulos.
				articleList = sorted(articleList, key=sortByTime, reverse=True)
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
		if theUser:
			# Obtenemos el articulo comentado.
			theArticle = db.Article.find_one(ObjectId(comment['IDArticle']))
			if theArticle:
				# Aumentamos el numero de comentarios en el articulo.
				theArticle['coments'] = theArticle['coments'] + 1
				# Actualizamos la informacion del articulo.
				db.Article.update_one({'_id': ObjectId(comment['IDArticle'])}, {"$set": theArticle}, upsert=False)
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
	commentList = sorted(commentList, key = sortByTime)
	# Cerramos la conexion con la base de datos.
	client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'comments': commentList})

'''
	Esta peticion retorna el articulo indicado segun su 'id'.
	Parametro que resibe: {
		"IDArticle": "aqui recibimos el id del articulo",
	}
	Parametros que retorna: {
			"src": "Ubicacion de la imagen.",
			"title": "Titulo del articulo.",
			"category": "Categorias a la que pertenece el articulo.",
			"date": "Fecha de publicacion del articulo.",
			"text": "Abstract del articulo.",
			"autorId": "E-Mail del autor del articulo.",
			"likes": "Cantidad de Likes.",
			"comments": "Cantidad de comentarios.",
			"id": "ID del articulo."
		}
'''
@app.route('/article/get', methods = ['POST'])
def getart():
	#Creamos el JSON donde ira el articulo a retornar.
	article = {}
	#Almacenamos el id del articulo deseado.
	idArticle = request.json
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
	#Buscamos el articulo solicitado.
	theArticle = db.Article.find_one(ObjectId(idArticle['IDArticle']))
	#Verificamos si es un articulo que ya ha sido publicado.
	if theUser:
		#Es un usuario registrado.
		if theArticle['posted']:
			#El articulo esta publicado.
			#Almacenamos los campos del articulo.
			article = {'id': str(theArticle['_id']), 'src': theArticle['image'], 'category': theArticle['category'],
				'date': theArticle['time-create'], 'text': theArticle['content'], 'autorId': theArticle['author'],
				'likes': theArticle['likes'], 'comments': theArticle['coments'], 'title': theArticle['title'], 
				'editors': theArticle['editors'], 'key-words': theArticle['key-words']}
		else:
			#El articulo no esta publicado.
			#Verificamos si el usuario tiene permisos para ver articulos no publicados.
			if theUser['type'] in ['author', 'admin', 'editor']:
				#Verificamos si es el autor del articulo.
				if theUser['type'] == 'author':
					if theArticle['author'] == email:
						#Es el autor del articulo.
						article = {'id': str(theArticle['_id']), 'src': theArticle['image'], 'category': theArticle['category'],
							'date': theArticle['time-create'], 'text': theArticle['abstract'], 'author': theArticle['author'],
							'likes': theArticle['likes'], 'comments': theArticle['coments'], 'key-words': theArticle['key-words']}
				#Los editores y admin pueden acceder al articulo.
				else:
					article = {'id': str(theArticle['_id']), 'src': theArticle['image'], 'category': theArticle['category'],
				'date': theArticle['time-create'], 'text': theArticle['content'], 'autorId': theArticle['author'],
				'likes': theArticle['likes'], 'comments': theArticle['coments'], 'title': theArticle['title'], 
				'editors': theArticle['editors'], 'key-words': theArticle['key-words']}
	else:
		#Es un usuario visitante.
		if theArticle['posted']:
			#El articulo esta publicado.
			#Verificamos que sea un articulo del dia para que lo pueda acceder el visitante.
			if datetime.now().date() == datetime.strptime(theArticle['time-create'], "%d/%m/%Y - %I:%M%p").date():
				#Almacenamos los campos del articulo.
				article = {'id': str(theArticle['_id']), 'src': theArticle['image'], 'category': theArticle['category'],
				'date': theArticle['time-create'], 'text': theArticle['content'], 'autorId': theArticle['author'],
				'likes': theArticle['likes'], 'comments': theArticle['coments'], 'title': theArticle['title'], 
				'editors': theArticle['editors']}
	# Cerramos la conexion con la base de datos.
	client.close()
	#Retornamos la respuesto
	return jsonify({'article': article})

'''
	Agrega el articulo seleccionado a la lista de favoritos del usuario.
	Parametro que resibe: {
		"IDArticle": "aqui recibimos el id del articulo",
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/user/favorites/add', methods = ['POST'])
def fav():
	#Obtenemos el id del articulo.
	article = request.json
	stringErrorMessage = 'Error #00007 / session[\'data\']'
	stringStatus = 'error'
	#Verificamos si existe una sesion activa.
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		theArticle = db.Article.find_one(ObjectId(article['IDArticle']))
		#Agregamos el id del articulo a la lista de favoritos.
		if not article['IDArticle'] in theUser['favorites'] and theArticle:
			theArticle['likes'] = theArticle['likes'] + 1
			theUser['favorites'].append(article['IDArticle'])
			db.Article.update_one({'_id': ObjectId(article['IDArticle'])}, {"$set": theArticle}, upsert=False)
			#Actualizamos la lista de favoritos del usuario en la bd.
			db.User.update_one({'email': email}, {"$set": {'favorites': theUser['favorites']}}, upsert=False)
		# Establesemos el mensaje a retornar.
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
		# Cerramos la conexion con la base de datos.
		client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Esta peticion retorna los articulos publicados por este usuario.
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
@app.route('/user/published', methods = ['GET'])
def published():
	#Creamos la variable donde almacenamos la lista de articulos.
	published = []
	#Verificamos si existe una sesion activa.
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		# Verificamos si es un autor el que solicita ver su lista de publicados.
		if theUser['type'] in ['author', 'admin']:
			#Es un autor.
			# Obtenemos todos los articulos no publicados creados por ese autor.
			theArticleList = db.Article.find({'author': email})
			for article in theArticleList:
				published.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
				'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
				'likes': article['likes'], 'coments': article['coments'], 'title': article['title']})
			#Ordenamos los articulos por fecha.
			published = sorted(published, key=sortByTime, reverse=True)
		# Cerramos la conexion con la base de datos.
		client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'articles': published})

'''
	Esta peticion retorna los articulos editados por este usuario.
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
@app.route('/user/edited', methods = ['GET'])
def edited():
	#Creamos la variable donde almacenamos la lista de articulos.
	edited = []
	#Verificamos si existe una sesion activa.
	if 'data' in session:
		# El usuario tiene una sesion activa.
		# Creamos la conexion con la base de datos.
		(client, db) = getConnectionToDB()
		# Obtenemos los datos de la sesion.
		email = session['data']['email']
		password = session['data']['password']
		# Buscamos al usuario en la base de datos.
		theUser = db.User.find_one({'email': email, 'password': password})
		# Verificamos si es un editor el que solicita ver su lista de editados.
		if theUser['type'] in ['editor', 'admin']:
			#Es un autor.
			# Obtenemos todos los articulos no publicados.
			theArticleList = db.Article.find()
			for article in theArticleList:
				#Verificamos si el usuario edito dicho articulo.
				if email in article['editors']:
				#Si fue editado por este usuario lo añadimos a la lista.
					edited.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'],
					'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'],
					'likes': article['likes'], 'coments': article['coments'], 'title': article['title']})
			#Ordenamos los articulos por fecha.
			edited = sorted(edited, key=sortByTime, reverse=True)
		# Cerramos la conexion con la base de datos.
		client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'articles': edited})	

'''
	Remueve el articulo seleccionado de la lista de favoritos del usuario.
	Parametro que resibe: {
		"IDArticle": "aqui recibimos el id del articulo",
	}
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		'errorMessage': "aqui el mensaje de error"
	}
'''
@app.route('/user/favorites/delete', methods = ['POST'])
def favdelete():
	#Obtenemos el id del articulo.
	article = request.json
	stringErrorMessage = 'Error #00007 / session[\'data\']'
	stringStatus = 'error'
	#Verificamos si existe una sesion activa.
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
		theArticle = db.Article.find_one(ObjectId(article['IDArticle']))
		# Borramos el id del articulo a la lista de favoritos.
		if article['IDArticle'] in theUser['favorites'] and theArticle:
			theArticle['likes'] = theArticle['likes'] - 1
			theUser['favorites'].remove(article['IDArticle'])
			#Actualizamos la lista de favoritos del usuario en la bd.
			db.User.update_one({'email': email}, {"$set": {'favorites': theUser['favorites']}}, upsert=False)
			db.Article.update_one({'_id': ObjectId(article['IDArticle'])}, {"$set": theArticle}, upsert=False)
		# Establesemos el mensaje a retornar.
		stringErrorMessage = 'All is fine :P'
		stringStatus = 'success'
		# Cerramos la conexion con la base de datos.
		client.close()
	# Devolvemos el resultado de la peticion.
	return jsonify({'status': stringStatus, 'errorMessage': stringErrorMessage})

'''
	Resetea la base de datos.
'''
@app.route('/db/reset', methods = ['GET'])
def delete_db():
	if 'data' in session:
		(client, db) = getConnectionToDB()
		email = session['data']['email']
		password = session['data']['password']
		theUser = db.User.find_one({'email': email, 'password': password})
		if theUser['type'] == 'admin':
			client.drop_database('DailyPlanet')
		client.close()
		session.pop('data', None)
		return "<h1>Usted acaba de borrar la base de datos! :P</h1>"
	return "<h1>Usted no puede hacer esto :(</h1>"

'''
	Esta peticion retorna los articulos que se mostraan en el feed principal.
	Parametro que resibe: {
		"initArticle": "Numero del articulo inicial.",
		"numArticles": "Numero de articulos a desplegar.", // -1 para no limitar.
		"query": "La palaba a buscar", // Vacio para no limitar.
		"categoryArticle": "Categoria a la que pertenece el articulo.", // Vacio para no limitar.
		"sortMode": "Modo de ordenamiento 'date-time', 'fab', 'comment'",
		"sortRule": "Ordenamiento creciente '<', Ordenamiento decreciente '>'"
	}
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
@app.route('/search', methods = ['POST'])
def search():
	returnData = []
	filteredData = []
	theUser = None
	(client, db) = getConnectionToDB()
	allArticleList = db.Article.find({'posted': True})
	info = request.json
	for article in allArticleList:
		if not info['query'] or simpleSearch(db, article, info['query']):
			if not info['categoryArticle'] or info['categoryArticle'] == article['category']:
				filteredData.append(article)
	if 'data' in session:
		email = session['data']['email']
		password = session['data']['password']
		theUser = db.User.find_one({'email': email, 'password': password})
	if theUser :
		# Es un usuario registrado.
		for article in filteredData:
			returnData.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'], 'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'], 'likes': article['likes'], 'comments': article['coments'], 'title': article['title']})
	else:
		# No es un usuario registrado.
		for article in filteredData:
			if datetime.now().date() == datetime.strptime(article['time-create'], "%d/%m/%Y - %I:%M%p").date():
				returnData.append({'id': str(article['_id']), 'src': article['image'], 'category': article['category'], 'date': article['time-create'], 'text': article['abstract'], 'autorId': article['author'], 'likes': article['likes'], 'comments': article['coments'], 'title': article['title']})
	if info['sortMode'] == 'fab':
		returnData = sorted(returnData, key=sortByFav, reverse=info['sortRule'] == '>')
	elif info['sortMode'] == 'comment':
		returnData = sorted(returnData, key=sortByComment, reverse=info['sortRule'] == '>')
	else:
		returnData = sorted(returnData, key=sortByTime, reverse=info['sortRule'] == '>')
	# Cerramos la conexion con la base de datos.
	client.close()
	initial_var = info['initArticle'] if info['initArticle'] else 0
	end_var = initial_var + info['numArticles'] if not info['numArticles'] == -1 else len(returnData)
	end_var = min(end_var, len(returnData))
	articleList = []
	for i in range(initial_var, end_var):
		articleList.append(returnData[i])
	# Devolvemos el resultado de la peticion.
	return jsonify({'articles': articleList})

'''
	Carga un archivo al servidor.
	Parametro que resibe: form-data -> file=
	Parametros que retorna: {
		"status": "aqui el resultado de la solicitud ("error/succses")",
		"errorMessage": "aqui el mensaje de error",
		"fileId": "el nombre del archivo cargado"
	}
'''
@app.route('/upload', methods = ['POST'])
def upload():
	# check if the post request has the file part
	if 'file' not in request.files:
		return jsonify({'status': 'error', 'errorMessage': 'No file input.', 'fileId': ''})
	file = request.files['file']
	if file.filename == '':
		return jsonify({'status': 'error', 'errorMessage': 'No selected file.', 'fileId': ''})
	if file:
		filename = str(ObjectId()) + os.path.splitext(file.filename)[1]
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return jsonify({'status': 'success', 'errorMessage': 'All is fine :P', 'fileId': '/static/upload/' + filename})

"""
	Iniciamos el programa!!!
"""
if __name__ == '__main__':
	app.run(host='localhost', port=80, debug=True)
