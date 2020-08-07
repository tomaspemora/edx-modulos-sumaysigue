from flask import Markup
from pdb import set_trace as bp
import os
import pysftp

static_server = "static.sumaysigue.uchile.cl"
def server_connnect():
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None
	srv = pysftp.Connection(host=static_server, username="edustatic",
	password="qD7pcVQF", port=2837, private_key=".ppk", cnopts=cnopts)
	# Get the directory and file listing
	return srv

# Closes the connection
#srv.close()

def input_radio(name,display_text,tipo_formulario):
	return "<input type='radio' id='"+name+"' name='"+tipo_formulario+"' value='"+name+"'><label for='"+name+"'' style='margin-left:10px;user-select:none'>"+display_text+"</label><br>"

def input_text(name):
	return None


def desplegable(value, text):
	return "<option value='"+value+"'>"+text+"</option>"

def generar_params(requeste):
	srv = server_connnect()
	#sv_url = 'c:'+os.path.sep+'users'+os.path.sep+'desktop'+os.path.sep
	sv_url = 'cmmeduformacion/implementacion'
	if requeste.form['escondido_field'] == 'pdf':
		file_path = sv_url +'/' +requeste.form['opciones_programas'] + '/'
		file_path_local = os.path.join('resources',requeste.form['opciones_programas'])
		
		if not srv.isdir(file_path):
			srv.mkdir(file_path, mode=755)
		if not os.path.isdir(file_path_local):
			os.makedirs(file_path_local)

		image = requeste.files['select_archivo']
		
		file_path_local = os.path.join(file_path_local, image.filename)

		image.save(file_path_local)
		print(file_path)
		srv.chdir(file_path)
		srv.put(file_path_local)
		srv.close()
		os.remove(file_path_local)

		return {
					'file_url': "https://" + static_server + '/' + file_path + image.filename
					##'local_url': os.path.join('resources'+os.path.sep + requeste.form['opciones_programas'],image.filename)
				}
	elif requeste.form['escondido_field'] == 'genially':
		return {'genially_url':'https://view.genial.ly/5e32e18a98f5d33c6d5130ee'}
	elif requeste.form['escondido_field'] == 'video':
		pass
	elif requeste.form['escondido_field'] == 'imagen':
		pass
	elif requeste.form['escondido_field'] == 'recap':
		pass
	else:
		pass


## Codigos para plataforma


def subir_codigo(tipo_elemento,params):
	contenido = ""
	if tipo_elemento == 'pdf':
		contenido = "<div style='height:620px'><center><iframe src='"+params['file_url']+"' width='790' height='600'></iframe></center></div><p><a href='"+params['file_url']+"'><button type='button' class='submit btn-brand'><span class='submit-label'>Descargar</span></button></a></p>"

		contenido_despliegue = ""
	elif tipo_elemento == 'genially':

		contenido = "<div style='width: 100%;'><div style='position: relative; padding-bottom: 56.25%; padding-top: 0; height: 0;'><iframe frameborder='0' width='1200' height='675' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;' src='"+params['genially_url']+"' type='text/html' allowscriptaccess='always' allowfullscreen='true' scrolling='yes' allownetworking='all'></iframe></div></div>"



	elif tipo_elemento == 'video':

		contenido = ''

	elif tipo_elemento == 'imagen':

		contenido = ''

	elif tipo_elemento == 'recap':

		contenido = ''

	else:

		contenido = ''

	return Markup(contenido.replace("\\","/"))


