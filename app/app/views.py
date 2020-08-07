from app import app
from flask import render_template
import os
from flask import send_from_directory
from flask import request, redirect
from app import jinja2_templates
from app.formas_tipo import *
from pdb import set_trace as bp

app.config["IMAGE_UPLOADS"] = os.path.join(app.root_path,"uploads")

@app.route("/")
def index():
	return render_template("public/index.html")


@app.route("/about")
def about():
	return render_template("public/about.html")


@app.route("/uploads", methods=["GET", "POST"])
def uploads():
	if request.method == "POST":
		if request.form['form-button'] == 'Elegir':
			if request.form['tipo_edx'] == 'pdf':
				form = PDFForm(request.form)
			elif request.form['tipo_edx'] == 'genially':
				form = GenForm(request.form)
			elif request.form['tipo_edx'] == 'video':
				form = VideoForm(request.form)
			elif request.form['tipo_edx'] == 'imagen':
				form = ImageForm(request.form)
			elif request.form['tipo_edx'] == 'recap':
				form =  RecapForm(request.form)

			return render_template("public/uploads.html", 
				segundo_paso=request.form['tipo_edx'], 
				templates=jinja2_templates, 
				form = form)

		else:
			if request.files:
				params = jinja2_templates.generar_params(request)
				#image = request.files["fileinput"]
				#image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
				if request.form['escondido_field'] == 'pdf':
					form = PDFForm(request.form)
				elif request.form['escondido_field'] == 'genially':
					form = GenForm(request.form)
				elif request.form['escondido_field'] == 'video':
					form = VideoForm(request.form)
				elif request.form['escondido_field'] == 'imagen':
					form = ImageForm(request.form)
				elif request.form['escondido_field'] == 'recap':
					form =  RecapForm(request.form)
				return render_template("public/uploads.html",
					tercer_paso="success", 
					segundo_paso=request.form['escondido_field'], 
					templates=jinja2_templates,
					form = form,
					codigo_mostrar=jinja2_templates.subir_codigo(request.form['escondido_field'],params)
					)


	return render_template("public/uploads.html", templates=jinja2_templates)


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():

	if request.method == "POST":

		req = request.form

		missing = list()
		for k, v in req.items():
			if v == "":
				missing.append(k)

		if missing:
			feedback = f"Missing fields for {', '.join(missing)}"
			return render_template("public/sign_up.html", feedback=feedback)

		return redirect(request.url)

	return render_template("public/sign_up.html")

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(app.root_path,'favicon.ico',mimetype='image/vnd.microsoft.icon')
