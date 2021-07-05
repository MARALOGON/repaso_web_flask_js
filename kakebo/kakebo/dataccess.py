import sqlite3


class DBmanager():
    def __toDict__(self, cur): # __toDict__ lo que hace es generar un resultado que es una lista y añadir los registos, va a devolver una lista con un unico registro
        #Obtengo los datos de la consulta
        claves = cur.description #Creo la variable claves para que contenga todos los campos de la tabla (fecha, concepto, categoria, etc.), que se los proporciona cur.description
        filas = cur.fetchall() #Fetchall muestra todos los datos de la tabla (todas las filas, todos los registros)
        #Proceso los datos para devolver una lista de diccionarios (un diccionario por fila)
        resultado = [] 
        for fila in filas: 
            d = {} 
            for tuplaclave, valor in zip(claves,fila): 
                d[tuplaclave[0]] = valor 
            resultado.append(d) 

        return resultado
    
    def consultaMuchasSQL(self, query, parametros = []): #Con esta función vamos a sacar todo lo referente a las consultas de la función de index para localizarlo aqui. Esta función siempre va a devolver una lista de diccionarios, al pedirle muchas consultas
        conexion = sqlite3.connect("movimientos.db") #Abro la conexion con la base de datos
        cur = conexion.cursor() #Creo una instancia del cursor y lo conecto

        #Ejecuto la consulta
        cur.execute(query, parametros) #Este execute queremos que nos devuelva un registro o una lista de registros, de ahi que su parametro sea query        
        resultado = self.__toDict__(cur)
        conexion.close()
        return resultado
    
    def consultaUnaSQL(self, query, parametros = []): #Esta función va a devolver una lista con un registro, ya que solo le solicitamos una busqueda
        resultado = self.consultaMuchasSQL(query, parametros)
        if len(resultado) > 0: #Aqui le dice que si el resultado de la consulta es mayor que 0, es decir, si existe
            return resultado[0] #Lo devuelve el primer elemento como una lista

    def modificaTablaSQL(self, query, parametros = []): #En esta función vamos a incluir todo lo que tenga que ver con las modificaciones de la tabla, el UPDATE, el DELETE, etc.
        conexion = sqlite3.connect("movimientos.db") 
        cur = conexion.cursor()

        cur.execute(query, parametros)


        conexion.commit() #Este commit lo que hace es que el cambio relizado lo fija en la base de datos. Es oblgatorio para que se fije en la base de datos.
        conexion.close()
