from wtforms.fields import TextAreaField
from wtforms.validators import ValidationError
from wtforms.widgets import HTMLString, html_params
#from cgi import escape
from wtforms.widgets import TextArea
from pdb import set_trace as bp


class ExtendedTextAreaWidget(TextArea):
	#html_params = staticmethod(html_params)

	def __init__(self, input_type='textarea', text=''):
		self.input_type = input_type
		self.text = text

	def __call__(self, field, **kwargs):
		kwargs.setdefault('id', field.id)
		kwargs.setdefault('type', self.input_type)
		if 'value' not in kwargs:
			kwargs['value'] = field._value()

		html = [u'<textarea %s></textarea>' % html_params(id="input_html5", name="input_html5")]
		#html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
		html.append(u'<link %s />' % html_params(rel='stylesheet', href="static/css/jquery.cleditor.css"))
		html.append(u'<script %s></script>' % html_params(src="static/js/jquery.cleditor.min.js"))
		html.append(u'<script>$(document).ready(function () { $("#input_html5").cleditor({bodyStyle: ""});$(".cleditorMain").append("<div class=''cleditorInstrucciones''>Para agregar un desplesgable, escribe \{\{opcion1_1, opcion2_0, opcion3_0, ...\}\} donde opcionk será el texto del desplesgable y _1 o _0 si es correcta o incorrecta. Solo una correcta por desplesgable</div>") });</script>')

		#<script>
		#		$(document).ready(function () { $("#input_html5").cleditor(); });
		#</script>
		return u''.join(html)
		#return Markup('<textarea %s>' % (html_params(name=field.name, **kwargs), field.text))


class ExtendedTextAreaField(TextAreaField):
	widget = ExtendedTextAreaWidget()

	def __init__(self, label=None, validators=None, text='Save', **kwargs):
		super(ExtendedTextAreaField, self).__init__(label, validators, **kwargs)
		self.text = text

	def _value(self):
		if self.data:
			return u''.join(self.data)
		else:
			return u''
