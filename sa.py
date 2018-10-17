import sqlite3

nombre_bd = "tienda.db"

def crear_tablas():
	"""Función que crea las tablas en la base de datos."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	try:
		bd.execute("""
			CREATE TABLE vendedores (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				usuario VARCHAR(35) UNIQUE NOT NULL,
				nombre VARCHAR(35) NOT NULL,
				contrasena VARCHAR(35) NOT NULL
			)
		""")
	except sqlite3.OperationalError:
		print("La tabla 'vendedores' ya existe.")
	else:
		print("La tabla 'vendedores' se ha creado.")

	try:
		bd.execute("""
			CREATE TABLE productos (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				producto VARCHAR(35) NOT NULL,
				marca VARCHAR(35) NOT NULL,
				contenido INTEGER NOT NULL,
				precio INTEGER NOT NULL
			)
		""")
	except sqlite3.OperationalError:
		print("La tabla 'productos' ya existe.")
	else:
		print("La tabla 'productos' se ha creado.")

	try:
		bd.execute("""
			CREATE TABLE ventas (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				producto_id INTEGER NOT NULL,
				cantidad INTEGER NOT NULL,
				vendedor_id INTEGER NOT NULL,
				hora VARCHAR(30) NOT NULL,
				fecha VARCHAR(30) NOT NULL,
				FOREIGN KEY(producto_id) REFERENCES productos(id)
				FOREIGN KEY(vendedor_id) REFERENCES vendedores(id)
			)
		""")
	except sqlite3.OperationalError:
		print("La tabla 'ventas' ya existe.")
	else:
		print("La tabla 'ventas' se ha creado.")

	conexion.close()

def registrar_cuenta(u, n, c):
	"""Función que registra un nuevo vendedor en la tabla vendedores"""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	try:
		bd.execute("INSERT INTO vendedores VALUES (null, '{}', '{}', '{}')".format(u, n, c))
	except sqlite3.IntegrityError:
		print("El usuario {} ya existe.".format(u))
	else:
		print("Cuenta creada.")

	conexion.commit()
	conexion.close()

def info_vendedor(u):
	"""Función que retorna información con el nombre de usuario u."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	vendedor = bd.execute("SELECT * FROM vendedores WHERE usuario='{}'".format(u)).fetchone()

	conexion.close()

	return vendedor

def registrar_producto(prod, marc, cont, prec):
	"""Función que registra un nuevo producto en la tabla productos."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	bd.execute("INSERT INTO productos VALUES (null, '{}', '{}', {}, {})".format(prod, marc, cont, prec))

	conexion.commit()
	conexion.close()

def info_producto(p):
	"""Función que retorna información con el id del producto p."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	producto = bd.execute("SELECT * FROM productos WHERE id={}".format(p)).fetchone()

	conexion.close()

	return producto

def todos_productos():
	"""Función que retorna todos los elementos en la tabla productos."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	productos = bd.execute("SELECT * FROM productos").fetchall()

	conexion.close()

	return productos

def registrar_compra(id_producto, cantidad, id_usuario, hora, fecha):
	"""Función que registra una nueva venta en la tabla ventas."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	bd.execute("INSERT INTO ventas VALUES (null, {}, {}, {}, '{}', '{}')".\
		format(id_producto, cantidad, id_usuario, hora, fecha))

	conexion.commit()
	conexion.close()

def todas_ventas():
	"""Función que retorna todos los elementos en la tabla ventas."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	ventas = bd.execute("SELECT * FROM ventas").fetchall()

	conexion.close()

	return ventas

def actualiza_vendedor(id, usuario, nombre, contrasena):
	"""Función que actualiza el nombre del usuario, nombre o contraseña con el id id_u."""

	conexion = sqlite3.connect(nombre_bd)
	bd = conexion.cursor()

	if usuario is not None:
		bd.execute("UPDATE vendedores SET usuario = '{}' WHERE id = {}".format(usuario, id))
	elif nombre is not None:
		bd.execute("UPDATE vendedores SET nombre = '{}' WHERE id = {}".format(nombre, id))
	elif contrasena is not None:
		bd.execute("UPDATE vendedores SET contrasena = '{}' WHERE id = {}".format(contrasena, id))


	conexion.commit()
	conexion.close()
