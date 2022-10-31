import json

from django.shortcuts               import render
from django.http                    import HttpResponse
from django.contrib.auth.models     import User
from django.views                   import generic
from tasks.models                   import Task
from django.urls                    import reverse_lazy
from django.contrib.auth            import authenticate, login, logout


class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'tasks'

	def get_queryset(self):
		return Task.objects.filter(user=self.request.user)

class DetailView(generic.DetailView):
	model = Task
	template_name = 'detail.html'