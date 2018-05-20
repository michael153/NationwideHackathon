# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest

from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# from student.models import Student

from django.core.urlresolvers import reverse

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import base64, datetime, random, string, time
import numpy as np

def getDrivingScore(userEmail):
	return (50.0 + np.random.random()*50.0)

def getDrivingScoreHistory(userEmail, num, start):
	scores = []
	for i in range(num):
		scores.append(start + np.random.random()*(100 - 50.0))
	return scores

def getDrivingScoreHistoryTrends(userEmail, num):
	scores = []
	scores.append(getDrivingScore(userEmail))
	for i in range(1, num):
		sign = random.randint(0, 1)
		if sign == 0:
			sign = -1
		else:
			sign = 1
		val = scores[i-1] + sign*(np.random.random()*30)
		if val > 100:
			val = 100.0 - np.random.random()*3.0
		if val < 0:
			val = np.random.random()*3.0
		scores.append(val)
	return scores


def getAggressiveTurns(userEmail):
	return (20.0 + np.random.random()*50.0)

def getSpeedingFrequency(userEmail):
	return np.random.random()*50.0

def getSmoothStopping(userEmail):
	return np.random.random()*50.0

def index_view(request):
	data = {}
	data['login'] = False
	data['userInformation'] = None
	if request.user.is_authenticated():
		try:
			data['login'] = True
			data['userInformation'] = {"first_name": request.user.first_name,
									   "last_name": request.user.last_name,
									   "email": request.user.email}
		except ObjectDoesNotExist:
			print("*** Not Authenticated")
	if data['login']:
		data['drivingScore'] = str(round(getDrivingScore(request.user.email), 1))
		data['drivingScoreHistory'] = [str(round(i, 1)) for i in getDrivingScoreHistory(request.user.email, 10, 50)]
		print("*** Authenticated")
	return render(request, 'insurance/index.html', data)


def register_view(request):
	email = request.POST['email']
	password = request.POST['password']
	emailAlreadyRegisted = (len(User.objects.all().filter(username=email)) != 0)
	if not emailAlreadyRegisted:
		user = User.objects.create_user(email, password=password)
		user.first_name = request.POST['first_name']
		user.last_name = request.POST['last_name']
		user.email = email
		user.save()
	return redirect(reverse('insurance:index'))

def login_view(request):
	data = {}
	email = request.POST['email']
	password = request.POST['password']
	user = authenticate(username=email, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
	return redirect(reverse('insurance:index'))

def map_view(request):
	data = {}
	return render(request, 'insurance/map.html', data)

def drivinginfo_view(request):
	data = {}
	data['login'] = False
	data['userInformation'] = None
	if request.user.is_authenticated():
		try:
			data['login'] = True
			data['userInformation'] = {"first_name": request.user.first_name,
									   "last_name": request.user.last_name,
									   "email": request.user.email}
		except ObjectDoesNotExist:
			print("*** Not Authenticated")
			return redirect(reverse('insurance:index'))
	if data['login']:
		data['drivingScore'] = str(round(getDrivingScore(request.user.email), 1))
		data['drivingScoreHistory'] = [str(round(i, 1)) for i in getDrivingScoreHistoryTrends(request.user.email, 40)]
		data['aggressiveTurns'] = str(round(getAggressiveTurns(request.user.email), 1))
		data['speedingFrequency'] = str(round(getSpeedingFrequency(request.user.email), 1))
		data['smoothStopping'] = str(round(getSmoothStopping(request.user.email), 1))
		print("*** Authenticated")
	return render(request, 'insurance/drivinginfo.html', data)

def logout_view(request):
	logout(request)
	return redirect(reverse('insurance:index'))