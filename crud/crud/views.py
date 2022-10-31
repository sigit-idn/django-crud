import json

from django.shortcuts           import render, redirect
from django.http                import HttpResponse
from django.contrib.auth.models import User
from django.views               import generic
from django.urls                import reverse_lazy
from django.contrib.auth        import authenticate, login, logout

class RegisterView(generic.View):
	def get(self, request):
		return render(request, 'register.html')

	def post(self, request):
		username  = request.POST['username']
		email     = request.POST['email']
		name      = request.POST['name']
		password  = request.POST['password']
		password2 = request.POST['password2']

		if password != password2:
			return HttpResponse('Passwords do not match')

		if User.objects.filter(username=username).exists():
			return HttpResponse('Username already exists')

		if User.objects.filter(email=email).exists():
			return HttpResponse('Email already exists')

		user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
		user.save()

		login(request, user)
	
		return redirect('tasks:index')

class LoginView(generic.View):
	def get(self, request):
		return render(request, 'login.html')

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('tasks:index')
		else:
			return render(request, 'login.html')

class LogoutView(generic.View):
	def get(self, request):
		logout(request)
		return redirect('login')
