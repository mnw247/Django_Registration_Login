from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
	return render(request, 'registration.html')

def register(request):
	errors = User.objects.regValidator(request.POST)
	
	if len(errors):
		for key, value in errors.items(): messages.error(request, value)
		return redirect('/')
	else:
		User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
		return redirect('/success')


def login(request):
	err = User.objects.loginValidator(request.POST)
	if err:
		for key,value in err.items():
			print('key:', key, 'value', value)
			messages.error(request, value)
		return redirect('/')
	request.session['id'] = User.objects.get(email = request.POST['email_login']).id
	return redirect('/success')

def success(request):
	first_name = User.objects.get(id=request.session['id']).first_name
	last_name = User.objects.get(id=request.session['id']).last_name
	datetimenow = datetime.now()
	context = {"first_name":first_name, "last_name":last_name, "datetimenow":datetimenow}
	return render(request, 'success.html', context)

