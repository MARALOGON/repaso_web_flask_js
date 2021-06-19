from kakebo import app
from flask import jsonify #jsonify hace lo mismo que el json.dumps, pero es mas adecuado importarlo porque es un objeto de flask y monta las cabeceras de manera mas adecuada
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db") #Abro la conexion con la base de datos
    cur = conexion.cursor() #Creo una instancia del cursor y lo conecto


    print(cur.description) #Esta instruccion crea una tupla de tuplas que sirve para que se muestren en el terminal el nombre de los campos de la tabla


    cur.execute("SELECT * FROM movimientos;") #Con cur.execute se le hace la consulta que queramos entre parentesis a la base de datos utilizando lenguaje SQL, en este caso se le dice que muestre todos los movimientos registrados en la tabla

    claves = cur.description #Creo la variable claves para que contenga todos los campos de la tabla (fecha, concepto, categoria, etc.), que se los proporciona cur.description

    filas = cur.fetchall() #Fetchall muestra todos los datos de la tabla
    movimientos = [] #Creo una varaible que es una lista vacia donde meteré los diccionarios resultantes de emparejar los campos y los valores de cada registro de la tabla de la bases de datos, será por tanto una lista de diccionarios
    for fila in filas: #Para cada fila 
        d = {} #Creo un diccionario
        for tuplaclave, valor in zip(claves,fila): #Recorro la tupla de claves que son los campos de la tabla (su valor). El zip enfrenta el primer elemento de la tupla de claves(que devuelve el nombre de cada campo y otros 6 paramentros None) con el primer valor de cada fila o registro(id, fecha, concepto, etc...)
            #En el for y el zip se estan enfrentando elementos iguales, es decir tupla clave sería igual que claves y valor igual que fila 
            d[tuplaclave[0]] = valor #Se elige el elemento que esta en la posicion 0 de la tupla de claves (es el 0 porque ya lo sabemos al hacer un print) que es el id, fecha, concepto, etc. y le asignamos el valor correspondiente de cada fila.
        movimientos.append(d) 

    conexion.close()

    return jsonify(movimientos) #Esto equivale a hacer un json.dumps de la lista de diccionarios movimientos