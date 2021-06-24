from datetime import datetime
from pdb import set_trace as bp
import json
import re

def print_dict(d,s1,s2):
	new = {}
	for k, v in d.items():
		if isinstance(v, dict):
			v = print_dict(v,s1,s2)
		# print(type(v))
		if type(v) == str:
			v = v.replace(s1,s2)
		new[k.replace(s1, s2)] = v
	return new

def customStringDateFormat(string):
	date_from_string = datetime.fromisoformat(string[:-1]).strftime("%d/%m/%Y %H:%M:%S")
	return date_from_string

def customUnique(array):
	return list(set(array))

def customReplace(string):
	if str(string).find("60be5d98bd622580be9de68e") != -1:
		# bp()
		pass
	# string = print_dict(string,'"',"")
	string = re.sub('"(.*)"','&quot;\g<1>&quot;',str(string))
	string = re.sub(r'\\n','&#10;',str(string))
	return string
	# return json.dumps(string)