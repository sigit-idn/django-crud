from typing                     import Any, List, Optional
from django.contrib.auth        import authenticate, login, logout
from django.contrib.auth.models import User
from django.http                import HttpResponse, HttpRequest
from django.shortcuts           import redirect, render
from django.views               import generic


class RegisterView(generic.View):
	"""RegisterView is a generic class base view for the register endpoint."""
	def get(self: object, request: HttpRequest) -> HttpResponse:
		"""Show the register form."""
		return render(request, 'auth/register.html')

	def post(self: object, request: HttpRequest) -> HttpResponse:
		"""Perform the registration."""
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
	"""LoginView is a generic class base view for the login endpoint."""
	def get(self: object, request: HttpRequest) -> HttpResponse:
		"""Show the login form."""
		return render(request, 'auth/login.html')

	def post(self: object, request: HttpRequest) -> HttpResponse:
		"""Perform the login."""
		username = request.POST['username']
		password = request.POST['password']
		user: Optional[User] = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('tasks:index')
		else:
			return render(request, 'auth/login.html', {'error': 'Invalid credentials'})

class LogoutView(generic.View):
	"""LogoutView is a generic class base view for the logout endpoint."""
	def get(self: object, request: HttpRequest) -> HttpResponse:
		"""Perform the logout."""
		logout(request)
		return redirect('login')
