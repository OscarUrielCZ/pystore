from datetime import datetime
from os import system

import sa

def interfaz():
	"""Función que muestra la interfaz del programa."""

	fecha = datetime.now().strftime("%I:%M || %A %d, %B %Y")
	if vendedor is not None:
		print("{} · {}".format(vendedor[2], fecha).rjust(80))
	else:
		print("{}".format(fecha).rjust(80))

	if sesion == False:
		print("1. Iniciar sesion.")
		print("2. Registrar cuenta.")
	else:
		print("1. Realizar compra.")
		print("2. Ver ventas.")
		print("3. Ver productos.")
		print("4. Registrar un producto.")
		print("5. Ver perfil.")
		print("6. Cerra sesión.")

	print("\n0. Salir.")

def opcion(texto, i, f):
	"""Función que asegura que una opción sea un entero en un intervalo (i, f)."""

	while True:
		try:
			op = int(input(texto))
		except ValueError:
			pass
		else:
			if i <= op <= f:
				break

	return op

def mostrar_productos():
	productos = sa.todos_productos()
	for p in productos:
		print("{}) {} {}. {} pesos".format(p[0], p[1], p[2], p[4]))

sesion = False
vendedor = None

sa.crear_tablas()
system("cls")

while True:
	interfaz()

	if sesion == False:
		op = opcion("Opción: ", 0, 2)
		print("")

		if op == 1:
			u = input("Usuario\n> ")
			c = input("Contraseña\n> ")

			vendedor = sa.info_vendedor(u)

			if vendedor == None or c != vendedor[3]:
				vendedor = None
				print("Usuario o contraseña incorrecto.")
			else:
				sesion = True
				print("Bienvenido", vendedor[2])

		elif op == 2:
			u = input("Nombre de usuario\n> ")
			n = input("Nombre\n> ")
			c = input("Contraseña\n> ")
			sa.registrar_cuenta(u, n, c)

	else:
		op = opcion("Opción: ", 0, 6)
		print("")

		if op == 1:
			suma = 0

			print("0) Salir.")
			mostrar_productos()
			while True:
				hora = datetime.now().strftime("%I:%M")
				fecha = datetime.now().strftime("%d %B %Y")
				prod = opcion("Comprar\n> ", 0, len(sa.todos_productos()))

				if prod == 0:
					break

				cant = opcion("Cantidad\n> ", 0, 1000000)

				if cant == 0:
					continue

				producto = sa.info_producto(prod)
				suma += (producto[4]*cant)
				sa.registrar_compra(prod, cant, vendedor[0], hora, fecha)
				print("Cantidad: {} pesos.".format(suma))

			print("\nTotal:")
			print(suma, "pesos")


		elif op == 2:
			todas_ventas = sa.todas_ventas()
			ventas = dict()
			total = 0

			for v in todas_ventas:
				if v[1] in ventas.keys():
					ventas[v[1]] += v[2]
				else:
					ventas[v[1]] = v[2]

			for i, k in ventas.items():
				producto = sa.info_producto(i)
				total += producto[4] * k
				print("{} {}. {} ventas.".format(producto[1], producto[2], k))

			print("\nIngresos totales: ")
			print(total)


		elif op == 3:
			mostrar_productos()

		elif op ==4:
			prod = input("Producto\n> ")
			marc = input("Marca\n> ")
			cont = opcion("Contenido\n> ", 1, 1000000)
			prec = opcion("Precio\n> ", 1, 1000000)

			sa.registrar_producto(prod, marc, cont, prec)

			print("Registrado correctamente.")

		elif op == 5:
			system("cls")

			while True:
				print("ID:", vendedor[0])
				print("Usuario:", vendedor[1])
				print("Nombre:", vendedor[2])

				print("")
				print("1. Cambiar nombre de usuario.")
				print("2. Cambiar nombre de vendedor.")
				print("3. Cambiar contraseña.")
				print("\n0. Regresar al menú.")

				op_u = opcion("Opción\n> ", 0, 3)

				if op_u == 0:
					break

				if op_u == 1:
					n_usuario = input("Nombre\n> ")
					cont = input("Contraseña para aplicar cambios\n> ")

					if cont == vendedor[3]:
						sa.actualiza_vendedor(vendedor[0], n_usuario, None, None)
						print("Se ha cambiado el nombre a", n_usuario)
						vendedor[1] = n_usuario
					else:
						print("Constraseña incorrecta.")

				elif op_u == 2:
					n_vendedor = input("Nombre\n> ")
					cont = input("Contraseña para aplicar cambios\n> ")

					if cont == vendedor[3]:
						sa.actualiza_vendedor(vendedor[0], None, n_vendedor, None)
						print("Se ha cambiado el nombre a", n_vendedor)
					else:
						print("Constraseña incorrecta.")

				elif op_u == 3:
					cont = input("Antigua contraseña\n> ")
					n_cont = input("Nueva contraseña\n> ")
					n_cont2 = input("Confirma nueva contraseña\n> ")

					if n_cont == n_cont2:
						if cont == vendedor[3]:
							sa.actualiza_vendedor(vendedor[0], None, None, n_cont)
							print("Se ha cambiado la contraseña.")
						else:
							print("Constraseña incorrecta.")
					else:
						print("Las contraseñas no coinciden.")

				input()
				system("cls")

				vendedor = sa.info_vendedor(vendedor[1])

		elif op == 6:
			print("Cerrando sesión.")
			sesion = False
			vendedor = None

	if op == 0:
		print("Fin del programa.")
		break

	input()
	system("cls")
