import json

from typing        import Any
from django.http   import JsonResponse, HttpRequest
from django.views  import generic
from tasks.models  import Task
from chunks.models import Chunk


# pylint: disable=no-member
class TasksView(generic.View):
	"""TasksView is a generic class base view for the tasks endpoint."""
	def post(self: object, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle POST requests."""
		request_body = json.loads(request.body)

		task: Task = Task.objects.create(
			title       = request_body['title'],
			description = request_body['description'],
			due_date    = request_body['due_date'],
			user		= request.user
		)

		task.save()
		return JsonResponse(task.to_json())

class TaskView(generic.View):
	"""TaskView is a generic class base view for the task endpoint."""
	def get(self: object, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle GET requests."""
		task = Task.objects.get(id=self.kwargs['id'])
		return JsonResponse(task.to_json())

	def put(self: object, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle PUT requests."""
		task: Task = Task.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)

		task.title       = request_body['title']
		task.description = request_body['description']
		task.due_date    = request_body['due_date']
		task.started_at	 = request_body['started_at']

		task.save()
		return JsonResponse(task.to_json())

	def patch(self: object, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle PATCH requests."""
		task = Task.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)

		task.title       = request_body['title']       if 'title'       in request_body else task.title
		task.description = request_body['description'] if 'description' in request_body else task.description
		task.due_date    = request_body['due_date']    if 'due_date'    in request_body else task.due_date
		task.started_at  = request_body['started_at']  if 'started_at'  in request_body else task.started_at
		
		task.save()
		return JsonResponse(task.to_json())

	def delete(self: object, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle DELETE requests."""
		task = Task.objects.get(id=self.kwargs['id'])
		task.delete()
		return JsonResponse(task.to_json())

class ChunksView(generic.View):
	"""ChunksView is a generic class base view for the chunks endpoint."""
	def get(self: object, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle GET requests."""
		chunks = Chunk.objects.filter(task_id=self.kwargs['id'])
		return JsonResponse([chunk.to_json() for chunk in chunks], safe=False)

	def post(self: object, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle POST requests."""
		request_body = json.loads(request.body)

		titles = request_body['title'].splitlines()

		chunks: list[Chunk] = []

		for title in titles:
			if title:
				chunk = Chunk.objects.create(
					title = title,
					task_id = self.kwargs['task_id']
				)
				chunk.save()
				chunks.append(chunk)

		return JsonResponse([chunk.to_json() for chunk in chunks], safe=False)

class ChunkView(generic.View):
	"""ChunkView is a generic class base view for the chunk endpoint."""
	def get(self: object, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle GET requests."""
		chunk: Chunk = Chunk.objects.get(id=self.kwargs['id'])
		return JsonResponse(chunk.to_json())

	def put(self: object, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle PUT requests."""
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		request_body = json.loads(request.body)
		chunk.title   = request_body['title']
		if request_body['finishedAt']:
			chunk.finished_at = request_body['finishedAt']

		chunk.save()
		return JsonResponse(chunk.to_json())

	def delete(self: object, *args: Any, **kwargs: Any) -> JsonResponse:
		"""Handle DELETE requests."""
		chunk = Chunk.objects.get(id=self.kwargs['id'])
		chunk.delete()
		return JsonResponse(chunk.to_json())