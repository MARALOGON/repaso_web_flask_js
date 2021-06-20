from kakebo import app
from flask import render_template, jsonify #jsonify hace lo mismo que el json.dumps, pero es mas adecuado importarlo porque es un objeto de flask y monta las cabeceras de manera mas adecuada
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db") #Abro la conexion con la base de datos
    cur = conexion.cursor() #Creo una instancia del cursor y lo conecto

    cur.execute("SELECT * FROM movimientos;") #Con cur.execute se le hace la consulta que queramos entre parentesis a la base de datos utilizando lenguaje SQL, en este caso se le dice que muestre todos los movimientos registrados en la tabla

    claves = cur.description #Creo la variable claves para que contenga todos los campos de la tabla (fecha, concepto, categoria, etc.), que se los proporciona cur.description
    filas = cur.fetchall() #Fetchall muestra todos los datos de la tabla
    movimientos = [] #Creo una varaible que es una lista vacia donde meteré los diccionarios resultantes de emparejar los campos y los valores de cada registro de la tabla de la bases de datos, será por tanto una lista de diccionarios
    saldo = 0 #Se crea la variable saldo igualada a 0 antes del for, porque una vez que se ponga a recorrer el for se incluirá el primer valor con la cantidad del primer registro o primera fila 
    for fila in filas: #Para cada fila 
        d = {} #Creo un diccionario
        for tuplaclave, valor in zip(claves,fila): #Recorro la tupla de claves que son los campos de la tabla (su valor). El zip enfrenta el primer elemento de la tupla de claves(que devuelve el nombre de cada campo y otros 6 paramentros None) con el primer valor de cada fila o registro(id, fecha, concepto, etc...)
            #En el for y el zip se estan enfrentando elementos iguales, es decir tupla clave sería igual que claves y valor igual que fila 
            d[tuplaclave[0]] = valor #Se elige el elemento que esta en la posicion 0 de la tupla de claves (es el 0 porque ya lo sabemos al hacer un print) que es el id, fecha, concepto, etc. y le asignamos el valor correspondiente de cada fila.
        if d['esGasto'] == 0: #Aqui estamos creando este if para caluclar el saldo. Le decimos que si es igual a 0, es decir si es false, es decir, si es ingreso, que sume a la variable saldo la cantidad correspondiente
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo # Aqui se crea el campo saldo en el diccionario y se iguala al saldo resultante despues de salir del if
        movimientos.append(d) 

    conexion.close()

    return render_template('movimientos.html', datos = movimientos) #para que podamos devolver en el navegador la estructura que hemos creado en el fichero HTML
    #En este caso, se ponen 2 parametros. En el segundo, datos = movimientos, nos sirve para presentar todos los datos ( valores de las celdas de encabezado y su correspondiente valores de las celdas datos) que aparecem en la lista de diccionarios que hemos creado con movimientos = [] en este mismo fichero views.
    #Este datos que incluimos en el render_template es el datos que hemos creado como variable en el movimientos.html, donde recorremos con "for movimiento in datos". la variable datos recoge todos los valores de las celdas de la tabla, como se exolica en linea de arriba


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    return render_template('alta.html')


