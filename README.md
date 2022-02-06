# challenge
Programa para Cargar datos del challenge de Alkemy en BD en PostgreSQL

1.- Se recomienda usar con python >3.7 y PostgreSQL>10

2.- crear entorno virtual usando venv: ejemplo "python3 -m venv alkemy-env" (Linux) o "python -m venv alkemy-env" (windows)

3.- Activar entorno virtual dentro del entorno virtual ir a alkemy-env/bin/activate

4.- descargar la carpeta completa en el lugar de preferencia

5.- dentro de la caperta y con la linea de comando ejecutar: pip install -r requirements.txt --no-index #para instalar los packahge necesarios para funcionar correctamente
    el programa
    
6.- crear base de datos= db_test y un usuario en la aplicacion: user_test password:test1234

7.- ejecutar programa con python principal.py

8.- Programa genera 4 tablas:
tbl_cine: estan todos los datos descargados de la categoria cine

tbl_data: es la union de los tres dataframe unidos segun los datos requeridos:['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'categoria', 'provincia', 'localidad', 'nombre',
    'direccion', 'CP', 'telefono', 'Mail', 'Web']

tbl_categoria: tabla con los datos:
    Cantidad de registros totales por categoría
    Cantidad de registros por provincia y categoría
tbl_resumen_cine: tabla que contiene los datos de los cines:
    Provincia, Cantidad de pantallas, Cantidad de butacas, Cantidad de espacios INCAA
