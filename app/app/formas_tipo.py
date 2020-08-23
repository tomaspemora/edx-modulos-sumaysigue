from wtforms import Form, SubmitField, FileField,StringField, validators, SelectField, HiddenField, TextAreaField, validators
from wtforms.widgets import HTMLString, html_params
from wtforms.fields.html5 import URLField, DateField
from app.wtforms_extended_selectfield import ExtendedSelectField
from app.wtforms_extended_textareafield import ExtendedTextAreaField
import re, datetime
from pdb import set_trace as bp

style={'class':'form-control'}
style_file = {'class':'custom-file-input'}
cursos = [
		('Media', (
			('dmf','DMF'),
			('iep','IEP'),
			)), 
		('Elearning', (
			('snd','SND'),
			('dpa','DPA'),
			('dpe','DPE'),
			('tnr','TNR'),
			('tmd','TMD'),
			('tfr','TFR'),
			('tip','TIP'),
			('ipg','IPG'),
			('tmm','TMM'),
			('ipe','IPE'),
			)),
		('Didactica', (
			('ci1','1er Ciclo'),
			('ci2','2do Ciclo'),
			))
		]

class PDFForm(Form):

	escondido_field = HiddenField()

	opciones_programas = ExtendedSelectField(u'Seleccione el curso', choices=cursos, render_kw=style)

	##select_archivo = FileField(u'Seleccione el archivo de la presentación', [validators.regexp(u'^[^/\\]\.png$')])
	select_archivo = FileField(u'Seleccione el archivo ...', render_kw=style_file, description="Archivo de la presentación (Fichas, Mat complementario, etc)")
	


	def validate_image(form, field):
		if field.data:
			field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)


class FichasForm(Form): 
	pass

class GenForm(Form):
	escondido_field = HiddenField()
	url_genially = URLField(u'Ingrese la url del genially')

class VideoForm(Form):
	pass

class ImageForm(Form):
	pass

class RecapForm(Form):
	escondido_field = HiddenField()
	text_area_html = ExtendedTextAreaField(id='input_html5', label=None)




''' FORMULARIOS PARA MULTIMEDIA DASHBOARD '''
programas = [
			('Media', (
				('dmf','DMF'),
				('iep','IEP'),
				('g3d','G3D'),
				)), 
			('Elearning', (
				('tnr','TNR'),
				('tmd','TMD'),
				('tfr','TFR'),
				('ipe','IPE'),
				('snd','SND'),
				('dpa','DPA'),
				('dpe','DPE'),
				('tip','TIP'),
				('ipg','IPG'),
				('tmm','TMM'),
				)),
			('Didactica', (
				('ci1','1er Ciclo'),
				('ci2','2do Ciclo'),
				))
			]
style_addtask={'class':'form-control .mx-sm-3'}
encargados = [('Programacion', (
				('jorge','Jorge'),
				('diego','Diego'),
				('seba','Seba'),
				('mati','Mati'),
				('otro','Otro'),
				)), 
			('Diseño', (
				('cachorro','Cachorro'),
				('fer','Fer'),
				('Otro','otro'),
			))]
class AddTask(Form):
	programa = ExtendedSelectField(u'Seleccione el programa', choices=programas, render_kw=style_addtask)
	descripcion = StringField(u'Ingrese una descripción')
	fecha = DateField(format='%Y-%m-%d',default=datetime.date.today,validators=[validators.DataRequired()])
	encargado = ExtendedSelectField(u'Encargado', choices=encargados, render_kw=style_addtask)
