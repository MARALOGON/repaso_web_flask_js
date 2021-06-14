from vias import app
import csv #Se importa la libreria csv, que contiene metodos de lectura del archivo csv ue nos van a servir para nuestro programa para no tener que hacerlo manualmente
import json



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
  