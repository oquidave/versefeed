from django.shortcuts import render

# Create your views here.
from quiz import models
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from quiz import versefeed_import
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pdb


def view_qns(request):
	qns_list = models.Qns.objects.all()
	paginator = Paginator(qns_list, 7)

	page = request.GET.get("page")
	try:
		qns = paginator.page(page)
	except PageNotAnInteger:
		#if page is not an integer, deliver first page
		qns = paginator.page(1)
	except EmptyPage:
		#if page is out of range,deliver last page of results
		qns = paginator.page(paginator.num_pages)
	
	return render_to_response("view_qns_paginated.html", {"qns_list":qns})

def view_qn(request):
	this_qn_id =request.GET.get("qn_id")
	qn = models.Qns.objects.get(id = this_qn_id).qn 
	choices_list = models.Choices.objects.filter(qn_id=this_qn_id)
	return render_to_response("qn.html", {"qn":qn, "choices_list":choices_list})

	
def quiz(request,theme_id, page):
	theme = models.Themes.objects.get(id=theme_id)
	qns_list = models.Qns.objects.filter(qnsthemes__theme=theme).order_by("id")[:5]

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
	#pdb.set_trace()
	right_choice = [choice for choice in choices_list if choice.is_ans][0]
	#get user choice

	request.session['see_score'] = False
	#pdb.set_trace()
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


	#pdb.set_trace()
	request.session["right_choice_id"] = str(right_choice.id)
	request.session["right_choice"] = right_choice.choice
	#pdb.set_trace()
	return {"qn_page":qn_page, "qn":qn, "choices_list":choices_list, "ans":ans}

def themed_quiz(request):
	theme_id = request.GET.get("theme_id")
	request.session['theme_id'] = theme_id
	page = request.GET.get("page")
	quiz_details = quiz(request, theme_id, page)
	return render_to_response("themed_quiz.html", 
		quiz_details,
		context_instance=RequestContext(request))

def qn(request):
	page = request.GET.get("page")
	theme_id = request.session['theme_id']
	quiz_details = quiz(request, theme_id, page)
	#pdb.set_trace()
	html_pg = "qn.html"
	if request.session['see_score']:
		html_pg = "quiz_score.html"
		request.session['see_score'] = False
	return render_to_response(html_pg, 
		quiz_details,
		context_instance=RequestContext(request))

def quiz_score(request):
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

	quiz_details = {"ans":ans}
	return render_to_response("quiz_score.html", 
	quiz_details,
	context_instance=RequestContext(request))

def qn_objs(request):
	this_qn_id =request.GET.get("qn_id")
	choices_list = models.Choices.objects.filter(qn_id=this_qn_id)
	return render_to_response("qn_objs.html", {"choices_list":choices_list})

def get_themes():
	themes = models.Themes.objects.order_by("id")
	return themes
def get_theme(request):
	theme_id = request.GET.get("theme_id")
	theme =  models.Themes.objects.get(id=theme_id)
	return render_to_response("theme.html", {"theme":theme})

def quiz_home(request):
	themes = get_themes()
	return render_to_response( "quiz_home.html",
		{'themes':themes},
		context_instance=RequestContext(request)
		)
