from kakebo import app
import sqlite3

@app.route('/')
def index():
    conexion = sqlite3.connect("movimientos.db") #Abro la conexion con la base de datos
    cur = conexion.cursor() #Creo una instancia del cursor y lo conecto


    print(cur.description) #Esta instruccion crea una tupla de tuplas que sirve para que se muestren en el terminal el nombre de los campos de la tabla


    cur.execute("SELECT * FROM movimientos;") #Con cur.execute se le hace la consulta que queramos entre parentesis a la base de datos utilizando lenguaje SQL, en este caso se le dice que muestre todos los movimientos registrados en la tabla

    claves = cur.description #Creo la variable claves para que contenga todos los campos de la tabla (fecha, concepto, categoria, etc.), que se los proporciona cur.description

    filas = cur.fetchall() #Fetchall muestra todos los datos de la tabla
    l = [] #Creo una varaible que es una lista vacia donde meteré los diccionarios resultantes de emparejar los campos y los valores de cada registro de la tabla de la bases de datos, será por tanto una lista de diccionarios
    for fila in filas: #Recorro cada registro fila de todas las fiilas de la tabla de la base de datos
        d = {} #Creo una variable vacia que va a contener los diccionarios
        for columna in fila: #Recorro cada dato de cada registro fila de la tabla
            

    
    conexion.close()

    return "consulta realizada"