import typing

from django.views                   import generic
from tasks.models                   import Task


# pylint: disable=no-member
class IndexView(generic.ListView):
	"""IndexView is a generic class base view for the index page."""
	template_name = 'tasks/index.html'
	context_object_name = 'tasks'

	def get_queryset(self) -> list[Task]:
		return Task.objects.filter(user=self.request.user)

class DetailView(generic.DetailView):
	"""DetailView is a generic class base view for the detail page."""
	model = Task
	template_name = 'tasks/detail.html'