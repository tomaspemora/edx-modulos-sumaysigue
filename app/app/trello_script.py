from trello import TrelloClient
from pdb import set_trace as bp
from datetime import date
from datetime import datetime
from pprint import pprint
import time, json, os.path, sys, requests, getopt, os, json, cProfile
from termcolor import colored
import dill as pickle

from difflib import SequenceMatcher
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config

with open("keys-trello.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

api_mia = jsonObject['api_mia']
token_mio = jsonObject['token_mio']

client = TrelloClient(
	api_key=api_mia,
	api_secret='your-secret',
	token=token_mio,
	token_secret='your-oauth-token-secret'
)

def unique(list1):
	# insert the list to the set
	list_set = set(list1)
	# convert the set to the list
	return list(list_set)
	
def prettyDicts(d, indent=0):
	if isinstance(d,list) or isinstance(d,set):
		for i in range(len(d)):
			print('\t' * (indent) + str(i),end='')
			prettyDicts(d[i], indent+1)
	elif isinstance(d, dict):
		for key, value in d.items():
			print('\t' * indent + str(key))
			if isinstance(value, dict):
				prettyDicts(value, indent+1)
			else:
				print('\t' * (indent+1) + str(value))
		print('\t' * (indent) +'________________________')
	else:
		print('\t' * (indent+1) + str(d))


def urlRequest(id_board,field):
	url = "https://api.trello.com/1/boards/"+id_board+"/"+field

	query = {
	   'key': api_mia,
	   'token': token_mio
	}

	response = requests.request(
	   "GET",
	   url,
	   params=query
	)
	try:
		return response.json()
	except:
		return None

def urlRequestAllCardInBoard(id_board):
	url = "https://api.trello.com/1/boards/"+id_board+"/actions/?limit=1000"

	query = {
	   'key': api_mia,
	   'token': token_mio
	}

	response = requests.request(
	   "GET",
	   url,
	   params=query
	)

	try:
		return response.json()
	except:
		return None

def urlRequestCard(id_cards,card_field):

	url = "https://api.trello.com/1/batch"

	url_f = ''
	for id_card in id_cards:
		url_f = url_f + '/cards/' + id_card+'/'+card_field+"?filter=all&limit=1000,"
		# url_f = url_f + '/cards/' + id_card+'/'+card_field+"?filter=all,"
	url_f = url_f[0:len(url_f)-1]
	

	headers = {
	   "Accept": "application/json"
	}

	query = {
	   'key': api_mia,
	   'token': token_mio,
	   'urls' : '{}'.format(url_f)
	}
	# response.__dict__['url'].split('&')[-1]


	response = requests.request(
	   "GET",
	   url,
	   headers=headers,
	   params=query
	)

	if response.text != None:
		for els in response.json():
			print('Numero de elementos recibidos '+ str(len(els['200'])))
		return response.json()
	else:
		print('ERROR EN TARJETA ->' + id_card)
		return None

def getMemberByName(members_list,members_name):
	
	members_found = []
	if type(members_name) == str:
		members_name = [members_name]
	for j in range(len(members_name)):
		for i in range(len(members_list)):
			if members_list[i].full_name == members_name[j]:
				members_found.append(members_list[i])
	return members_found

# retorna 
def detectCardMovement(cardAction):
	card_movement = {}

	# if cardAction['data']['card']['name'] in  ['[PYE] U1_Proyecto - Lección 1','[PYE] U1A1 - Clase 5']:
		# prettyDicts(cardAction)
		# print(colored('_______________','red'))

	if cardAction['type'] == 'addAttachmentToCard':
		card_movement['card_id'] = cardAction['data']['card']['id']
		card_movement['card_name'] = cardAction['data']['card']['name']
		card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
		card_movement['type_action'] = cardAction['type']
		bp()
		card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
		card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
		card_movement['attachment_name'] = cardAction['data']['attachment']['name']
		card_movement['attachment_url'] = cardAction['data']['attachment']['url'] if 'url' in cardAction['data']['attachment'] else 'no url'

	if cardAction['type'] == 'addMemberToCard':	
		card_movement['card_id'] = cardAction['data']['card']['id']
		card_movement['card_name'] = cardAction['data']['card']['name']
		card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
		card_movement['type_action'] = cardAction['type']
		card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
		card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
		card_movement['member_adder'] = cardAction['memberCreator']['fullName']

	if cardAction['type'] == 'removeMemberFromCard':
		card_movement['card_id'] = cardAction['data']['card']['id']
		card_movement['card_name'] = cardAction['data']['card']['name']
		card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
		card_movement['type_action'] = cardAction['type']
		card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
		card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
		card_movement['member_remover'] = cardAction['memberCreator']['fullName']

	if cardAction['type'] == 'commentCard':
		card_movement['card_id'] = cardAction['data']['card']['id']
		card_movement['card_name'] = cardAction['data']['card']['name']
		card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
		card_movement['type_action'] = cardAction['type']
		card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
		card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
		card_movement['text_commented'] = cardAction['data']['text']

	if cardAction['type'] == 'updateCard' and 'listBefore' in cardAction['data'] and 'listAfter' in cardAction['data']:
		card_movement['card_id'] = cardAction['data']['card']['id']
		card_movement['card_name'] = cardAction['data']['card']['name']
		card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
		card_movement['type_action'] = cardAction['type']
		card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
		card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
		card_movement['listBefore'] = cardAction['data']['listBefore']['id']
		card_movement['listAfter'] = cardAction['data']['listAfter']['id']
		card_movement['listBefore_n'] = cardAction['data']['listBefore']['name']
		card_movement['listAfter_n'] = cardAction['data']['listAfter']['name']

	if cardAction['type'] == 'updateCard' and 'old' in cardAction['data']:
		if 'desc' in cardAction['data']['old']:
			card_movement['card_id'] = cardAction['data']['card']['id']
			card_movement['card_name'] = cardAction['data']['card']['name']
			card_movement['card_url'] = 'https://trello.com/c/'+cardAction['data']['card']['shortLink']
			card_movement['type_action'] = cardAction['type'] + 'Desc'
			card_movement['date_action_shrunk'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y")
			card_movement['date_action'] = datetime.fromisoformat(cardAction['date'][:-1]).strftime("%d/%m/%y, %H:%M")
			match = SequenceMatcher(a=cardAction['data']['card']['desc'], b=cardAction['data']['old']['desc']).find_longest_match(0,len(cardAction['data']['card']['desc']),0,len(cardAction['data']['old']['desc']),)
			card_movement['desc_update'] = cardAction['data']['card']['desc'].replace(cardAction['data']['card']['desc'][match.a:match.a+match.size],'')
	return card_movement

# retorna las tareas de una persona en un tablero
def tareasPorPersona(dict_creado,tablero,personas=None):

	members = dict_creado[tablero]['members']
	if personas is None:
		personas = members
	else:
		personas = getMemberByName(members,personas)

	tarjetas = dict_creado[tablero]['cards']
	acts_per_members = {}
	lista_acciones = []
	tipo_acciones = []
	for i in range(len(personas)):
		acts = {}
		batch_counter = 0
		batch_actual = []
		acciones_batch = []
		nombres_tarjetas = []
		for j in range(len(tarjetas)):

			if batch_counter < 10:
				batch_counter += 1
				batch_actual.append(tarjetas[j].id)

			if batch_counter == 10 or j == len(tarjetas)-1:
				acciones_batch_aux = urlRequestCard(batch_actual,'actions')
				for x in acciones_batch_aux:
					acciones_batch.append(x['200'])
					nombres_tarjetas.append(tarjetas[j].name)
				batch_counter = 0
				batch_actual = []
		acciones = acciones_batch
		for j in range(len(acciones)):
			acciones_dentro_tarjeta = acciones[j]
			actividades = {}
			for k in range(len(acciones_dentro_tarjeta)):
				
				tipo_acciones.append(acciones_dentro_tarjeta[k]['type'])
				if 'member' in acciones_dentro_tarjeta[k]:
					bool_check = personas[i].id in [ acciones_dentro_tarjeta[k]['member']['id']]
				else:
					bool_check = personas[i].id in [ acciones_dentro_tarjeta[k]['memberCreator']['id']]

				if bool_check:
					card_move = detectCardMovement(acciones_dentro_tarjeta[k])
					if card_move != {}:						
						actividades[len(actividades)] = card_move

			if len(actividades) > 0:
				acts[actividades[0]['card_name']] = actividades

		acts_per_members[personas[i].full_name] = acts
	# print('tipo de movimientos ',end='')
	# print(unique(tipo_acciones))
	return acts_per_members


def ordenarTareasPorFecha(tareas_de_1_persona):
	dates = []
	for tarjeta in tareas_de_1_persona:
		for tarea in tareas_de_1_persona[tarjeta]:
			dates.append(tareas_de_1_persona[tarjeta][tarea]['date_action_shrunk'])
	
	dates_unique = unique(dates)
	
	dates_unique.sort(key=lambda date: datetime.strptime(date, "%d/%m/%y"))

	dates_in_iso_format = []
	for dys in dates_unique:
		dates_in_iso_format.append(datetime.strptime(dys, "%d/%m/%y").isocalendar())
	dates_in_iso_format.sort()
	wks = []
	for dys in dates_in_iso_format:
		if str(dys[0]).zfill(2)+'_'+str(dys[1]).zfill(2) not in wks:
			wks.append(str(dys[0]).zfill(2)+'_'+str(dys[1]).zfill(2))
	wks.sort()

	tareas_ordenadas = {}
	for wk in wks:
		tareas_ordenadas[wk] = {}
		for fecha in dates_unique:
			aux_fecha = datetime.strptime(fecha, "%d/%m/%y").isocalendar()
			if str(aux_fecha[0]).zfill(2)+'_'+str(aux_fecha[1]).zfill(2) == wk:
				tareas_ordenadas[wk][fecha] = []
				for tarjeta in tareas_de_1_persona:
					for tarea in tareas_de_1_persona[tarjeta]:
						if tareas_de_1_persona[tarjeta][tarea]['date_action_shrunk'] == fecha:
							tareas_ordenadas[wk][fecha].append(tareas_de_1_persona[tarjeta][tarea])
	return tareas_ordenadas

def displayTareasOrdenadasPorSemana(tareas_ordenadas,orden_de_listas):
	
	for week in tareas_ordenadas:
		year_and_week = week.split('_')
		lunes = str(datetime.fromisocalendar(int(year_and_week[0]), int(year_and_week[1]), 1).strftime("%d/%m/%y"))
		viernes = str(datetime.fromisocalendar(int(year_and_week[0]), int(year_and_week[1]), 5).strftime("%d/%m/%y"))
		print('\n')
		print(colored(week + ': del Lunes '+lunes+' al Viernes '+viernes,'cyan', attrs=['reverse','dark','bold']))	
		print('\n')
		tareas_ordenadas_de_la_semana = sum(tareas_ordenadas[week].values(), [])
		tareas_colapsadas = []
		tareas_colapsadas_cards_id_list = []

		for tarea in tareas_ordenadas_de_la_semana:
			dict_aux = {}

			if tarea['card_id'] in tareas_colapsadas_cards_id_list:
				idx = tareas_colapsadas_cards_id_list.index(tarea['card_id'])
				tareas_colapsadas[idx]['type_actions'].append(tarea['type_action'])
				tareas_colapsadas[idx]['dates'].append(tarea['date_action'])
				
				dict_aux_actions_from_to = [None, None]
				dict_aux_actions_from_to_ids = [None, None]
				dict_aux_text_commented = None
				dict_aux_member_adder = None
				dict_aux_member_remover = None
				dict_aux_attachment_name = None
				dict_aux_attachment_url = None
				dict_aux_desc_update = None

				if tarea['type_action'] == 'updateCard':
					dict_aux_actions_from_to = [tarea['listBefore_n'], tarea['listAfter_n']]
					dict_aux_actions_from_to_ids = [tarea['listBefore'], tarea['listAfter']]
				
				if tarea['type_action'] == 'commentCard':
					dict_aux_text_commented = tarea['text_commented']

				if tarea['type_action'] == 'addMemberToCard':
					dict_aux_member_adder = tarea['member_adder']

				if tarea['type_action'] == 'removeMemberFromCard':
					dict_aux_member_remover = tarea['member_remover']

				if tarea['type_action'] == 'addAttachmentToCard':
					dict_aux_attachment_name = tarea['attachment_name']
					dict_aux_attachment_url = tarea['attachment_url']

				if tarea['type_action'] == 'updateCardDesc':
					dict_aux_desc_update = tarea['desc_update']

				tareas_colapsadas[idx]['actions_from_to'].append(dict_aux_actions_from_to)
				tareas_colapsadas[idx]['actions_from_to_ids'].append(dict_aux_actions_from_to_ids)
				tareas_colapsadas[idx]['text_commented'].append(dict_aux_text_commented)
				tareas_colapsadas[idx]['member_adder'].append(dict_aux_member_adder)
				tareas_colapsadas[idx]['member_remover'].append(dict_aux_member_remover)
				tareas_colapsadas[idx]['attachment_name'].append(dict_aux_attachment_name)
				tareas_colapsadas[idx]['attachment_url'].append(dict_aux_attachment_url)
				tareas_colapsadas[idx]['desc_update'].append(dict_aux_desc_update)


			else:
				dict_aux['card_id'] = tarea['card_id']
				if 'card_url' not in  tarea:
					pass
				dict_aux['card_url'] = tarea['card_url'] if 'card_url' in tarea else 'no-link'

				dict_aux['card_name'] = tarea['card_name']
				dict_aux['type_actions'] = [tarea['type_action']]
				dict_aux['dates'] = [tarea['date_action']]

				dict_aux['actions_from_to'] = [[None, None]]
				dict_aux['actions_from_to_ids'] = [[None, None]]
				dict_aux['text_commented'] = [None]
				dict_aux['member_adder'] = [None]
				dict_aux['member_remover'] = [None]
				dict_aux['attachment_name'] = [None]
				dict_aux['attachment_url'] = [None]
				dict_aux['desc_update'] = [None]

				if tarea['type_action'] == 'updateCard':
					dict_aux['actions_from_to'] = [[tarea['listBefore_n'], tarea['listAfter_n']]]
					dict_aux['actions_from_to_ids'] = [[tarea['listBefore'], tarea['listAfter']]]

				if tarea['type_action'] == 'updateCardDesc':
					dict_aux['desc_update'] = [tarea['desc_update']]
				
				if tarea['type_action'] == 'commentCard':
					dict_aux['text_commented'] = [tarea['text_commented']]

				if tarea['type_action'] == 'addMemberToCard':
					dict_aux['member_adder'] = [tarea['member_adder']]

				if tarea['type_action'] == 'removeMemberFromCard':
					dict_aux['member_remover'] = [tarea['member_remover']]

				if tarea['type_action'] == 'addAttachmentToCard':
					dict_aux['attachment_name'] = [tarea['attachment_name']]
					dict_aux['attachment_url'] = [tarea['attachment_url']]

				tareas_colapsadas.append(dict_aux)
				tareas_colapsadas_cards_id_list.append(tarea['card_id'])
		
		for tarea in tareas_colapsadas:
			index_to_resort = sorted([[i,k] for i,k in enumerate(tarea['dates'])],key=lambda item: datetime.strptime(item[1], "%d/%m/%y, %H:%M"))
			index_to_resort = [i[0] for i in index_to_resort]

			tarea['dates'] = [x for _, x in sorted(zip(index_to_resort,tarea['dates']))]
			tarea['type_actions'] = [x for _, x in sorted(zip(index_to_resort,tarea['type_actions']))]
			tarea['actions_from_to'] = [x for _, x in sorted(zip(index_to_resort,tarea['actions_from_to']))]
			tarea['actions_from_to_ids'] = [x for _, x in sorted(zip(index_to_resort,tarea['actions_from_to_ids']))]
			tarea['text_commented'] = [x for _, x in sorted(zip(index_to_resort,tarea['text_commented']))]
			tarea['member_adder'] = [x for _, x in sorted(zip(index_to_resort,tarea['member_adder']))]
			tarea['member_remover'] = [x for _, x in sorted(zip(index_to_resort,tarea['member_remover']))]
			tarea['attachment_name'] = [x for _, x in sorted(zip(index_to_resort,tarea['attachment_name']))]
			tarea['attachment_url'] = [x for _, x in sorted(zip(index_to_resort,tarea['attachment_url']))]
			tarea['desc_update'] = [x for _, x in sorted(zip(index_to_resort,tarea['desc_update']))]

		for tarea in tareas_colapsadas:
			c = 1
			print('\t'+'{0: <45}'.format(tarea['card_name']),end='\n')
			print('\t'+'{0: <60}'.format(colored(' '+tarea['card_url'],'green')),end='')
			for i in range(0,len(tarea['dates'])):
				print('\t\t'+'{0: <20}'.format(tarea['type_actions'][i]),end='')

				if tarea['type_actions'][i] == 'addAttachmentToCard':
					nombre_adjunto = tarea['attachment_name'][i]
					url_adjunto = tarea['attachment_url'][i]
					print(
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' -> ','yellow') + 
						'{0: <100}'.format(str(nombre_adjunto[0:min(45,len(str(nombre_adjunto)))])+
						colored(' url('+ str(nombre_adjunto[0:min(42,len(str(nombre_adjunto)))])+')','magenta')),end='')
				
				if tarea['type_actions'][i] == 'removeMemberFromCard':
					miembro_que_remuevo = tarea['member_remover'][i]
					print(
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' -> ','red') + 
						'{0: <91}'.format(str(miembro_que_agrego[0:min(91,len(str(miembro_que_remuevo)))])) ,end='')

				if tarea['type_actions'][i] == 'addMemberToCard':
					miembro_que_agrego = tarea['member_adder'][i]
					print(
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' -> ','yellow') + 
						'{0: <91}'.format(str(miembro_que_agrego[0:min(91,len(str(miembro_que_agrego)))])) ,end='')

				if tarea['type_actions'][i] == 'commentCard':
					texto = tarea['text_commented'][i].replace('\n','')
					print(
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' -> ','yellow') + 
						'{0: <91}'.format(str(texto[0:min(91,len(str(texto)))])) ,end='')

				if tarea['type_actions'][i] == 'updateCardDesc':
					textoDesc = str(tarea['desc_update'][i]).replace('\n','')
					print(
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' -> ','yellow') + 
						'{0: <91}'.format(str(textoDesc[0:min(91,len(str(textoDesc)))])) ,end='')

				if tarea['type_actions'][i] == 'updateCard':
					print(
						colored('{0: <45}'.format(str(tarea['actions_from_to'][i][0])),'cyan') + 
						colored('- ','yellow') + 
						colored(tarea['dates'][i].replace(' ',''),'green') + 
						colored(' ->','yellow') + 
						colored('{0: >45}'.format(str(tarea['actions_from_to'][i][1])),'cyan'),end='')
				

				print('',end=colored(' |'+str(c)+'|','red'))
				print('',end='\n')
				
				if c<len(tarea['dates']):
					print('\t\t'+'{0: <45}'.format(''),end='')
				
				c+=1
			print('')

def getBoardData(tableros_relevantes,equipos_relevantes,client,since_filter,before_filter):
	boards_dict = {}
	all_boards = client.list_boards()
	for i in range(len(all_boards)):
		if all_boards[i].name in tableros_relevantes:
			org = urlRequest(all_boards[i].id,'organization')['displayName']
			if org in equipos_relevantes:
				# urlRequestCardsfromBoard(all_boards[i].id,since_filter,before_filter)
				# urlRequestAllCardInBoard(all_boards[i].id)
				boards_dict[all_boards[i].name] = {
												'id': all_boards[i].id,
												'labels': all_boards[i].get_labels(),
												'cards' : all_boards[i].get_cards(filters={'since':since_filter,'before':before_filter}),
												'n_cards': len(all_boards[i].get_cards(filters={'since':since_filter,'before':before_filter})),
												'columnas': all_boards[i].get_lists('open'),
												'members': all_boards[i].get_members()
												}
	return boards_dict

## Lee datos de tablero de trello si no existe archivo previo y luego guardar en archivo .bin

def ReadnSaveBoardData(nombre_archivo,equipo,tablero,since_filter,before_filter):

	if os.path.exists(nombre_archivo):
		#read file with existent data
		print('Leyendo datos guardados')
		with open(nombre_archivo,'rb') as outfile:  # Python 3: open(..., 'rb')
			boards_dict = pickle.load(outfile)
	else:
		#get data from trello board and write to file
		print('Leyendo datos desde Trello')
		boards_dict = getBoardData(tablero,equipo,client,since_filter,before_filter)
		with open(nombre_archivo, 'wb') as outfile:  # Python 3: open(..., 'wb')
			pickle.dump(boards_dict, outfile)
	return boards_dict

## Nuevas funciones para analisis por tablero


def getAllCardsInfo():
	board_name = 'Liceo digital'

	all_boards = client.list_boards()
	alldata = getBoardData(board_name,'CMMEdu',client,'2001-01-01','2030-01-01')
	all_cards_names = alldata[board_name]['cards']
	batch_counter = 0
	batch_actual = []
	acciones_batch = []
	nombres_tarjetas = []

	all_cards_names = all_cards_names[10:14]
	for j in range(len(all_cards_names)):

		if batch_counter < 10:
			batch_counter += 1
			batch_actual.append(all_cards_names[j].id)

		if batch_counter == 10 or j == len(all_cards_names)-1:
			# bp()
			acciones_batch_aux = urlRequestCard(batch_actual,'actions')
			for x in acciones_batch_aux:
				acciones_batch.append(x['200'])
				# bp()
				nombres_tarjetas.append(all_cards_names[j].name)
			batch_counter = 0
			batch_actual = []
	all_cards = acciones_batch
	dates_of_actions_in_cards = []
	for card in all_cards:
		dates_of_this_card = []
		for action in card:
			 dates_of_this_card.append({'date' : action['date'], 'type' : action['type'], 'id': action['id']})
		sorted(dates_of_this_card, key=lambda x: x['date'])
		dates_of_actions_in_cards.append(dates_of_this_card)


	prettyDicts(dates_of_actions_in_cards)	
	bp()

	# prettyDicts(all_cards[1])
	return all_cards

def main(argv):
	os_var = os.system('cls')
	usuarios = ''
	tableros = ''
	since_filter = '2010-01-01'
	before_filter = '2099-01-01'
	force_new = False
	try:
		opts, args = getopt.getopt(argv,"hu:t:s:b:f",["usuarios=","tableros=","since=","before=","forcenew="])
	except getopt.GetoptError:
		print('script.py -u <usuarios> -t <tableros> -since <since_date> -before <before_date> -f')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('script.py -u <usuarios> -t <tableros>')
			sys.exit()
		elif opt in ("-u", "--usuarios"):
			usuarios = arg
		elif opt in ("-t", "--tableros"):
			tableros = arg
		elif opt in ("-s", "--since"):
			since_filter = arg
		elif opt in ("-b", "--before"):
			before_filter = arg
		elif opt in ("-f", "--forcenew"):
			force_new = True
	print('Los usuarios seleccionados son ' + json.dumps(usuarios))
	print('Los tableros seleccionados son ' + json.dumps(tableros))
	print('Se aplicara un filtro entre ' +since_filter +' y ' + before_filter)
	return [usuarios,tableros,since_filter,before_filter,force_new]


if __name__ == "__main__":
	config = Config(max_depth=4)
	with PyCallGraph(output=GraphvizOutput(),config=config):

		# py script.py -u "Thomas Peet" -t "Liceo digital" -s "2021-05-15" -b "2021-06-30"
		start_time = time.time()
		params = main(sys.argv[1:])
		personas_a_consultar = set((params[0]).split(","))
		tableros_relevantes = set((params[1]).split(","))
		since_filter = params[2]
		before_filter = params[3]
		force_new = params[4]
		equipos_relevantes = {'CMMEdu'}
		fields_relevantes = {}
		nombres_tableros = list(tableros_relevantes)
		nombres_equipos = list(equipos_relevantes)
		board_dict =  {}

		for equipo in nombres_equipos:
			board_dict[equipo] = {}
			for tablero in nombres_tableros:
				print('equipo:'+equipo+' tablero:'+tablero)
				nombre_archivo_data_equipoytablero_con_filtrofecha = 'data_equipo-'+equipo+'_tablero-'+tablero+'_fechas-'+since_filter+'-'+before_filter+'.pkl'
				board_dict[equipo][tablero] = ReadnSaveBoardData(nombre_archivo_data_equipoytablero_con_filtrofecha,equipo,tablero,since_filter,before_filter)
		print('La lectura tomo : '+str(time.time() - start_time))
		one_board_dict = board_dict[equipo][tablero] # por ahora solo 1 tablero

		
		orden_de_listas = ['Listo para conceptualización','Construcción Guion','Construcción Guion listo','Diseño haciendo','Diseño Listo','Montaje haciendo','Montaje listo','Revisión lista','Ajustes aplicados','Lista para subir a Aula 360','Listo','Corrección de estilo (Mat complementario)']

		if True:
			for persona_consulta in personas_a_consultar:
				print(persona_consulta)
				for tablero_r in tableros_relevantes:
					nombre_archivo_json = 'edata_'+persona_consulta+'_'+tablero_r+'_since-'+since_filter+'_before-'+before_filter+'.json'
					if os.path.exists(nombre_archivo_json) and (not force_new):
						#read json file with existent data
						with open(nombre_archivo_json) as json_file:
							tareas = json.load(json_file)
					else:
						#get data from trello board and write to json file
						tareas = tareasPorPersona(one_board_dict,tablero_r,persona_consulta)
						with open(nombre_archivo_json,'w') as outfile:
							json.dump(tareas, outfile)

					tareas_de_1_persona_ordenadas = ordenarTareasPorFecha(tareas[persona_consulta])
					displayTareasOrdenadasPorSemana(tareas_de_1_persona_ordenadas,orden_de_listas)
		print('La ejecución completa tomo : '+str(time.time() - start_time))
		'''

		Por hacer:

		- Implementar display en pagina web por tarea que muestre la evolución de cada una.
		- Implementar otro tipo de acciones diferentes a las ya implementadas (falta createCard por ej). ver https://developer.atlassian.com/cloud/trello/guides/rest-api/action-types/

		'''	