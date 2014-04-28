from django.shortcuts import render

# Create your views here.
from quiz import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from quiz import versefeed_import
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
import pdb
	
def quiz(request,theme_id, page, quiz_round):
	theme = models.Themes.objects.get(id=theme_id)
	#work on the offsets
	if quiz_round == "1":
		start = 0
		end = 5
	else:
		start = (int(quiz_round) -1) * 5
		end = start * 2
	qns_list = models.Qns.objects.filter(qnsthemes__theme=theme).order_by("id") [start:end]

	paginator = Paginator(qns_list, 1)

	try:
		qn_page = paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer, deliver first page
		qn_page = paginator.page(1)
	except EmptyPage:
		#if page is out of range,deliver last page of results
		qn_page = paginator.page(paginator.num_pages)
	
	pg_no = qn_page.number
	qn_id = qns_list[pg_no-1].id

	qn = models.Qns.objects.get(id = qn_id)
	choices_list = models.Choices.objects.filter(qn_id=qn_id)
	right_choice = [choice for choice in choices_list if choice.is_ans][0]
	request.session['see_score'] = False

	if pg_no == 1:
		ans = "not_answered"
		points = 0
		request.session["points"] = points
	else:
		user_choice_id = request.GET.get("user_choice_id")
		correct_ans = request.session["right_choice"]
		user_choice = request.GET.get("user_choice")
		request.session["user_choice"] = user_choice
		request.session["previous_right_choice"] = request.session["right_choice"]
		if user_choice_id == request.session["right_choice_id"]:
			ans = "correct"
			request.session["points"] += 1
		else:
			ans = "wrong"

	request.session["right_choice_id"] = str(right_choice.id)
	request.session["right_choice"] = right_choice.choice
	return {"qn_page":qn_page, "qn":qn, "choices_list":choices_list, "ans":ans}


def quiz_score(request):
	'''make previous qn & display final score and also go the next round if available'''
	user_choice_id = request.GET.get("user_choice_id")
	user_choice = request.GET.get("user_choice")
	correct_ans = request.session["right_choice"]
	request.session["user_choice"] = user_choice
	request.session["previous_right_choice"] = request.session["right_choice"]
	if user_choice_id == request.session["right_choice_id"]:
		ans = "correct"
		request.session["points"] += 1
	else:
		ans = "wrong"
	quiz_details = {"ans":ans}

	quiz_round = request.session["quiz_round"]
	no_rounds = request.session["no_rounds"]
	if quiz_round < no_rounds:
		#go to the next round
		quiz_details['has_next_round'] = "true"
		quiz_round = int(quiz_round) + 1 #set the next round
		quiz_details['quiz_round'] = quiz_round
	else:
		quiz_details['has_next_round'] = "false"

	return render_to_response("quiz_score.html", 
	quiz_details,
	context_instance=RequestContext(request))


def qn(request):
	'''load the theme quiz for this round via ajax requests'''
	page = request.GET.get("page")
	theme_id = request.session['theme_id']
	quiz_round = request.session['quiz_round']
	quiz_details = quiz(request, theme_id, page, quiz_round)
	html_pg = "qn.html"
	if request.session['see_score']:
		'''done with the qns for this round, show see_score'''
		html_pg = "quiz_score.html"
		request.session['see_score'] = False

	return render_to_response(html_pg, 
		quiz_details,
		context_instance=RequestContext(request))

def themed_quiz(request):
	''' load quiz question for this theme and round number'''
	quiz_round = request.GET.get("quiz_round")
	request.session["quiz_round"] = quiz_round
	page = 1
	if quiz_round == "1":
		#starting round 1
		theme_id = request.GET.get("theme_id")
		no_rounds = request.GET.get("no_rounds")
		request.session['theme_id'] = theme_id
		request.session['no_rounds'] = no_rounds
	else:
		theme_id = request.session["theme_id"]
		no_rounds = request.session['no_rounds']

	quiz_details = quiz(request, theme_id, page, quiz_round)

	quiz_details['no_rounds'] = no_rounds
	quiz_details['quiz_round'] = quiz_round
	return render_to_response("themed_quiz.html", 
		quiz_details,
		context_instance=RequestContext(request))


def get_this_theme(theme_id):
	'''get this theme's details from the db'''
	theme =  models.Themes.objects.get(id=theme_id)
	this_theme_qns = models.Qns.objects.filter(qnsthemes__theme=theme)
	no_this_theme_qns = len(this_theme_qns)
	no_rounds = int(math.ceil(no_this_theme_qns/float(10)))
	return theme, no_this_theme_qns, no_rounds

def get_theme(request):
	'''get theme details that the user clicked and display them in an html div'''
	theme_id = request.GET.get("theme_id")
	theme, no_this_theme_qns, no_rounds = get_this_theme(theme_id)
	return render_to_response("theme.html", {"theme":theme, "no_qns":no_this_theme_qns, "no_rounds":no_rounds, "quiz_round":1})

def get_themes():
	'''get all the themes'''
	themes = models.Themes.objects.order_by("id")
	return themes

def quiz_home(request):
	'''this is the quiz home page. Display all the themes on a side bar'''
	themes = get_themes()
	return render_to_response( "quiz_home.html",
		{'themes':themes},
		context_instance=RequestContext(request)
		)
