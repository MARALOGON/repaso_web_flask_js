from flask import render_template, request
from vias import app
import csv #Se importa la libreria csv, que contiene metodos de lectura del archivo csv ue nos van a servir para nuestro programa para no tener que hacerlo manualmente
import json
from datetime import date



@app.route("/provincias") #Decorador y endpoint
def provincias():
    #abrir el archivo
    fichero = open("data/provincias.csv", "r")
    #leer cada registro del archivo
    csvreader = csv.reader(fichero, delimiter=',') #csv.reader es el metodo que el modulo csv tiene para leer ficheros. reader te devuelve una lista. Con delimiter le indicamos el caracter por el que debe separar los valores del registro, para luego devolverlos o imprimirlos separados por ese caracter
    
    #procesar el fichero para crear el diccionario que necesitamos para mandarlo al navegador
    lista = [] #Creamos la lista vacia de diccionarios 
    for registro in csvreader: #registro es cada linea del fichero provincias, por ejemplo "O,Asturias"
        d = {'codigo': registro[0], 'valor': registro[1]} #creo la variable d que almacena los pares codigo-valor de la lista de diccionarios. Ej: codigo:'O', valor: 'Asturias'
        lista.append(d) #le añado a la lista cada una de las lineas del fichero en forma de diccionario
    
    #cierro el fichero
    fichero.close()

    #devuelvo el diccionario creado en formato de archivo .json, para que pueda interpretarlo el navegador y mostrarlo
    return json.dumps(lista)

@app.route("/provincia/<codigoProvincia>") #cuando queremos meter un parametro mas que no esta definido, que es variable, lo metemos entre simbolos mayor y menor
def laprovincia(codigoProvincia):
    fichero = open("data/provincias.csv", "r")
    dictreader = csv.DictReader(fichero, fieldnames=['codigo','provincia']) #DictReader es un metodo de csv que permite leer los registros del archivo y mostrarlos en forma de diccionario, en lugar de forma de lista como hace .reader
    for registro in dictreader: #Leo cada registro del diccionario 
        if registro['codigo'] == codigoProvincia: #Si el codigo que figura como clave (codigo) del diccionario es igual que el valor que he metido como codigoProvinica en el navegador
            return registro['provincia'] #Devuelvo lo que figura como resultado en el valor 'provincia' del diccionario

    fichero.close()
    return "La provincia no existe" #Si el codigo que hemos puesto en el navegador no existe, develve ese mensaje

@app.route("/vias/<int:year>", defaults={'mes': None, 'dia': None}) #Esta es la ruta que se activa en caso de que solo se introduzca año, hay que poner los valores mes y dia por defecto a None porque si no peta
@app.route("/vias/<int:year>/<int:mes>", defaults={'dia': None}) #Esta es la ruta que se activa en caso de que solo se introduzca año y mes
@app.route("/vias/<int:year>/<int:mes>/<int:dia>") #Aqui en la ruta forzamos a que los numeros que se metan en el navegador sean enteros, flask hace este trabajo de reconocerlos y de dar error en caso de que no lo sean.
def vias(year, mes, dia):
    #La secuencia de los ifs se hace desde la mas restrictiva a la menos:en el if se tiene en cuenta que solo se inform el año, en el elif se informa año y mes, en el else se informa año, mes y dia
    if not mes:
        fecha = "{:04d}".format(year) #Este elif quiere decir que muestre los resultado del año, es decir, cuando no ponemos el mes ni el dia en el navegador, o cuando solo ponemos dia y no mes
    elif not dia: #Este elif quiere decir que muestre los resultado del año y el mes, es decir, cuando no ponemos el dia en el navegador
        fecha = "{:04d}-{:02d}".format(year, mes)
    else:    
        fecha = "{:04d}-{:02d}-{:02d}".format(year, mes, dia) #El :02d quiere decir que solo admite dos digitos en este campo y que en caso de que solo se introduzca uno, rellene con un 0 delante de ese numero introducido

    fichero = open("data/vias_provincia.csv", "r")
    dictreader = csv.DictReader(fichero, delimiter=";") #Aqui no hace falta ponerle los fieldnames porque ya vienen en el fichero por defecto en la primera linea, con lo cual DictReader los reconoce y crea el diccionario tomandolos como clave directamente

    #creo la estructura de diccionario para conseguir que devuelva la suma de resultados por cada categoria de via, despues de sumar el dato de todas las provincias en la fecha que le pedimos al navegador, dandole el valor por defecto a 0 para que luego se vayan acumulando
    res = {
        'vias_totales':0,
        'vias_V':0,
        'vias_6':0,
        'vias_7':0,
        'vias_8':0,
        'vias_9':0

    }

    for registro in dictreader:
        if fecha in registro["fecha"]: #Aqui le decimos qnue si la fecha esta en el registro en vesz de que si es == a registro, asi nos sirve para todos los casos de uso, cuando solo esta el año y el mes, o el año y el dia, o solo el año, o los 3 a la vez
            for clave in res: #Aqui itero sobre el diccionario creado para la variable res de mas arriba 
                res[clave] += int(registro[clave]) #Para cada clave iterada le voy sumando lo que le corresponde a esa clave en el registro correspondiente del fichero csv
        elif registro["fecha"] > fecha: #Esta linea es para que no siga buscando más cuando ya haya buscado en la fecha que le hemos pedido, ya que hara un  break cuando siga buscando y la fecha ya es mayor 
            break
    
    fichero.close()
    return json.dumps(res) #Aqui le pido que convierta a formato .json el diccionario resultante de la variable res

    ''' 
    Este bloque de codigo es para que sume el numero de vias totales de la fecha que le pidamos sin separar por el grado de las mismas


    vias_totales = 0 
    for registro in dictreader:
        if fecha == registro['fecha']:
            vias_totales += int(registro['vias_totales']) #Se transforman en enteros antes los numeros porque al ser valores de un diccionario, originalmente estan en formato cadena y despues se suman a la variable todos los numeros de la columna vias_totales de todas las provincias que coincidan con la fecha introducida
          elif registro['fecha'] > fecha: #Esta linea es para que no siga buscando más cuando ya haya buscado en la fecha que le hemos pedido, ya que hara un  break cuando siga buscando y la fecha ya es mayor 
            break

    fichero.close()
    return str(vias_totales)

    '''

@app.route("/viasdiarias", methods = ['GET', 'POST'])
def vias_diarias():
    formulario = {  #para no tener que meter todas las variables (provincia, fecha, vias_V, etc.) del formulario en la linea de return render_template, creo este diccionario que contenga todas las claves y valores que voy a tener que actualizarcuando mande una petición al servidor, con la intención de crear un nuevo registro
        'provincia': '',
        'fecha': str(date.today()),
        'vias_V': 0,
        'vias_6': 0,
        'vias_7': 0,
        'vias_8': 0,
        'vias_9': 0,

    }

    fichero = open("data/provincias.csv", "r") #Creo una variable para llamar a abrir el fichero del listado de provincias y leerlo (con "r")
    csvreader = csv.reader(fichero, delimiter=';') #Leo el fichero provincias con csv.reader y le asigno una variable donde se guardan todos los datos de la lectura
    next(csvreader) #metodo para que no lea el primer registo, ya que son los fieldnames

    lista = [] #Creamos la lista vacia de diccionarios, cada diccionario va compuesto de una clave (que es el codigo de la provincia) y de un valor(que es la descripción del codigo, la provincia en si) 
    for registro in csvreader: #registro es cada linea del fichero provincias, por ejemplo "O,Asturias"
        d = {'codigo': registro[0], 'descripcion': registro[1]} #creo la variable d que almacena los pares codigo-valor de la lista de diccionarios. Ej: codigo:'O', descripcion: 'Asturias'
        lista.append(d) #Añado a la lista cada registro leido y almacenado en la variable d
    
    fichero.close()

    if request.method == 'GET':
        return render_template("alta.html", datos = formulario, provincias =lista) #Con este render_template se devuelve el formulario que hemos creado en alta.html al hacer una petición GET, con los valores por defecto que hemos incluido en el diccionario llamado formulario. 
        #La clave "datos" de la linea de arriba llama a Jinja de alta.html, ya que entre llaves el valor que se le da es el que se le asigna en value por ejemplo value="{{datos.vias_6}}". Esto quiere decir que el valor del input de vias_6 que viaje va a ser el dato que introduzcamos en el campo vias_6
        #La variables provincias es ua lista de diccionarios, recorre la lista del archivo provincias y lo convierte en un diccionario, con clave-valor, segun hemos indicado con Jinja en el archivo HTML, a traves de las etiquetas select y option. Ademas, se devuelve el diccionario de codigos provincia y descripcion de provincia que hemos creado con la variable lista justo arriba. 

    #Validar la informacion que llega:
    #Que la provincia sea correcta, para ello vamos a utilizar request.form
   
   
   # Antes de validar, vamos a informar el forumlario para que en caso de que se haga un POST y haya un error en algun campo, no se borren los datos introducidos cuando os de el mensaje de error, es decir cuando el servidor devuelva una respuesta
    for clave in formulario:
        formulario[clave] = request.form[clave] #El diccionario de entrada que viene con las valores que ha dado el usuario a las claves, se lo asigno a mi formulario de vuelta, se quedan esos valores por defecto, pero solo si hace un pOST, por eso se pone detras del request.method == 'GET' y no delante


    #Que los valores de los casos sean numeros y sean enteros positivos
    
    #validar que el numero de vias_V sea >= 0 y entero positivo
    formulario['provincia'] = request.form['provincia']

    vias_V = request.form['vias_V']
    try:   
        vias_V = int(valores["vias_V"])     
        if vias_V < 0: 					
            raise ValueError ('Debe ser positivo’) 

    except ValueError:
        return render_template("alta.html", datos = formulario)





    #Que el total de los casos sea la suma del resto de casos
  
    #Que la fecha sea correcta en formato y en valor
    #Que la fecha no sea a futuro ni anterior a la fecha de inciio de la primera entrada de la base de datos

    #Si la infroamión es incorrecta





    return "Se ha hecho un post" #Cuando rellenamos el formulario y lo enviamos, como el method es POST y no GET, no entra en el if y lo que hace es enviar los datos introducidos en el formulario y devolver el mensaje 


