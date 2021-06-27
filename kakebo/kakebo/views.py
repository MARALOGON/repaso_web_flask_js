import re
from flask.helpers import url_for, flash
from kakebo import app
from flask import render_template, jsonify, request, redirect, url_for #jsonify hace lo mismo que el json.dumps, pero es mas adecuado importarlo porque es un objeto de flask y monta las cabeceras de manera mas adecuada
import sqlite3
from kakebo.forms import MovimientosForm

def consultaSQL(query, parametros = []): #Con esta función vamos a sacar todo lo referente a las consultas de la función de index para localizarlo aqui
    conexion = sqlite3.connect("movimientos.db") #Abro la conexion con la base de datos
    cur = conexion.cursor() #Creo una instancia del cursor y lo conecto

    #Ejecuto la consulta
    cur.execute(query) #Este execute queremos que nos devuelva un registro o una lista de registros, de ahi que su parametro sea query

    #Obtengo los datos de la consulta
    claves = cur.description #Creo la variable claves para que contenga todos los campos de la tabla (fecha, concepto, categoria, etc.), que se los proporciona cur.description
    filas = cur.fetchall() #Fetchall muestra todos los datos de la tabla (todas las filas, todos los registros)
    
    
    #Proceso los datos para devolver una lista de diccionarios (un diccionario por fila)
    resultado = [] #Creo una variable que es una lista vacia donde meteré los diccionarios resultantes de emparejar los campos y los valores de cada registro de la tabla de la bases de datos, será por tanto una lista de diccionarios
    #saldo = 0 #El saldo no se incluye en este proceso de los datos porque no forma parte de la consulta
    for fila in filas: #Para cada fila 
        d = {} #Creo un diccionario
        for tuplaclave, valor in zip(claves,fila): #Recorro la tupla de claves que son los campos de la tabla (su valor). El zip enfrenta el primer elemento de la tupla de claves(que devuelve el nombre de cada campo y otros 6 paramentros None) con el primer valor de cada fila o registro(id, fecha, concepto, etc...)
            #En el for y el zip se estan enfrentando elementos iguales, es decir tupla clave sería igual que claves y valor igual que fila 
            d[tuplaclave[0]] = valor #Se elige el elemento que esta en la posicion 0 de la tupla de claves (es el 0 porque ya lo sabemos al hacer un print) que es el id, fecha, concepto, etc. y le asignamos el valor correspondiente de cada fila.
        resultado.append(d) 

    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros = []): #En esta función vamos a incluir todo lo que tenga que ver con las modificaciones de la tabla, el UPDATE, el DELETE, etc.
    conexion = sqlite3.connect("movimientos.db") 
    cur = conexion.cursor()

    cur.execute(query, parametros)


    conexion.commit() #Este commit lo que hace es que el cambio relizado lo fija en la base de datos. Es oblgatorio para que se fije en la base de datos.
    conexion.close()


@app.route('/')
def index(): #Ahora esta funcion la vamos a dejar solo para que muestre los datos de la consulta o modificaciones en la ruta ("/") y para que contenga el calculo del saldo

    movimientos = consultaSQL("SELECT * FROM movimientos;") #Ahora la variable movimientos va a contener todos los registros de la tabla, incluyendo los que se hayn podido modificar con la funcion consultaSQL 
   
    saldo = 0 #Se crea la variable saldo igualada a 0 antes del for, porque una vez que se ponga a recorrer el for se incluirá el primer valor con la cantidad del primer registro o primera fila 
    for d in movimientos: # d se convierte en el diccionario y en este caso movimientos es la variable que contiene la lista de diccionarios. 
        if d['esGasto'] == 0: #Aqui estamos creando este if para caluclar el saldo. Le decimos que si es igual a 0, es decir si es false, es decir, si es ingreso, que sume a la variable saldo la cantidad correspondiente
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo # Aqui se añade el campo saldo al diccionario y se iguala al saldo resultante despues de salir del if
       

    return render_template('movimientos.html', datos = movimientos) #para que podamos devolver en el navegador la estructura que hemos creado en el fichero HTML
    #En este caso, se ponen 2 parametros. En el segundo, datos = movimientos, nos sirve para presentar todos los datos ( valores de las celdas de encabezado y su correspondiente valores de las celdas datos) que aparecem en la lista de diccionarios que hemos creado con movimientos = [] en este mismo fichero views.
    #Este datos que incluimos en el render_template es el datos que hemos creado como variable en el movimientos.html, donde recorremos con "for movimiento in datos". la variable datos recoge todos los valores de las celdas de la tabla, como se exolica en linea de arriba


@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():

    formulario = MovimientosForm() #Creamos la variable form que va a ser una instancia de MovimientosForm que hay en el fichero forms.py y que hemos importado a este fichero
    if request.method == 'GET':
        return render_template('alta.html', form = formulario) #En este segundo parametro, el form hace referencia al form de alta.html y formulario hace referencia a la variable formulario de este fichero, en la lunea de encima de este
    else:
        if formulario.validate(): #Validate es un metodo que valida de forma automática todas las validaciones que hemos incluido en forms.py. Además en la variable formulario (instancia de MovimientosForm) nos deja la información de cada error que se produzca   
            #Insertar el movimiento en la base de datos
            
            #3 comillas es una cadena multilinea, Python lo considera como cadenas. Aunque sea otro lenguaje el que vaya entre comillas, como SQL, Python lo reconoce como una cadena, es lo que necesita para meter un movimiento nuevo en la tabla.
            query = """ 
                    INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad)
                    VALUES (?, ?, ?, ?, ?)
                """ #Las interrogaciones sirven para que coja los valores de esos campos que se introduzcan para un nuevo movimiento
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error: #Intentamos capturar el error para que en caso de error no se caiga el programa
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos")
                return render_template('alta.html', form = formulario)

            #Redirect a la ruta:

            return redirect(url_for("index"))

        else:
            return render_template('alta.html', form = formulario)