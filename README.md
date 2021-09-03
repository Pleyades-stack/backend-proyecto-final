uia del api

Modelos:
	Usuario{
		tipo
		nombre
		apellido
		sexo
		correo
		telefono
		ciudad
		rrss
	}
	Perro{
		ubicacion
		nombre
		sexo
		edad
		peso
		tamaño
		raza
		caracter
		caracteristicas
		patologias
		adoptado
	}

usuario:
Registro de usuario
'/usuario/crear'
metodo POST
toma un objeto con todos los campos del modelo

Obtener usuario
'/usuario/<id>'
metodo GET
retorna un usuario en formato de objeto

Modificar Usuario
'/usuario/'
metodo PUT
Permite modificar el usuario pasando a la ruta un objeto con todos los campos del objeto usuario

Eliminar Usuario
'/usuario/'
metodo DELETE
Elimina el objeto seleccionado de la base de datos

Inicio de sesion
'/usuario/login'
metodo POST
Toma un objeto con DOS valores: correo y clave
Retorna el token en: res.data.token

Crear Perro
'/perro/crear'
metodo POST
Toma un objeto con todos los campos del modelo

Editar Perro
'/perro/editar/<id>'
Metodo PUT
Modificacion de los datos de un perro pasando los campos necesarios

Obtener Perro
'/perro/<id>'
Metodo GET
Retorna los datos de un Perro en especifico

Obtener Perros
'/perros'
Metodo Get
Retorna una lista con todos los perros

Declarar como adoptado
'/perro/adoptado/<id>'
Metodo PUT
Modifica el estatus del perro de noAdoptado a Adoptado

Perros del usuario
'/usuario/perros'
Metodo GET
Retorna una lista con todos los perros de UN usuario

Subir imagen de Perro
'/perro/imagen/<id>'
Metodo POST
Crea una nueva imagen en cloudinary basados en el archivo que el frontend provea

Obtener foto de Perro
'/perro/imagen/<id>'
Metodo GET
Obtiene las imagenes asignadas a UN perro

Eliminar foto de Perro
'/perro/imagen/<id>'
Metodo DELETE
Elimina la imagen seleccionada de cloudinary y la eliminar de la base de datos
