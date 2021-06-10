from flask import Flask

app = Flask(__name__) #Esta instruccion es para crear una instancia de Flask (Flask es una clase que es una aplicación, su instancia en este caso es app) reconozca por su nombre la aplicacion que debe usar

@app.route('/')  #Un decorador es una función que rodea a otra funcion. A la instancia app se le pasa una ruta del navegador('/') escrita como una cadena 
def index(): #Debajo de un decorador siempre hay una función que va a devolver algo en el navegador. Route es un metodo de Flask que asocia todo lo que hay en su funcion a la ruta del navegador que le hemos puesto.
    return 'Hola, mundo!'