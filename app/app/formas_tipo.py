from wtforms import Form, SubmitField, FileField,StringField, validators, SelectField, HiddenField

from app.wtforms_extended_selectfield import ExtendedSelectField
import re


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
	pass

class VideoForm(Form):
	pass

class ImageForm(Form):
	pass

class RecapForm(Form):
	pass
