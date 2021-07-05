from flask.helpers import url_for, flash
from kakebo import app
from flask import render_template, jsonify, request, redirect, url_for #jsonify hace lo mismo que el json.dumps, pero es mas adecuado importarlo porque es un objeto de flask y monta las cabeceras de manera mas adecuada
import sqlite3
from kakebo.forms import MovimientosForm, FiltraMovimientosForm
from datetime import date
from kakebo.dataccess import *

dbManager = DBmanager() #Instancio la clase que he creado en el fiechero dataaceess.py


@app.route('/', methods = ['GET', 'POST'])
def index(): #Ahora esta funcion la vamos a dejar solo para que muestre los datos de la consulta o modificaciones en la ruta ("/") y para que contenga el calculo del saldo
    filtraForm = FiltraMovimientosForm() #Instancio la calse FiltraMovimientosForm, que la he creado en el fichero forms.py. Si cuando hacemos GET viene un formulario informado, la instancia filtraForm lo va a informar con los campos que le hemos puesto a FiltraMovimientosForm
    query = "SELECT * FROM movimientos WHERE  1=1" 
    parametros = []
    #Validar filtraForm
    if request.method == 'POST':
        if filtraForm.validate(): #Este if es para validar filtraForm
            query = "SELECT * FROM movimientos WHERE 1=1" #Se monta la consulta
            parametros = []
            if filtraForm.fechaDesde.data != None: #Si el campo fechaDesde está informado, es distinto de None
                query += " AND fecha >= ?" #Este query es la consulta que se va a ejecutar en el movimientos = consultaSQL(query) de mas abajo. El "WHERE fecha >= ?" se añade al query "SELECT * FROM movimientos"
                parametros.append(filtraForm.fechaDesde.data)
            if filtraForm.fechaHasta.data != None:
                query += " AND fecha <= ?"
                parametros.append(filtraForm.fechaHasta.data)
            if filtraForm.texto.data != '':
                query += ' AND concepto LIKE ?' #El ? representa cualquier cadena de texto que queramos meterle como concepto
                parametros.append("%{}%".format(filtraForm.texto.data)) #Con este format lo que le digo al parametros.apppend es que añada la cadema de texto que he metido en el query anterior, eso lo consigo con el "%{}%"
            
    #este bloque de codigo, hasta el return render_template, se va a ejecutar tanto si la peticion es GET (solo consulta de los registros), como si es POST (consulta con flitrado)       
    query += " ORDER BY fecha" #Esta query se la ponemos para que ordene por fecha el resultado del filtrado que hemos hecho
    print(query)
    movimientos = dbManager.consultaMuchasSQL(query, parametros) #Ahora la variable movimientos va a contener todos los registros de la tabla, incluyendo los que se hayn podido modificar con la funcion consultaSQL 

    saldo = 0 #Se crea la variable saldo igualada a 0 antes del for, porque una vez que se ponga a recorrer el for se incluirá el primer valor con la cantidad del primer registro o primera fila 
    for d in movimientos: # d se convierte en el diccionario y en este caso movimientos es la variable que contiene la lista de diccionarios. 
        if d['esGasto'] == 0: #Aqui estamos creando este if para caluclar el saldo. Le decimos que si es igual a 0, es decir si es false, es decir, si es ingreso, que sume a la variable saldo la cantidad correspondiente
            saldo = saldo + d['cantidad']
        else:
            saldo = saldo - d['cantidad']
        d['saldo'] = saldo # Aqui se añade el campo saldo al diccionario y se iguala al saldo resultante despues de salir del if
    

    return render_template('movimientos.html', datos = movimientos, formulario = filtraForm) #para que podamos devolver en el navegador la estructura que hemos creado en el fichero HTML
    #En este caso, se ponen 2 parametros. En el segundo, datos = movimientos, nos sirve para presentar todos los datos ( valores de las celdas de encabezado y su correspondiente valores de las celdas datos) que aparecem en la lista de diccionarios que hemos creado con movimientos = dbManager.consultaMuchasSQL(query, parametros) en este mismo fichero views.
    #Este datos que incluimos en el render_template es el datos que hemos creado como variable en el movimientos.html, donde recorremos con "for movimiento in datos". la variable datos recoge todos los valores de las celdas de la tabla, como se exolica en linea de arriba
    #Como ultimo parametro, creo un formulario de filtrado cuando haya una petición GET. Lo creo con formulario = filtraForm



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
                dbManager.modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])
            except sqlite3.Error as el_error: #Intentamos capturar el error para que en caso de error no se caiga el programa
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return render_template('alta.html', form = formulario)

            #Redirect a la ruta:

            return redirect(url_for("index"))

        else:
            return render_template('alta.html', form = formulario)


@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        registro = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if not registro: #Se hace este if por si acaso al enviar el GET para que salga el formulario de borrado, otro usuario lo ha hecho al mismo tiempo y ya no existe ese registro
            flash("El registro no existe", "error")
            return render_template('borrar.html', movimiento={}) #En caso de meter en la barra del navegador un registro para borrar que no exista, devuelve el formulario vacio (el diccionario movimiento vacio) y el mensaje de error
    
        
        return render_template('borrar.html', movimiento=registro) #Esta variable movimiento es la misma que viene en la template borrar.html dividida por campos, por ejemplo movimiento.cantidad. Contiene un registro de la base de datos, toda la fila de datos entera
        #A La variable movimiento se le asigna los valores obtenido de la variable registro, al hacer la consultaUnaSQL, unas lineas mas arriba y eso es lo que devuleve como formulario
    else:
        try:
            dbManager.modificaTablaSQL("DELETE FROM movimientos WHERE id=?;", [id])

        except sqlite3.error as e:
            flash("Se ha producido un error en la base de datos, vuelva a intentarlo", 'error')
            return redirect(url_for('index'))

        flash("Borrado realizado con éxito", 'aviso')    
        return redirect(url_for('index'))
        

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method == 'GET':
        registro = dbManager.consultaUnaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if not registro:
            flash("El registro no existe", "error")
            return render_template('modificar.html', form=MovimientosForm())
        registro['fecha'] = date.fromisoformat(registro['fecha'])

        formulario = MovimientosForm(data = registro) 
    
        return render_template('modificar.html', form = formulario) 
    if request.method == 'POST':
        formulario = MovimientosForm()
        if formulario.validate():
            try:    
                dbManager.modificaTablaSQL("UPDATE movimientos SET fecha = ?, concepto = ?, categoria = ?, es Gasto = ?, cantidad = ? WHERE id = ?", 
                                [formulario.fecha.data, 
                                formulario.concepto.data,
                                formulario.categoria.data,
                                formulario.esGasto.data, 
                                formulario.cantidad.data,
                                id]
                )
                flash("Modificación realizada con éxito", "aviso")
                return redirect(url_for("index"))
            except sqlite3.Error as e:
                print("Error en update:", e)
                flash("Se ha producido un error en acceso a base de datos. Contacte con el administrador", "error")
                return render_template('modificar.html', form=formulario)
        
        else:
            return render_template('modificar.html', form=formulario)




        
