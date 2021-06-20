from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, SelectField, FloatField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):  #Aqui creamos una función que nos va a calidadr que en el formulario solo se puedan meter fechas por debajo  de la actual. Le pasamos los parametros formulario y campo, habrá que informar de ambos en la variable fecha de la siguiente clase MovimientosForm
    hoy = date.today
    if campo.data > hoy:
        raise ValidationError('La fecha no puede ser mayor que hoy') #ValidationError es un error especifico de WTForms, por eso hay que importarlo también.

class MovimientosForm(FlaskForm): #Creamos la clase MovimientosForm que hereda del objeto FlaskForm. El objeto FlaskForm automatiza entre otras cosas la validacion de errores de los formularios. En las siguientes lineas se definen los campos y se mete si son requeridos o no 
    fecha = DateField("Fecha", validators=[DataRequired(message = "Debe informar una fecha valida"), fecha_por_debajo_de_hoy])
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('00', ''), ('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'), ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField(" Es gasto")
    submit = SubmitField('Aceptar')
