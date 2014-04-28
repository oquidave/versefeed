from django.http import HttpResponse
import sqlite3
import models
import pdb

def get_db_cursor():
	db = sqlite3.connect('quiz/quiz.db')
	return db.cursor()

def save_to_choices_model(qn_id, rows):
	last_id = ""
	for row in rows:
		choice = models.Choices()
		option = row[0]
		isAns = row[1]
		choice.qn_id = qn_id
		choice.choice = option
		choice.is_ans = isAns
		choice.save()
		last_id = choice.id
	return last_id

def save_to_qns_model(quiz_qn, ref):
	qn = models.Qns()
	qn.qn = quiz_qn
	qn.ref = ref
	qn.save()
	return qn.id

def save_to_qns_themes(qn_id, theme_id):
	qns_themes = models.QnsThemes()
	qns_themes.qn_id = qn_id
	qns_themes.theme_id = theme_id
	qns_themes.save()

def save_to_qns_tags(qn_id, tag_id):
	qns_tags = models.QnsTags()
	qns_tags.qn_id = qn_id
	qns_tags.tag_id = tag_id
	qns_tags.save()

def save_to_tags_model(tag):
	tags = models.Tags()
	model_tag = models.Tags.objects.filter(tag=tag)
	if model_tag.exists():
		#this tag is already saved in our model. just return it's id
		return model_tag[0].id
	tags.tag = tag
	tags.save()
	return tags.id

def save_qns_tags(qn_id, tags):
	for tag in tags:
		tag_id = save_to_tags_model(tag)
		save_to_qns_tags(qn_id, tag_id)

def save_to_themes_model(theme_details):
	themes = models.Themes()
	#pdb.set_trace()
	model_theme = models.Themes.objects.filter(theme=theme_details[0])
	if model_theme.exists():
		#this theme is already saved in our model. just return it's id
		return model_theme[0].id
	themes.theme = theme_details[0]
	themes.description = theme_details[1]
	themes.author = theme_details[2]
	themes.save()
	return themes.id

def get_tags(qn_id):
	cursor = get_db_cursor()
	cursor.execute('''select tags.tag from tags inner join tags_qns 
		on tags.tag_id=tags_qns.tag_id 
		where tags_qns.qn_id=?''', (qn_id,))
	rows = cursor.fetchall()
	return rows


def get_theme(qn_id):
	cursor = get_db_cursor()
	cursor.execute('''select themes.theme, themes.description, themes.author 
		from themes_qns inner join themes 
		on themes.theme_id = themes_qns.theme_id 
		where themes_qns.qn_id=?''', (qn_id,))
	return cursor.fetchone()

def get_choices(qn_id):
	cursor = get_db_cursor()
	cursor.execute('''select choice, isAns from choices where qn_id=?''', (qn_id,))
	rows = cursor.fetchall()
	return rows

def get_qn(request):
	cursor = get_db_cursor()
	cursor.execute('''select distinct(qns.qn_id), qns.qn, qns.ref from qns inner join choices on qns.qn_id=choices.qn_id''')
	rows = cursor.fetchall()
	last_id = ""
	for row in rows:
		id, qn, ref = row[0], row[1], row[2]
	 	
	 	'''save this qn to the qn model '''
	 	qn_id = save_to_qns_model(qn, ref)
	 	'''get qn choice and save to the choices model '''
	 	choices = get_choices(id)
	 	last_id = save_to_choices_model(qn_id, choices)
	 	'''get this qn theme and save to the theme model ans then qn-theme model '''
	 	theme = get_theme(id)
	 	#pdb.set_trace()
	 	if theme:
	 		theme_id = save_to_themes_model(theme)
		 	save_to_qns_themes(qn_id, theme_id)
	 	'''get this qn tag and save to the tag model and the qn-tag model'''
	 	tags = get_tags(id)
	 	save_qns_tags(qn_id, tags)

	return str(last_id)

