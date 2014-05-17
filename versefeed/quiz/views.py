from django.shortcuts import render

# Create your views here.
from quiz import models
from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from quiz import versefeed_import
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
import pdb
	
def quiz(request,theme_id, page, quiz_round, resumed=False):
	"""Mark the previous qn if not first qn as well as load current qn with its objectives"""
	theme = models.Themes.objects.get(id=theme_id)
	#work on the offsets
	if int(quiz_round) == 1:
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

	ans = "not_answered"
	if not resumed:
		if pg_no == 1:
			round_pts = 0
			request.session["round_pts"] = round_pts
		else:
			user_choice_id = request.GET.get("user_choice_id")
			user_choice = request.GET.get("user_choice")
			correct_ans = request.session["right_choice"]
			request.session["user_choice"] = user_choice
			request.session["previous_right_choice"] = request.session["right_choice"]
			#mark the previous qn
			if user_choice_id == request.session["right_choice_id"]:
				ans = "correct"
				request.session["round_pts"] += 1
				request.session["quiz_pts"] += 1
			else:
				ans = "wrong"
	#store the right objective of this qn, so we mark the user when next page is loaded
	request.session["right_choice_id"] = str(right_choice.id)
	request.session["right_choice"] = right_choice.choice
	return {"theme":theme, "qn_page":qn_page, "qn":qn, "choices_list":choices_list, "ans":ans}

def pause(request):
	'''persist user's session'''

	user_id, theme_id, quiz_round, no_rounds, round_pg, round_pts, quiz_pts = request.user.id, int(request.session['theme_id']), \
	int(request.session['quiz_round']), int(request.session['no_rounds']), int(request.GET.get("page")),request.session['round_pts'], request.session['quiz_pts']

	user_session = models.UserSession()
	user_session.user_id = user_id 
	user_session.theme_id = theme_id
	user_session.quiz_round = quiz_round
	user_session.no_rounds = no_rounds
	user_session.round_pg = round_pg
	user_session.round_pts = round_pts
	user_session.quiz_pts = quiz_pts 
	#pdb.set_trace()
	user_session.save()
	return HttpResponse("saved the session")

def resume_quiz(request):
	'''resume quiz that user had paused '''
	theme_id = int(request.GET.get('theme_id'))
	user_session = models.UserSession.objects.get(theme_id=theme_id)
	user_id = user_session.user_id
	round_pg = user_session.round_pg
	quiz_round = user_session.quiz_round
	no_rounds = user_session.no_rounds
	request.session['theme_id'] = theme_id
	request.session['quiz_round'] = quiz_round
	request.session['no_rounds'] = no_rounds
	request.session['round_pts'] = user_session.round_pts
	request.session['quiz_pts'] = user_session.quiz_pts

	quiz_details = quiz(request, theme_id, round_pg, quiz_round, resumed=True)
	
	quiz_details['no_rounds'] = no_rounds
	quiz_details['quiz_round'] = quiz_round
	quiz_details['quiz_pts'] = quiz_pts

	#lets delete this paused session in the user session table
	paused_quiz = models.UserSession.objects.get(theme_id=theme_id, user_id=user_id)
	paused_quiz.delete()
	return render_to_response("themed_quiz.html", 
		quiz_details,
		context_instance=RequestContext(request))



def quiz_score(request):
	'''make previous qn & display final score and also go the next round if available'''
	user_choice_id = request.GET.get("user_choice_id")
	user_choice = request.GET.get("user_choice")
	correct_ans = request.session["right_choice"]
	request.session["user_choice"] = user_choice
	request.session["previous_right_choice"] = request.session["right_choice"]
	#mark the user
	if user_choice_id == request.session["right_choice_id"]:
		ans = "correct"
		request.session["round_pts"] += 1
		request.session["quiz_pts"] += 1
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
		#done with the qns for this round, show see_score
		html_pg = "quiz_score.html"
		request.session['see_score'] = False

	return render_to_response(html_pg, 
		quiz_details,
		context_instance=RequestContext(request))

def themed_quiz(request):
	''' load quiz question for this theme and round number'''
	quiz_round = request.GET.get("quiz_round")
	request.session["quiz_round"] = quiz_round
	page = 1 #display one question for page
	quiz_pts = 0
	if quiz_round == "1":
		#starting round 1
		theme_id = request.GET.get("theme_id")
		no_rounds = request.GET.get("no_rounds")
		#store these in session variable for subsequent quiz rounds
		request.session['theme_id'] = theme_id
		request.session['no_rounds'] = no_rounds
		request.session['quiz_pts'] = quiz_pts
	else:
		theme_id = request.session["theme_id"]
		no_rounds = request.session['no_rounds']
		quiz_pts = request.session['quiz_pts']

	quiz_details = quiz(request, theme_id, page, quiz_round)

	quiz_details['no_rounds'] = no_rounds
	quiz_details['quiz_round'] = quiz_round
	return render_to_response("themed_quiz.html", 
		quiz_details,
		context_instance=RequestContext(request))

def check_paused(theme_id):
	 if not models.UserSession.objects.filter(theme_id=theme_id).exists():
	 	return False
	 return True 


def get_this_theme(theme_id):
	'''get this theme's details from the db'''
	theme =  models.Themes.objects.get(id=theme_id)
	this_theme_qns = models.Qns.objects.filter(qnsthemes__theme=theme)
	no_this_theme_qns = len(this_theme_qns)
	qns_per_round = 5 #have 5 questions per round. last Round may have less than 5 questions of course
	no_rounds = int(math.ceil(no_this_theme_qns/float(qns_per_round))) #round up e.g 2.2 quiz rounds rounds off to 3 rounds 
	return theme, no_this_theme_qns, no_rounds

def get_theme(request):
	'''get theme details that the user clicked and display them in the theme_details html div'''
	theme_id = request.GET.get("theme_id")
	theme, no_this_theme_qns, no_rounds = get_this_theme(theme_id)
	#check if user already starting doing a quiz with this theme
	paused = "false"
	if check_paused(theme_id):
		paused = "true"
	return render_to_response("theme.html", {"theme":theme, "no_qns":no_this_theme_qns, 
		"no_rounds":no_rounds, "quiz_round":1, "paused":paused})

def get_themes():
	'''get all the themes'''
	themes = models.Themes.objects.order_by("id")
	return themes

def quiz_home(request):
	'''this is the quiz home page. Display all the themes on a side bar'''
	themes = get_themes()
	return render_to_response("quiz_home.html",
		{'themes':themes},
		context_instance=RequestContext(request)
		)

def login(request):
	'''login '''
	return render_to_response('login.html')

def logout(request):
	'''logout '''
	auth.logout(request)
	#Redirect to home page
	return HttpResponseRedirect("/quiz/")


def contact(request):
	'''server the contact us form or something similar'''
	return render_to_response('contact.html')

def about(request):
	'''about us stuff'''
	return render_to_response('about.html')
