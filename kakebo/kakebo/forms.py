from sqlite3.dbapi2 import Date
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, SelectField, FloatField, BooleanField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):  #Aqui creamos una función que nos va a calidadr que en el formulario solo se puedan meter fechas por debajo  de la actual. Le pasamos los parametros formulario y campo, habrá que informar de ambos en la variable fecha de la siguiente clase MovimientosForm
    if campo.data == None: # Con este if le estamos diciendo que si no se ha informado el campo de alguna de las fechas del filtrado (fechaDesde o fechaHasta), no haga nada, solo return, es decir que no lo valide
        return

    hoy = date.today()
    if campo.data > hoy: #data es un atributo de la clase Field, que es un clase de WTForms
        raise ValidationError('La fecha no puede ser mayor que hoy') #ValidationError es un error especifico de WTForms, por eso hay que importarlo también.

class MovimientosForm(FlaskForm): #Creamos la clase MovimientosForm que hereda del objeto FlaskForm. El objeto FlaskForm automatiza entre otras cosas la validacion de errores de los formularios. En las siguientes lineas se definen los campos y se mete si son requeridos o no 
    id = HiddenField()
    fecha = DateField("Fecha", validators=[DataRequired(message = "Debe informar una fecha valida"), fecha_por_debajo_de_hoy])
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('00', ''), ('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'), ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField(" Es gasto")
    submit = SubmitField('Aceptar')


class FiltraMovimientosForm(FlaskForm): #Creo esta otra clase para crear el formulario de filtrado, para poder buscar en la bse de datos un registro por fechas o por concepto
    fechaDesde = DateField("Desde", validators=[fecha_por_debajo_de_hoy], default=date(1, 1, 1))
    fechaHasta = DateField("Hasta", validators=[fecha_por_debajo_de_hoy], default=date.today()) #Le ponemos aqui el default para que ponga por defecto la fecha actual, y ya este informada, porque si no da error tipo del Datefield
    texto = StringField("Concepto")
    submit = SubmitField("Filtrar)")

    
    