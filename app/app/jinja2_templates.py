from flask import Markup
from pdb import set_trace as bp
import os
import pysftp
import paramiko
from app import app
import re
static_server = "static.sumaysigue.uchile.cl"

def server_connnect():
	ssh_client = paramiko.SSHClient() 
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
	ssh_client.connect(hostname=static_server,port=2837,username='edustatic',password='qD7pcVQF') 
	s = ssh_client.open_sftp()
	return s

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
		#bp()
		checkFolder = None
		try:
			checkFolder = srv.stat(file_path)
		except Exception as e:
			pass

		if checkFolder == None:
		#if not srv.isdir(file_path):
			srv.mkdir(file_path)
		srv.chmod(file_path,0o755)

		if not os.path.isdir(file_path_local):
			os.makedirs(file_path_local)

		image = requeste.files['select_archivo']
		
		file_path_local = os.path.join(file_path_local, image.filename)

		image.save(file_path_local)
		srv.put(file_path_local,file_path+image.filename)
		# srv.put(os.path.join(os.path.dirname(app.root_path),file_path_local).replace('\\','/'),file_path+image.filename)
		#srv.put(file_path_local,file_path+image.filename)
		# srv.chdir(file_path)
		# srv.put(file_path_local)
		srv.close()
		os.remove(file_path_local)

		return {
					'file_url': "https://" + static_server + '/' + file_path + image.filename
					##'local_url': os.path.join('resources'+os.path.sep + requeste.form['opciones_programas'],image.filename)
				}
	elif requeste.form['escondido_field'] == 'genially':
		return {'genially_url':requeste.form['url_genially']}
	elif requeste.form['escondido_field'] == 'video':
		pass
	elif requeste.form['escondido_field'] == 'imagen':
		pass
	elif requeste.form['escondido_field'] == 'recap':
		return {'recap_html': requeste.form['input_html5'].replace('"',"'")}
	else:
		pass


## Codigos para plataforma


def subir_codigo(tipo_elemento,params):
	def option_recap(lista_opts):
		lista_string="<optioninput inline='1'>"
		for option in lista_opts:
			lista_string += "<option correct='"+option['value']+"'>"+option['string']+"</option>"
		lista_string+="</optioninput>"
		return lista_string

	def sacar_espacios(txt):
		return ' '.join(txt.split())


	contenido = {""}
	if tipo_elemento == 'pdf':
		contenido = {"raw_html-1":"<div style='height:620px'><center><iframe src='"+params['file_url']+"' width='790' height='600'></iframe></center></div><p><a href='"+params['file_url']+"'><button type='button' class='submit btn-brand'><span class='submit-label'>Descargar</span></button></a></p>"}

		contenido_despliegue = ""
	elif tipo_elemento == 'genially':

		contenido = {"raw_html-1":"<div style='width: 100%;'><div style='position: relative; padding-bottom: 56.25%; padding-top: 0; height: 0;'><iframe frameborder='0' width='1200' height='675' style='position: absolute; top: 0; left: 0; width: 100%; height: 100%;' src='"+params['genially_url']+"' type='text/html' allowscriptaccess='always' allowfullscreen='true' scrolling='yes' allownetworking='all'></iframe></div></div>"}



	elif tipo_elemento == 'video':

		contenido = {''}

	elif tipo_elemento == 'imagen':

		contenido = {''}

	elif tipo_elemento == 'recap':

		#contenido = '''<div id="divContenedor"></div><script>$('#divContenedor').html($('#input_html5').cleditor()[0].doc.body.innerHTML);</script>'''

		desplegables = re.findall('\{\{(?:[a-zA-Z\s0-9\<\=\'\"\/\>\-\;\:\&]*\_[1|0](?:\s?\,?\s?))*\}\}',params['recap_html'])
		html_option = []
		for desp in desplegables:
			desp_list = [x.strip() for x in desp.replace('{{','').replace('}}','').split(',')]
			opt_list = []
			for x in desp_list:
				opt_list.append({'value':x[-1],'string':x[0:-2]})
			html_option.append(option_recap(opt_list))
		
		html_recap = params['recap_html']
		for i,el in enumerate(html_option):
			html_recap = html_recap.replace(desplegables[i],el)
		contenido = {"raw_html-1":"""
			<img src='https://static.sumaysigue.uchile.cl/cmmeduformacion/produccion/assets/img/bgrecap.png' />
			<script>$( document ).ready(function() {$('.unit-title').hide();})<\/script>
			<style>.multi-inputs-group {text-align: justify;} .submission-feedback{display:none!important;}</style>
			""",
			"blank_common_problem-2":"""<problem><style>
				.recapCapsula{text-align:justify} .recapCapsula p{display:inline} .recapCapsula div{display:inline-block !important;} .recapCapsula ul ul{margin-left: 30px !important;margin-top: 20px;list-style: circle !important;} .recapCapsula ul li div{margin-bottom:0 !important;}
			</style><optionresponse><div class='recapCapsula'>
			"""+html_recap+'</div></optionresponse></problem>'}

	else:

		contenido = {''}

	#return Markup(contenido.replace("\\","/"))
	contenido = {k: sacar_espacios(v) for k, v in contenido.items()}
	contenido = {k: v.replace('<br>','<br/>') for k, v in contenido.items()}
	contenido = {k: Markup(v) for k, v in contenido.items()}
	return contenido


